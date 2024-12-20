from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Временные данные сотрудника
employee = {
    "first_name": "Нурдаулет",
    "last_name": "Салимов",
    "patronymic": "",
    "position": "Администратор",  # Измените на "Менеджер", чтобы проверить видимость кнопки
    "table_number": "3",
}

# Временное хранилище для пользователей
users = []

@app.route('/profile')
def profile():
    return render_template('profile.html', employee=employee)

@app.route('/register_manager', methods=['POST'])
def register_manager():
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    if not phone or not password:
        return jsonify({"error": "Номер телефона и пароль обязательны"}), 400

    # Проверка на существующего пользователя
    if any(user['phone'] == phone for user in users):
        return jsonify({"error": "Пользователь с таким номером телефона уже существует"}), 400

    # Добавляем нового менеджера
    new_user = {"phone": phone, "password": password}
    users.append(new_user)

    return jsonify({"message": "Менеджер успешно зарегистрирован", "users": users}), 201

if __name__ == '__main__':
    app.run(debug=True)
