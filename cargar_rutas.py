#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:41:10 2025

@author: davidcontrerasgarza
"""

import pandas as pd 
import json
from datetime import datetime
import numpy as np
import os

working_directory='/Users/davidcontrerasgarza/Documents/Repositorios_SS/Monitor Financiero/'
os.chdir(working_directory)
from app import *
from python.models import *


def rutas_inciales():
    # crear rutas iniciales
    data = [
        {'nombre': 'Acceso total', 'ruta': '/'},
        {'nombre': 'Inicio', 'ruta': '/'},
        {'nombre': 'Permisos', 'ruta': '/permisos'},
        {'nombre': 'Bases de datos', 'ruta': '/bases_de_datos'}
    ]

    # Create the DataFrame
    rutas = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Administrador").first().id
        for i in range(len(rutas)):
            new_record = Rutas(nombre=rutas['nombre'][i],ruta=rutas['ruta'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

# funcion para crear rutas de formularios
def crear_ruta(nombre_formulario,ruta_principal):
    ruta='/'+ruta_principal.lower()+'/'+nombre_formulario.lower()
    data = [
        {'nombre': 'Acceso total '+nombre_formulario, 'ruta': ruta},
        {'nombre': 'Visualizar '+nombre_formulario, 'ruta': ruta+'/'+'visualizar'},
        {'nombre': 'Formulario '+nombre_formulario, 'ruta': ruta+'/'+'formulario'},
        {'nombre': 'add '+nombre_formulario, 'ruta': ruta+'/'+'add'},
        {'nombre': 'Editar '+nombre_formulario, 'ruta': ruta+'/'+'editar'},
        {'nombre': 'Eliminar '+nombre_formulario, 'ruta': ruta+'/'+'eliminar'}
    ]
    rutas = pd.DataFrame(data)
    with app.app_context():
        id_usuario=Usuarios.query.filter_by(nombre="Administrador").first().id
        for i in range(len(rutas)):
            new_record = Rutas(nombre=rutas['nombre'][i],ruta=rutas['ruta'][i],id_usuario=id_usuario)
            db.session.add(new_record)
        db.session.commit()

# funcion para crear rutas de formularios
def crear_admin():

    with app.app_context():
        data = [
            {'nombre': 'Administrador','correo_electronico':'davidcontrerasgarza@gmail.com','contrasena':'123','estatus': 'Activo'}
        ]
        data = pd.DataFrame(data)
        for i in range(len(data)):
            new_record = Usuarios(nombre=data['nombre'][i],correo_electronico=data['correo_electronico'][i],contrasena=data['contrasena'][i],estatus=data['estatus'][i])
            db.session.add(new_record)
        db.session.commit()

crear_admin()








