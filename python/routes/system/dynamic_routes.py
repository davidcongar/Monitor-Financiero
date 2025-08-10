# python/routes/dynamic_routes.py

from datetime import datetime

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for,session

from python.models import db
from python.models.modelos import *
from python.services.helper_functions import *
from python.services.form_workflows.edit_on_success import *
from python.services.form_workflows.on_success import *
from python.services.authentication import *
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm.dynamic import AppenderQuery
from sqlalchemy.orm import aliased
from python.services.dynamic_routes_functions import *
from python.services.boto3_s3 import S3Service
s3_service = S3Service()

# Crear un Blueprint para rutas dinámicas basado en el nombre de la tabla
dynamic_bp = Blueprint("dynamic", __name__, url_prefix="/dynamic")


@dynamic_bp.route("/<table_name>")
@login_required
def table_view(table_name):
    """
    Ruta para listar todos los registros de una tabla de forma dinámica.
    """
    model = get_model_by_name(table_name)
    if not model:
        flash(f"La tabla '{table_name}' no existe.", "danger")
        return redirect(url_for("home.home"))

    # Obtener las columnas definidas en el modelo
    columns=get_table_columns().get(table_name)
    if columns==None:
        columns = model.__table__.columns.keys()
        # Get Many-to-Many relationships
        many_to_many_columns = [
            rel.key for rel in model.__mapper__.relationships.values()  if rel.secondary is not None and "archivos" not in rel.key.lower() and "rutas" not in rel.key.lower()
        ]
        # Combine both lists
        columns = columns + many_to_many_columns

    # Datos para resaltar el menú activo en el sidebar
    module,active_menu=get_breadcrumbs(table_name)

    context = {
            "activeMenu": active_menu, 
            "activeItem": table_name,
            "breadcrumbs": [{"name":module,"url":""},{"name":table_name.replace('_', ' ').capitalize(),"url":""}]
        }
    buttons_modal_exits = os.path.exists(f'templates/partials/table/modals/{table_name}.html')
    tabs_exist = os.path.exists(f'templates/partials/table/tabs/{table_name}.html')
    table_buttons = os.path.exists(f'templates/partials/table/buttons/{table_name}.html')
    number_buttons=get_table_buttons().get(table_name,0)
    if tabs_exist:
        data_tabs=get_data_tabs(table_name)
    else:
        data_tabs={}
    return render_template(
        "dynamic_table.html",
        buttons_modal_exits=buttons_modal_exits,
        tabs_exist=tabs_exist,
        columns=columns,
        table_name=table_name,
        table_buttons=table_buttons,
        data_tabs=data_tabs,
        number_buttons=number_buttons,
        **context,
    )

@dynamic_bp.route("/<table_name>/form", methods=["GET", "POST"])
@login_required
def form(table_name):
    model = get_model_by_name(table_name)
    if not model:
        flash(f"La tabla '{table_name}' no existe.", "danger")
        return redirect(url_for("dynamic.table_view", table_name=table_name))
    ignored_columns=get_ignored_columns(table_name)
    columns = [col for col in model.__table__.columns.keys() if col not in ignored_columns]
    columnas_no_obligatorios=get_non_mandatory_columns(table_name)
    required_fields=[col for col in columns if col not in columnas_no_obligatorios]

    foreign_options = get_foreign_options()
    estatus_options =  get_estatus_options().get(table_name, {"Activo", "Inactivo"})
    foreign_options["estatus"] = estatus_options

    # Add Many-to-Many relationships
    many_to_many_data = {}
    for attr_name, attr in model.__mapper__.relationships.items():
        if attr.secondary is not None:  # Ensures it's Many-to-Many
            related_model = attr.mapper.class_

            # Get selected values for the current record
            selected_items = []

            # Ensure selected_items is iterable
            if isinstance(selected_items, list) or hasattr(selected_items, '__iter__'):
                selected_ids = [item.id for item in selected_items]  
            else:
                selected_ids = [selected_items.id] if selected_items else []

            # Get all available options
            all_options = related_model.query.all()

            # Store in dictionary
            many_to_many_data[attr_name] = {
                "selected": selected_ids,
                "options": all_options
            }
    # Add Multiple choice fields
    multiple_choice_data=get_multiple_choice_data()

    modulo,active_menu=get_breadcrumbs(table_name)

    # edicion
    record_id = request.args.get("id")
    if record_id!=None:
        record = model.query.get(record_id)
        name = getattr(record, "nombre", None)
        accion = f"Editar registro: {name}" if name else "Editar registro "+ str(record.id_visualizacion)
        if not record:
            flash(f"Registro con ID {record_id} no encontrado en '{table_name}'.", "danger")
            return redirect(url_for("dynamic.table_view", table_name=table_name))
    else:
        accion="Registrar"
        record=None
  
    context = {
        "activeMenu": active_menu,
        "activeItem": table_name,
        "foreign_options": foreign_options,
        "breadcrumbs": [{"name":modulo,"url":""},{"name":table_name.replace('_', ' ').capitalize(),"url":url_for("dynamic.table_view", table_name=table_name)},{"name":accion,"url":""}]
    }

    return render_template(
        "dynamic_form.html",
        columns=columns,
        required_fields=required_fields,
        table_name=table_name,
        many_to_many_data=many_to_many_data,
        multiple_choice_data=multiple_choice_data,
        action=accion,
        record=record,
        **context,
    )

