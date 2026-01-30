from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from .models import db, Mod, Category, get_mod_by_id, delete_mod

mods = Blueprint('mods', __name__)

@mods.route('/add', methods=['GET', 'POST'])
def add_mod_page():
    if request.method == 'POST': 
        #get data from the form fields
        name = request.form.get('name')
        version = request.form.get('version')
        developer = request.form.get('developer')
        description = request.form.get('description')
        status = "Active" if request.form.get('status') else "Inactive"
     
        file = request.files.get('file')
        filename = None

        category = Category.query.first()
        if not category:
            category = Category(name="General")
            db.session.add(category)
            db.session.commit()
        
        if not name:
            flash('Name is required!', category='error')
        else:
          
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
             
            #create a new Mod entry
            new_mod = Mod(
                name=name, 
                version=version, 
                description=description, 
                developer=developer, 
                category_id=category.id, 
                status=status,
                filename=filename 
            )
            db.session.add(new_mod)
            db.session.commit()
            
            flash('Mod added successfully!', category='success')
            return redirect(url_for('views.home'))

    return render_template('add_mood.html') 

@mods.route('/detail/<int:id>')
def mod_detail(id):
    mod = get_mod_by_id(id)
    if not mod:
        flash("Mod not found.", category='error')
        return redirect(url_for('views.home'))
    return render_template('detail.html', mod=mod)

@mods.route('/delete/<int:id>')
def delete_mod_func(id):  #delete the mod from the database
    delete_mod(id)
    flash('Mod deleted successfully!', category='success')
    return redirect(url_for('views.home'))

#route to download the mod file
@mods.route('/download/<int:id>')
def download_mod(id):
    mod = get_mod_by_id(id)
    if mod and mod.filename:
        try:
            return send_from_directory(
                current_app.config['UPLOAD_FOLDER'], 
                mod.filename, 
                as_attachment=True 
            )
        except FileNotFoundError:
            flash("File not found on server.", category='error')
            return redirect(url_for('mods.mod_detail', id=id))
    
    flash("This mod has no file attached.", category='error')
    return redirect(url_for('mods.mod_detail', id=id))