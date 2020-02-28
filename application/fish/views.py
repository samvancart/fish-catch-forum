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
    set_session_group(group_id)
    fish = Fish.query.filter(Fish.group_id==id)
    no_posts = User.find_users_with_no_posts(id)
    at_least_posts = User.find_users_with_at_least_3_posts_in_group(id)
    for f in fish:
        download_picture_save(f)


    return render_template("fish/list.html", fish=fish, users=users,
                no_posts=no_posts,at_least_posts=at_least_posts)



def download_picture_save(fish):
    if fish.image_file is not "" and fish.image_file is not None:
        picture_path = os.path.join(app.root_path, 'static/pictures', fish.image_file)
        writeTofile(fish.image_blob,picture_path)


def picture_save(form_picture,fish_id):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = "picture" + str(fish_id) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)

    return picture_fn

def user_is_in_group(group_id):
    users= User.query.join(groups).join(Group).filter((groups.c.account_id == User.id)
    & (groups.c.group_id == group_id)).all()
    return current_user in users

def upload_picture_save(form_picture,fish_id):
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = "picture" + str(fish_id) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)
    form_picture.save(picture_path)
    return picture_path

def blob_delete(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)


def convertToBinaryData(filename):

    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def writeTofile(data, filename):
    picture_delete_from_folder(filename)

    with open(filename, 'wb') as file:
        file.write(data)

def picture_delete_from_folder(filename):
    osPath =  os.path.dirname(os.path.abspath(__file__))
    newPath = os.path.dirname(osPath)
    file_path = newPath+filename

    if os.path.isfile(file_path):
        os.remove(file_path)



@app.route("/<int:group_id>/fish/new", defaults={"group_id":1})
@app.route("/<int:group_id>/fish/new", methods=['GET', 'POST'])
@login_required(role="ADMIN")
def fish_new(group_id):
    form = FishForm()
    fish = None
    active_group = Group.query.get(group_id)
    set_session_group(group_id)
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
    picture_file = picture_save(form.picture.data,fish_id)
    flash('New catch created!', 'success')
    f.image_file = picture_file

    # blob
    file_path = upload_picture_save(form.picture.data,fish_id)
    binaryData = convertToBinaryData(file_path)
   
    f.image_blob=binaryData

    db.session.add(f)
    db.session.commit()

    blob_delete(file_path)

    return redirect(url_for("fish_index",group_id=group_id))




@app.route("/fish/<int:fish_id>")
def fish_view(fish_id):

    fish = Fish.query.get_or_404(fish_id)
    user = User.query.get_or_404(fish.account_id)

    if fish.image_file is None:
         return render_template("fish/view.html", fish=fish, user=user)

    download_picture_save(fish)

    picture = url_for('static', filename='pictures/'+ fish.image_file)

    myfile=os.path.exists('\\application')
    osPath =  os.path.dirname(os.path.abspath(__file__))

    newPath = os.path.dirname(osPath)


    return render_template("fish/view.html", fish=fish, user=user, picture=picture)


def picture_delete(image_file):
    file_path=""

    if  image_file is not None:
        picture = url_for('static', filename='pictures/'+ image_file)
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

    picture_delete(fish.image_file)
    
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

        picture_delete(fish.image_file)

        picture_file = picture_save(form.picture.data,fish_id)
        fish.image_file = picture_file
        file_path = upload_picture_save(form.picture.data,fish_id)
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
    
    picture_delete(fish.image_file)
    db.session.delete(fish)

    fish.image_file = ""
    db.session.add(fish)
    db.session.commit()