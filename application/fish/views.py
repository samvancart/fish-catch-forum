from flask import Flask, redirect, render_template, request, url_for, abort, flash, session
from flask_login import current_user
from io import BytesIO

import os
from application import app, db, login_required,set_session_group
from application.fish.models import Fish
from application.fish.forms import FishForm
from application.auth.models import User,groups
from application.group.models import Group



@app.route("/<int:group_id>/fish", defaults={"group_name":1})
@app.route("/<int:group_id>/fish", methods=["GET"])
def fish_index(group_id):
    users=User.query.all()
    id = group_id
    # id = session['group']
    fish = Fish.query.filter(Fish.group_id==id)
    no_posts = User.find_users_with_no_posts(id)
    for f in fish:
        save_download_picture(f)


    return render_template("fish/list.html", fish=fish, users=users,
                no_posts=no_posts)



def save_download_picture(fish):
    picture_path = os.path.join(app.root_path, 'static/pictures', fish.image_file)
    writeTofile(fish.image_blob,picture_path)


def save_picture(form_picture,fish_id):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = "picture" + str(fish_id) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    print("IMAGE PATH ",picture_path)
    # form_picture.save(picture_path)
    print("PICTURE_FN ",picture_fn)
    return picture_fn

def user_is_in_group(group_id):
    users= User.query.join(groups).join(Group).filter((groups.c.account_id == User.id)
    & (groups.c.group_id == group_id)).all()
    return current_user in users

def save_upload_picture(form_picture,fish_id):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = "picture" + str(fish_id) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    form_picture.save(picture_path)
    return picture_path

def delete_blob(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def writeTofile(data, filename):
    delete_picture_from_folder(filename)

    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

def delete_picture_from_folder(filename):
    osPath =  os.path.dirname(os.path.abspath(__file__))
    newPath = os.path.dirname(osPath)
    file_path = newPath+filename
    print("file_path ",file_path)
    if os.path.isfile(file_path):
        os.remove(file_path)



@app.route("/<int:group_id>/fish/new", defaults={"group_id":1})
@app.route("/<int:group_id>/fish/new", methods=['GET', 'POST'])
@login_required(role="ADMIN")
def fish_new(group_id):
    form = FishForm()
    fish = None
    active_group = Group.query.get(group_id)
    if request.method == 'GET':
        if not user_is_in_group(group_id):
            return redirect(url_for('group_index'))

        return render_template("fish/new.html", fish=fish, form=FishForm(),
                               title='New post', legend='New post', value='Add post')

    if not form.validate_on_submit():
        return render_template('fish/new.html',fish=fish, form=form,
            title='New post', legend='New post', value='Add post')

    f = Fish(form.species.data)
    f.weight = form.weight.data
    f.account_id = current_user.id
    f.group_id = group_id

    if not form.picture.data:
        db.session.add(f)
        db.session.commit()
        return redirect(url_for("fish_index",group_id=group_id))


    fish_id = db.session.query(Fish).count()
    picture_file = save_picture(form.picture.data,fish_id)
    flash('New catch created!', 'success')
    f.image_file = picture_file

    # BLOB
    print("FORM_PICTURE_DATA: ",form.picture.data)
    file_path = save_upload_picture(form.picture.data,fish_id)
    binaryData = convertToBinaryData(file_path)
   
    f.image_blob=binaryData

    db.session.add(f)
    db.session.commit()

    delete_blob(file_path)

    return redirect(url_for("fish_index",group_id=group_id))




@app.route("/fish/<int:fish_id>")
def fish_view(fish_id):

    fish = Fish.query.get_or_404(fish_id)
    user = User.query.get_or_404(fish.account_id)

    if fish.image_file is None:
         return render_template("fish/view.html", fish=fish, user=user)

    save_download_picture(fish)

    picture = url_for('static', filename='pictures/'+ fish.image_file)

    myfile=os.path.exists('\\application')
    osPath =  os.path.dirname(os.path.abspath(__file__))

    newPath = os.path.dirname(osPath)
    print("OS .. ", newPath)
    print("NEW PATH ",newPath+picture)

    return render_template("fish/view.html", fish=fish, user=user, picture=picture)


def delete_picture(image_file):
    file_path=""
    print("DELETE_PIC_IMAGE",image_file)
    if  image_file is not None:
        picture = url_for('static', filename='pictures/'+ image_file)
        print("picture", picture)
        osPath =  os.path.dirname(os.path.abspath(__file__))
        newPath = os.path.dirname(osPath)
        file_path = newPath+picture

    if os.path.isfile(file_path):
        os.remove(file_path)

@app.route("/fish/<int:fish_id>/<int:group_id>/delete", methods=['POST'])
@login_required
def fish_delete(fish_id,group_id):

    fish = Fish.query.get_or_404(fish_id)
    user = User.query.get_or_404(fish.account_id)
    print("user.id ", user.id, " current_user.id ", current_user.id)

    delete_picture(fish.image_file)
    
    if user.id != current_user.id:
        abort(403)

    db.session.delete(fish)
    db.session.commit()

    flash('Your Catch has been deleted!', 'success')

    return redirect(url_for('fish_index',group_id=group_id))


@app.route("/fish/<int:fish_id>/update", methods=['GET', 'POST'])
@login_required
def fish_update(fish_id):
    fish = Fish.query.get_or_404(fish_id)
    user = User.query.get_or_404(fish.account_id)
    print(user.username)

    print("CHECK ", request.form.get('delete-picture'))

    if user.id != current_user.id:
        abort(403)
    form = FishForm()

    if form.validate_on_submit():
        fish.species = form.species.data
        fish.weight = form.weight.data

        if request.form.get('delete-picture'):
            fish_picture_delete(fish_id)
            return redirect(url_for('fish_view', fish_id=fish.id))

        if not form.picture.data:
            db.session.commit()
            return redirect(url_for('fish_view', fish_id=fish.id))
        
        id = int(fish_id)-1
        fish_id = str(id)

        delete_picture(fish.image_file)

        picture_file = save_picture(form.picture.data,fish_id)
        print("PIC_FILE ",picture_file )
        fish.image_file = picture_file
        print("FISH ID ",fish_id)
        file_path = save_upload_picture(form.picture.data,fish_id)
        binaryData = convertToBinaryData(file_path)
   
        fish.image_blob=binaryData

        db.session.delete(fish)
        db.session.add(fish)

        db.session.commit()

        flash('Your Catch has been updated!', 'success')

        return redirect(url_for('fish_view', fish_id=fish.id))

    elif request.method == 'GET':
        form.species.data = fish.species
        form.weight.data = fish.weight
        print("FISH ID ",fish_id)
        
    if fish.image_file is None:
        picture = ""
        return render_template("fish/new.html", fish = fish, form=form, picture = picture,
                        title='Update post', legend='Update post', value='Update post')

    picture = url_for('static', filename='pictures/'+ fish.image_file)
    return render_template("fish/new.html", fish = fish, form=form, picture = picture,
                           title='Update post', legend='Update post', value='Update post')

def fish_picture_delete(fish_id):
    fish = Fish.query.get_or_404(fish_id)
    form = FishForm()
    print('FISH.IMAGE.FILE ',fish.image_file)
    
    delete_picture(fish.image_file)
    
    db.session.delete(fish)

    fish.image_file = ""
    db.session.add(fish)
    db.session.commit()