@dynamic_bp.route("/<table_name>/add", methods=["POST"])
@login_required
def add(table_name):
    model = get_model_by_name(table_name)
    if not model:
        flash(f"La tabla '{table_name}' no existe.", "danger")
        return redirect(url_for("dynamic.table_view", table_name=table_name))
    try:
        # Retrieve all form data (handling multi-select fields correctly)
        data = {key: request.form.getlist(key) for key in request.form.keys()}
        data.pop('archivo', None)
        data = sanitize_data(model, data)
        # Extract many-to-many fields (to process separately)
        relationship_data = {}
        normal_data = {}
        for key, value in data.items():
            attr = getattr(model, key, None)
            if isinstance(attr, InstrumentedAttribute) and hasattr(attr.property, "mapper"):
                # This is a relationship field
                relationship_data[key] = value  # Store for later processing
            else:
                # Normal field (use first value if it's a list with one element)
                normal_data[key] = value[0] if isinstance(value, list) and len(value) == 1 else value
        # Create new record with only normal fields first
        new_record = model(**normal_data)
        new_record.id_usuario = Usuarios.query.get(session["id_usuario"]).id
        if hasattr(model, 'id_visualizacion'):
            new_record.id_visualizacion=get_id_visualizacion(table_name)
        if table_name=='archivos':
            file_uuid=str(uuid.uuid4())
            archivo = request.files.get("archivo")
            s3_service.upload_file(archivo, file_uuid)
            new_record.tabla_origen=session['tabla_origen']
            new_record.id_registro=session['id_registro_tabla_origen']
            new_record.nombre=archivo.filename
            new_record.ruta_s3=f"{file_uuid}_{archivo.filename}"
        if table_name=='usuarios':
            alphabet = string.ascii_letters + string.digits
            contrasena = ''.join(secrets.choice(alphabet) for i in range(20))
            new_record.contrasena=generate_password_hash(contrasena)
            new_user_email(new_record.correo_electronico,contrasena)
        db.session.add(new_record)
        db.session.flush()
        # Process many-to-many relationships
        for key, value in relationship_data.items():
            related_model = getattr(model, key).property.mapper.class_
            # Convert IDs to actual objects
            selected_items = db.session.query(related_model).filter(related_model.id.in_([int(v) for v in value if v])).all()
            # Assign relationship
            getattr(new_record, key).extend(selected_items)
        # Commit transaction
        db.session.commit()
        on_success(table_name,new_record.id)
        flash(f"Registro creado exitosamente en '{table_name.replace('_', ' ').capitalize()}'.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al crear el registro: {str(e)}", "danger")
    return redirect(url_for("dynamic.table_view", table_name=table_name))

