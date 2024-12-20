from flask import Flask, jsonify, render_template
from flask import Blueprint, jsonify
from utils.decorators import login_required
import services.archive_service as AS

archive = Blueprint('archive', __name__)


@archive.route("/")
@login_required
def archives():
    return render_template("archive.html")

@archive.route("/history")
@login_required
def get_archive():
    history = AS.get_archive()
 
    print(history)
    return jsonify(history)







