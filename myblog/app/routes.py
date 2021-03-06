import os
from ast import Not
from distutils.log import Log
from flask import render_template, flash, redirect, url_for,request
from app import app,db,photos
from app.forms import LoginForm, RegistForm , ProfileEditingForm, PostingForm,UploadImageForm
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Post, Images
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from datetime import datetime
from app.forms import EmptyForm
import boto3

s3_client = boto3.client('s3', aws_access_key_id = app.config['S3_KEY'],
                        aws_secret_access_key= app.config['S3_SECRET'],
                        aws_session_token = app.config['S3_SESSION_TOKEN']
                        )
s3_resources = boto3.resource('s3', aws_access_key_id = app.config['S3_KEY'],
                        aws_secret_access_key= app.config['S3_SECRET'],
                        aws_session_token = app.config['S3_SESSION_TOKEN']
                        )

BUCKET_NAME='mybloghost'
@app.route('/',methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostingForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page',1,type = int)
    posts = current_user.followed_posts().paginate(
        page,app.config['POSTS'], False
    )
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('index.html', title='Home', form=form,
                        posts=posts.items, next_url=next_url,
                        prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_p(form.password.data):
            flash('Recheck username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc!='':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_p(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page',1,type= int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,ext_url=next_url, prev_url=prev_url,form=form)

@app.before_request
def beforeRequest():
    if current_user.is_authenticated:
        current_user.lastSeen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileEditingForm(current_user.username,current_user.email)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.aboutMe = form.aboutMe.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.aboutMe.data = current_user.aboutMe
    return render_template('edit_user_profile.html', title='Edit Profile',form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS'], False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template("explore.html", title='Explore', posts=posts.items,next_url=next_url, prev_url=prev_url)


@app.route('/upload_image',methods=['GET','POST'])
@login_required
def upload_image():
    """
    form = UploadImageForm()
    if form.validate_on_submit():
        
        #filename = photos.save(form.photo.data)
        filename = form.photo.data
        image = Images(user_id = current_user.id,image_uri=filename)
        db.session.add(image)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        file_url = None
    return render_template("upload_image.html",title="Upload Image",form = form)
    """
    msg = ""
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)  
            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    flash("Image only")
                    return render_template("upload_image.html",msg ="Image only!")
         
            s3_client.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
            )
            msg = "Upload Done ! "
            image = Images(user_id = current_user.id,image_uri=filename)
            db.session.add(image)
            db.session.commit()
            
            
    return render_template("upload_image.html",msg =msg)


@app.route('/gallery',methods=['GET'])
@login_required
def gallery():
    imgs = Images.query.filter_by(user_id=current_user.id)
    imgs_paths=[]
    for img in imgs:
        imgs_paths.append(app.config['S3_LOCATION']+img.image_uri)
    for img_path in imgs_paths:
        print(img_path)
   
    
    return render_template("gallery.html",title="Gallery",paths = imgs_paths)