@dynamic_bp.route("/<table_name>/data", methods=["GET"])
@login_required
def data(table_name):
    model = get_model_by_name(table_name)
    if not model:
        return jsonify({"error": f"La tabla '{table_name}' no existe."}), 404

    # Obtener parámetros de consulta
    view = request.args.get("view", 50, type=int)
    search = request.args.get("search", "", type=str)
    sortField = request.args.get("sortField", "fecha_de_creacion", type=str)
    sortRule = request.args.get("sortRule", "desc", type=str)
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status", "", type=str)
    dateRange=request.args.get("dateRange", "", type=str)

    if table_name in ("usuarios", "logs_auditoria"):
        query = model.query
    else:
        query = model.query.filter_by(id_usuario=session["id_usuario"])

    # Agregar joins condicionales
    joins = get_joins()
    filtered_joins = {
        field: val for field, val in joins.items() if field in model.__table__.columns
    }

    for field, (table, id_column, name_column) in filtered_joins.items():
        # Asegura que el campo exista en el modelo base
        if field not in model.__table__.columns:
            continue

        # Crea un alias único por campo (soporta varias uniones al mismo modelo)
        alias = aliased(table, name=f"{table.__tablename__}__{field}")

        # Re-vincula columnas al alias
        alias_id_col = getattr(alias, id_column.key)
        alias_name_col = getattr(alias, name_column.key)

        # Join explícito y ON explícito contra el modelo base
        query = (
            query.outerjoin(alias, alias_id_col == getattr(model, field))
                .add_columns(alias_name_col.label(f"{field}_{name_column.key}"))
        )

    # Aplicar búsqueda
    if search:
        query = search_table(query, model, search, filtered_joins)

    #if table_name=='archivos':
        #query=query.filter(Archivos.id_registro==session['id_registro_tabla_origen'])

    status_field = get_tabs().get(table_name,'estatus')

    if status != 'todos':
        query = query.filter(getattr(model, status_field) == status)
    

    if dateRange:
        try:
            start_str, end_str = dateRange.split(" to ")
            start_date = start_str.strip()
            end_date = end_str.strip()
            query = query.filter(model.fecha.between(start_date, end_date))
        except:
            query = query.filter(model.fecha.between(dateRange, dateRange))

    # Contar registros filtrados
    total = query.count()

    # Aplicar ordenamiento
    if sortField in model.__table__.columns:
        column_attr = getattr(model, sortField)
        query = query.order_by(column_attr.asc() if sortRule.lower() == "asc" else column_attr.desc())
    else:
        query = query.order_by(model.id.asc())

    # Aplicar paginación
    query = query.offset((page - 1) * view).limit(view)
    records = query.all()

    # Convertir registros a diccionario
    def record_to_dict(record):
        # Si es un Row (joined query), unpack del mapping
        if hasattr(record, "_mapping"):
            record_mapping = record._mapping
            model_instance = record_mapping.get(model, record)
        else:
            record_mapping = {}
            model_instance = record

        # Construir diccionario base con las columnas del modelo principal
        model_dict = {
            col: (
                getattr(model_instance, col).isoformat()
                if hasattr(getattr(model_instance, col), "isoformat")
                else getattr(model_instance, col)
            )
            for col in model_instance.__table__.columns.keys()
        }

        # Agregar columnas de joins (usando alias definidos al hacer el JOIN)
        for fk_field, (_, _, name_column) in joins.items():
            label_name = f"{fk_field}_{name_column.name}"  # usamos el nombre de la columna
            if label_name in record_mapping:
                model_dict[fk_field] = record_mapping[label_name]

        return model_dict


    items = [record_to_dict(record) for record in records]

    return jsonify(
        {
            "items": items,
            "total": total,
            "pages": (total + view - 1) // view, 
            "totals": {},  
        }
    )

@dynamic_bp.route("/<table_name>/delete", methods=["POST"])
@login_required
def delete(table_name):
    model = get_model_by_name(table_name)
    if not model:
        flash(f"La tabla '{table_name}' no existe.", "danger")
        return redirect(url_for("home.home"))

    record_id = request.args.get("id")  # Obtener como cadena
    if record_id is None:
        flash("No se especificó el ID del registro a eliminar.", "danger")
        return redirect(url_for("dynamic.table_view", table_name=table_name))

    # Determinar el tipo de la clave primaria
    primary_key_column = list(model.__table__.primary_key.columns)[0]
    if primary_key_column.type.python_type is int:
        try:
            record_id = int(record_id)
        except ValueError:
            flash("El ID del registro debe ser numérico.", "danger")
            return redirect(url_for("dynamic.table_view", table_name=table_name))

    record = model.query.get(record_id)
    if not record:
        flash(f"Registro con ID {record_id} no encontrado en '{table_name}'.", "danger")
        return redirect(url_for("dynamic.table_view", table_name=table_name))

    try:
        db.session.delete(record)
        db.session.commit()
        flash(f"Registro eliminado exitosamente en '{table_name.replace('_', ' ').capitalize()}'.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error al eliminar el registro: {str(e)}", "danger")

    return redirect(url_for("dynamic.table_view", table_name=table_name))

