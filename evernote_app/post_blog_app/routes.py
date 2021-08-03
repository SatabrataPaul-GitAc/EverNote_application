from flask import render_template,url_for,flash,redirect,request,abort
from post_blog_app import web_app,db,bcrypt_obj
from post_blog_app.forms import registration_form,login_form,account_update_form,post_form,request_reset_form,password_reset_form
from post_blog_app.models import User,Post
from post_blog_app.utilities import save_profile_pic,send_reset_mail,welcome_email
from flask_login import login_user,logout_user,login_required,current_user

#The following route is for the home page of the application.
@web_app.route("/")
@web_app.route("/home")
def homepage():
    return render_template("home.html",title="Home")

#The following route is for the registration page .
#The users will be able to register themselves for using the application.
@web_app.route("/register",methods=['POST','GET'])
def registration_page():
    form_instance = registration_form()
    if form_instance.validate_on_submit():
            hash_password = bcrypt_obj.generate_password_hash(form_instance.password.data).decode('utf-8')    
            user = User(username=form_instance.username.data, email=form_instance.email.data, password=hash_password)
            db.session.add(user)
            db.session.commit()
            welcome_email(user)
            flash(f'Account created for {form_instance.username.data} ! You can now log in !!!', "success")
            flash("A Welcome email has been sent ! Do Check your inbox","success")
            return redirect(url_for("login_page"))
    return render_template("register.html",title="Registration",form_blp=form_instance)

#The following route is for the users to login into the application.
#Users can login after they have registered themseleves.
@web_app.route("/login",methods=['POST','GET'])
def login_page():
    login_instance = login_form()
    next_page = request.args.get("next")
    if login_instance.validate_on_submit():
        user = User.query.filter_by(email=login_instance.email.data).first()
        if user and bcrypt_obj.check_password_hash(user.password,login_instance.password.data):
            login_user(user,remember=login_instance.remember.data)
            if next_page:
                return redirect(next_page)
            flash("Logged in Succesfully !","success")
            return redirect(url_for("homepage"))
    
        elif user==None:
            flash("No such account exists ! Click on Register to create an account .","danger")
            return redirect(url_for("login_page"))

        else:
            if next_page:
                flash("Login unsuccessful ! Check the email and password again .","danger")
                return redirect(url_for("login_page",next=next_page))
            else:
                flash("Login unsuccessful ! Check the email and password again .","danger")
                return redirect(url_for("login_page"))

    return render_template("login.html",title="Login",form_blp=login_instance)  

#The following route , makes the user logout of the application.
@web_app.route("/logout")
def logout():
    logout_user()
    flash("Logged Out Successfully .","success")
    return redirect(url_for("homepage"))




#The following route , provides the account information]
#about the user who has currently logged in into the application.
@web_app.route("/account",methods=['POST','GET'])
@login_required
def account():
    account_form = account_update_form()
    if account_form.validate_on_submit():
        if account_form.profile_pic.data:
            picture_file = save_profile_pic(account_form.profile_pic.data)
            current_user.image_file=picture_file

        current_user.username = account_form.username.data
        current_user.email = account_form.email.data
        db.session.commit()
        flash("Your Account Has Been Updated Successfully !","success")
        return redirect(url_for("account"))

    elif request.method == 'GET':
        account_form.username.data = current_user.username
        account_form.email.data = current_user.email

    image = url_for("static",filename="profile_pic/"+current_user.image_file)
    return render_template("account.html",title="Account",image_file=image,form_blp=account_form)





#This route displays the posts from all the users , that exist in this application.
@web_app.route("/posts")
def posts_page():
    pg= request.args.get("page",1,type=int)
    post_list = Post.query.order_by(Post.date_posted.desc()).paginate(page=pg,per_page=4)
    return render_template("posts.html",posts=post_list,title="Posts")

#This route allows the currently logged in user to create a new post.
@web_app.route("/posts/new",methods=['POST','GET'])
@login_required
def new_post():
    form = post_form()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created !","success")
        return redirect(url_for("posts_page"))
    return render_template("create_post.html",title="New Post",form_blp=form,legend="New Post")

#This route allows the user to view a post explicitly.
@web_app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html",p=post)

#This route displays all the posts that a particular user has posted on the application, till date.
@web_app.route("/userposts/<string:username>")
def user_posts(username):
    pg=request.args.get('page',1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    post_list = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=pg,per_page=4)
    return render_template("user_post.html",posts=post_list,user=user)

#This route allows the currently logged in user to update any of its existing posts.
@web_app.route("/post/<int:post_id>/update",methods=['POST','GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = post_form()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been updated !","success")
        return redirect(url_for("post",post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html",title="New Post",form_blp=form,legend="Update Post")

#This route allows the cuurently logged in user to delete any of its existing posts.
@web_app.route("/post/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if (post.author != current_user):
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been deleted successfully !","success")
    return redirect(url_for("posts_page"))

#This route allows a user to view the latest posts on the application.
@web_app.route("/evernote/latestposts")
def latest_posts():
    lp = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=15)
    return render_template("latest_posts.html",posts=lp,title="Latest Posts")




#This route allows a user to generate a password reset request.
@web_app.route("/resetpassword",methods=['POST','GET'])
def reset_request():
    form = request_reset_form()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_mail(user)
        flash("An email has been sent with the instructions to reset the password","info")
        return redirect(url_for("login_page"))
    return render_template("reset_request.html",title="Reset Password",form_blp=form)

#This route allows a user to change the password , after the password request has been intiated.
@web_app.route("/resetpassword/<token>",methods=['POST','GET'])
def reset_token(token):
    user = User.verify_reset_token(token)
    if(user==None):
        flash("The token is invalid or has expired !","danger")
        return redirect(url_for("reset_request"))
    form = password_reset_form()
    if form.validate_on_submit():
        hash_password = bcrypt_obj.generate_password_hash(form.password.data).decode('utf-8')    
        user.password = hash_password
        db.session.commit()
        flash(f'Your Password has been Changed Successfully ! You can now log in !!!', "success")
        return redirect(url_for("login_page"))
        
    return render_template("reset_password.html",title="Reset Password",form_blp=form)
  