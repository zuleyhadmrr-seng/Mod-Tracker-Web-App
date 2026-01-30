from flask import Flask
import os

# ATTENTION: Since we moved models.py to the 'website' folder, we updated the import path:
from website.models import db, Category, add_category, add_mod, get_all_mods, update_mod, delete_mod, get_mod_by_id

app = Flask(__name__)

# --- SETTINGS (SQLite instead of SQL Server) ---
# We ensure the database file is created inside the 'website' folder
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'website', 'database.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the database to this test application
db.init_app(app)

def print_Mods():
    mods = get_all_mods()
    if not mods:
        print("No mods found to list.")
    for m in mods:
        print(f"{m.id} | {m.name} | {m.version} | {m.category.name}")
    print("-----------------------")

# --- TEST OPERATIONS ---
with app.app_context():
    # Create tables if they don't exist (First run)
    db.create_all()

    print("\n1) Adding new category")
    # Using try-except to prevent error if category already exists
    try:
        yeni_kat = add_category("TestCategory")
        print("Category added:", yeni_kat)
    except:
        print("Category might already exist, continuing...")
        yeni_kat = Category.query.filter_by(name="TestCategory").first()

    print("\n2) Adding new mod")
    if yeni_kat:
        yeni_mod = add_mod("TestMod", "v0.1", yeni_kat.id)
        print("Mod added:", yeni_mod)

        print_Mods()

        print("\n3) Updating mod")
        update_mod(yeni_mod.id, name="TestModUpdated", version="v0.2")
        print("Updated mod:", get_mod_by_id(yeni_mod.id))

        print_Mods()

        print("\n4) Deleting mod")
        delete_mod(yeni_mod.id)
        print("Mod deleted.")

        print_Mods()
    else:
        print("Mod could not be added due to category error.")