@dynamic_bp.route("/<table_name>/edit", methods=["GET", "POST"])
@login_required
def edit(table_name):
    """
    Endpoint alternativo para editar un registro.
    Se espera recibir el ID del registro a editar mediante un parámetro de query (por ejemplo, ?id=22).
    """
    model = get_model_by_name(table_name)
    if not model:
        flash(f"La tabla '{table_name.replace('_', ' ').capitalize()}' no existe.", "danger")
        return redirect(url_for("home.home"))

    record_id = request.args.get("id")
    if record_id is None:
        flash("No se especificó el ID del registro a editar.", "danger")
        return redirect(url_for("dynamic.table_view", table_name=table_name))

    record = model.query.get(record_id)
    if not record:
        flash(f"Registro con ID {record_id} no encontrado en '{table_name}'.", "danger")
        return redirect(url_for("dynamic.table_view", table_name=table_name))

    if request.method == "POST":
        try:
            # Convertir y sanitizar los datos enviados
            data = {key: request.form.getlist(key) for key in request.form.keys()}  # Ensure multi-select fields get all values
            data = sanitize_data(model, data)
            for key, value in data.items():
                if key != "fecha_de_creacion" and hasattr(record, key):
                        attr = getattr(record.__class__, key)
                        # Check if the field is a relationship (Many-to-Many)
                        if isinstance(attr, InstrumentedAttribute) and hasattr(attr.property, 'mapper'):
                            related_model = attr.property.mapper.class_
                            # Convert selected IDs to integers
                            selected_ids = [int(v) for v in value if v] if value else []
                            # Query related objects and update relationship
                            selected_items = db.session.query(related_model).filter(related_model.id.in_(selected_ids)).all()
                            getattr(record, key).clear()  # Clear existing relationships
                            getattr(record, key).extend(selected_items)  # Add new selections

                        else:
                            # Assign normal fields
                            setattr(record, key, value[0] if isinstance(value, list) and len(value) == 1 else value)
            db.session.commit()
            edit_on_success(table_name,record.id)
            flash(f"Registro actualizado exitosamente en '{table_name.replace('_', ' ').capitalize()}'.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error al actualizar el registro: {str(e)}", "danger")
        return redirect(url_for("dynamic.table_view", table_name=table_name))

@dynamic_bp.route("/<table_name>/data/<id_registro>", methods=["GET"])
@login_required
def record_data(table_name,id_registro):
    model = get_model_by_name(table_name)
    if not model:
        return jsonify({"error": f"La tabla '{table_name}' no existe."}), 404

    # Iniciar la consulta
    query = model.query

    # Agregar joins condicionales
    joins = get_joins()
    filtered_joins = {
        field: val for field, val in joins.items() if field in model.__table__.columns
    }

    for field, (table, id_column, name_column) in filtered_joins.items():
        # Asegura que el campo exista en el modelo base
        if field not in model.__table__.columns:
            continue

        # Crea un alias único por campo (soporta varias uniones al mismo modelo)
        alias = aliased(table, name=f"{table.__tablename__}__{field}")

        # Re-vincula columnas al alias
        alias_id_col = getattr(alias, id_column.key)
        alias_name_col = getattr(alias, name_column.key)

        # Join explícito y ON explícito contra el modelo base
        query = (
            query.outerjoin(alias, alias_id_col == getattr(model, field))
                .add_columns(alias_name_col.label(f"{field}_{name_column.key}"))
        )

    query=query.filter(model.id == id_registro)
    # Aplicar paginación
    records = query.all()
    def record_to_ordered_list(record, table_name):
        columns_order = get_columns_order().get(table_name)
        ordered_fields = []

        if hasattr(record, "_mapping"):
            record_mapping = record._mapping
            model_instance = record_mapping.get(model, record)
        else:
            record_mapping = {}
            model_instance = record

        # Step 1: Base model columns
        base_data = {
            col: (
                getattr(model_instance, col).isoformat()
                if hasattr(getattr(model_instance, col), "isoformat")
                else getattr(model_instance, col)
            )
            for col in model.__table__.columns.keys()
        }

        # Step 2: Foreign key fields with joined data
        for fk_field, (_, _, name_column) in joins.items():
            label_name = f"{fk_field}_{name_column.name}"  # usamos el nombre de la columna
            if label_name in record_mapping:
                base_data[fk_field] = record_mapping[label_name]
                
        # Step 4: Build ordered output based on config
        if columns_order:
            for col in columns_order:
                # Support dotted notation: Roles.nombre -> id_rol_nombre
                if "." in col:
                    table_alias, column_name = col.split(".")
                    alias_field = f"id_{table_alias.lower()}_{column_name}"
                    value = record_mapping.get(alias_field)
                else:
                    value = base_data.get(col)
                if value is not None:
                    ordered_fields.append((col, value))
        else:
            # Default to base_data order
            ordered_fields = list(base_data.items())

        return ordered_fields


    record = [record_to_ordered_list(record,table_name) for record in records]

    return jsonify(record)
