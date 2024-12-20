from flask import Flask, Blueprint, jsonify, render_template, request, redirect, url_for, session
import services.queue_service as QM
import re

talon = Blueprint('talon', __name__)

@talon.route('/')
def get_talon():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('register'))

    queue = QM.get_queue_by_user_id_service(user_id)
    if not queue:
        return "Пользователь не найден."

    ticket_number = f"B{str(queue.queue_number)}"
    return render_template('talon.html', queue=queue, ticket_number=ticket_number)