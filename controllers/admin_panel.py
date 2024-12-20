from flask import Blueprint, jsonify, render_template
from utils.decorators import login_required

# Create a blueprint
admin_pn = Blueprint("admin", __name__)

# Static list of managers
managers = [
    {"name": "Кумисбек Ариана", "table": "СТОЛ 1", "status": "Доступен"},
    {"name": "Казанбасова Амина", "table": "СТОЛ 2", "status": "Доступен"},
    {"name": "Таукен Аспандияр", "table": "СТОЛ 3", "status": "В процессе"},
    {"name": "Агабай Аида", "table": "СТОЛ 4", "status": "Не доступен"},
    {"name": "Сейпыш Алан", "table": "СТОЛ 5", "status": "Доступен"},
]

# Routes for the admin panel
@admin_pn.route("/")
@login_required
def index():
    return render_template("admin_panel.html")


@admin_pn.route("/managers")
def get_managers():
    return jsonify(managers)
