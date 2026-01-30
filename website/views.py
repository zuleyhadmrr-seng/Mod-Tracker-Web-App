from flask import Blueprint, render_template
from .models import Mod 

views = Blueprint('views', __name__)

@views.route('/')
#it gets all mods from the database and shows them
def home():
    mods = Mod.query.all()
    return render_template("index.html", mods=mods)