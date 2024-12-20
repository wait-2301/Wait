from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from utils.decorators import login_required
import services.queue_service as QM
import services.user_service as US
import re


auth = Blueprint('auth', __name__)

# @auth.route("/login")
# def login():
#     return render_template("vhod.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]
        
        # Clean the phone number (remove non-numeric characters)
        cleaned_phone = ''.join(filter(str.isdigit, phone))
        print("/sda.fadaf///////////////////////////")
        try:
            
            user = US.get_user_by_phone_number_service(cleaned_phone)

            is_valid = check_password_hash(user[4], password)
            if is_valid:
                print("Password is correct!")
            else:
                print("Invalid password!")
            print(user)
            if user:
                # Login successful
                session['user_id'] = user[1]  # Store user id in the session
                print(session.get('user_id'))
                return redirect(url_for('profile.get_profile'))  # Redirect to the dashboard
            else:
                error = "Неправильный номер телефона или пароль."
                return render_template("vhod.html", error=error)
        except Exception as e:
            print(f"Error: {e}")
            return "Произошла ошибка при обработке запроса."
    
    return render_template("vhod.html")





@auth.route('/register', methods=['GET', 'POST'])
def register():
    print("Begin")  # Check if route is being triggered
    print(f"Received {request.method} request at {request.url}")
    
    if request.method == 'POST':
        print(f"Form Data: {request.form}")  # Debug form data
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        purpose = request.form.get('purpose')
        queue_type = request.form.get('queue_type')

        # Clean the phone number to keep only digits
        cleaned_phone = re.sub(r'\D', '', phone)
        print(f"Cleaned Phone: {cleaned_phone}")  # Debug print

        try:
            full_name = f"{first_name} {last_name}"
            print(f"Inserting into queue service for phone: {cleaned_phone}")
            QM.insert_into_queue_service(cleaned_phone, full_name, None, purpose)
            session['user_id'] = cleaned_phone
        
            if queue_type == "Долговременная запись":
                return redirect(url_for('auth.submit_time'))
            else:
                return redirect(url_for('talon.get_talon'))
        except Exception as e:
            print(f"Error: {e}")
            return f"An error occurred while saving the data: {e}"

    return render_template('vvod_dannyh.html')


@auth.route('/r/submit_time', methods=['GET', 'POST'])
def submit_time():
    if request.method == 'POST':
        date = request.form.get('date')
        time = request.form.get('time')
        user_id = session.get('user_id')

        if not user_id:
            return redirect(url_for('auth.register'))
        
        try:
            # Example of saving to the queue service (update to match your logic)
            QM.update_queue_time_service(user_id, date, time)
            return redirect(url_for('talon.get_talon'))
        except Exception as e:
            print(f"Error: {e}")
            return f"An error occurred while saving the date and time: {e}"

    return render_template('zapis_vremya.html')



@auth.route('/success')
def success():
    return "Data saved successfully!"