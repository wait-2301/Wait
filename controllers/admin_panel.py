from flask import Blueprint, jsonify, render_template
from utils.decorators import login_required
import services.admin_panel_service as AS

# Create a blueprint
admin_pn = Blueprint("admin", __name__)


# Routes for the admin panel
@admin_pn.route("/")
@login_required
def index():
    return render_template("admin_panel.html")


@admin_pn.route("/managers")
def get_managers():
    managers = AS.get_managers_service()
    print(managers)
    return jsonify(managers)
