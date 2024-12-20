from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash
import services.employee_service as ES
import services.user_service as US
import re
from utils.decorators import login_required

profile = Blueprint('profile', __name__)

# employee = {
#     "first_name": "Нурдаулет",
#     "last_name": "Салимов",
#     "patronymic": "",
#     "position": "Менеджер",  # Измените на "Менеджер", чтобы проверить видимость кнопки
#     "table_number": "3",
# } 
@profile.route("/")
@login_required
def get_profile():
    print(session.get("user_id"))
    employee = ES.get_employee_by_id_service(session.get('user_id'))
    return render_template("profile.html", employee=employee)


@profile.route("/edit")
@login_required
def edit_profile():
    return render_template("edit_profile.html")


@profile.route('/register_manager', methods=['POST'])
@login_required
def register_manager():
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    cleaned_phone = re.sub(r'\D', '', phone)
    print(phone, cleaned_phone)

    if not phone or not password:
        return jsonify({"error": "Не все поля заполнены"}), 400

    existing_user = ES.get_employee_by_phone_service(cleaned_phone)
    if existing_user:
        return jsonify({"error": "Пользователь с таким номером телефона уже существует"}), 400

    hashed_password = generate_password_hash(password)

    print(data, phone, hashed_password)
    US.save_user(cleaned_phone, cleaned_phone, hashed_password)

    return jsonify({"success": True, "message": "Менеджер успешно зарегистрирован"}), 201
