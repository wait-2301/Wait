from flask import Flask, render_template
from controllers.admin_panel import admin_pn
from controllers.archive import archive
from controllers.auth import auth
from controllers.managment import management
from controllers.talon import talon
from controllers.profile import profile

import os


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Register blueprints
app.register_blueprint(admin_pn, url_prefix="/admin")
app.register_blueprint(archive, url_prefix="/archive")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(management, url_prefix="/management")
app.register_blueprint(talon, url_prefix="/talon")
app.register_blueprint(profile, url_prefix="/profile")


@app.route("/")
def index():
    return render_template("main.html")


@app.template_filter('phone_format')
def phone_format(phone):

    phone = str(phone)
    phone = ''.join(filter(str.isdigit, phone))
    
    # Format phone number as +7(XXX)XXX-XX-XX
    if len(phone) == 11:  
        return f"+7({phone[1:4]}){phone[4:7]}-{phone[7:9]}-{phone[9:11]}"
    else:
        return phone  


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


