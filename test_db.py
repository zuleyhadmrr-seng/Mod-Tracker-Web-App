from flask import Flask
import os

# ATTENTION: Corrected import path since models.py is inside 'website' folder
from website.models import (
    db,
    Category,
    Mod,
    add_category,
    add_mod,
    get_all_mods
)

app = Flask(__name__)

# --- SETTINGS (Switching from SQL Server to SQLite) ---
# We define the database path inside the 'website' folder
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'website', 'database.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Create Tables and Seed Data
with app.app_context():
    try:
        db.create_all()
        print("Tables created or already exist.")

        # If there are no categories, seed sample data
        if not Category.query.first():
            print("Adding sample data...")
            c1 = add_category("Skyrim")
            c2 = add_category("CS:GO")

            add_mod("Realistic Water", "v2.1", c1.id)
            add_mod("Skin Changer", "v1.4", c2.id)
            print("Sample data added.")

        # List mods and print to terminal
        mods = get_all_mods()
        print("Current mods:")
        for m in mods:
            print(f"Mod: {m.name}, Version: {m.version}, Category: {m.category.name}")

    except Exception as e:
        print("ERROR: Issue with connection or table operations.")
        print(e)