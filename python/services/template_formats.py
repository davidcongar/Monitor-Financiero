from app import app
from datetime import datetime
# Filtro para formatear números con comas
def commafy(value):
    if value:
        return f"{round(value, 2):,}"
    else:
        return 0

# Filtro para formatear nombres de bases
def title_format(value):
    if value=='id':
        return 'ID'
    else:
        return value.replace("_", " ").capitalize().replace('Id','ID')

# Filtro para formatear nombres de bases
def money_format(value):
    return f"${round(value, 2):,}"


# Ejemplo de uso

app.jinja_env.filters["commafy"] = commafy
app.jinja_env.filters["money_format"] = money_format
app.jinja_env.filters["title_format"] = title_format
