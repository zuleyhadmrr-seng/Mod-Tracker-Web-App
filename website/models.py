from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class Category(db.Model):  #table for categories
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    mods = db.relationship("Mod", backref="category", lazy=True)

class Mod(db.Model): #table for the mods
    __tablename__ = 'mods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    version = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    developer = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), default="Active")
    date_added = db.Column(db.DateTime(timezone=True), default=func.now())

    filename = db.Column(db.String(255), nullable=True) 

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)

def get_mod_by_id(id): #finds a mod by its ID
    return Mod.query.get(id)

def delete_mod(id): #deletes a mod from the database
    mod = Mod.query.get(id)
    if mod:
        db.session.delete(mod)
        db.session.commit()