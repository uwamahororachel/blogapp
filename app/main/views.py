
# from flask import render_template,request,redirect,url_for
from . import main
import requests
from ..requests import getQuotes

from flask_login import login_required,current_user,login_user,logout_user
from flask import render_template,request,redirect,url_for,abort
from ..models import Blog, User,Comment,Quotes
from .forms import BlogForm,CommentForm,CommentForms,UpdateProfile ,BlogUploadForm
from .. import db,photos
from flask_login import login_required, current_user

# import markdown2 
# @main.route('/review/<int:id>')
# def single_review(id):
#     review=Review.query.get(id)
#     if review is None:
#         abort(404)
#     format_review = markdown2.markdown(review.movie_review,extras=["code-friendly", "fenced-code-blocks"])
#     return render_template('review.html',review = review,format_review=format_review)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/profile/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    userid=user.id
    blog=Blog.query.filter_by(user_id=userid).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,blog=blog)

    # ..........................................login ..................................

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    
    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/')
def index():

     blogs =Blog.get_blogs()
  
     quotes = getQuotes()
  
    
     title='Welcome to blog'
     return render_template('index.html',blogs=blogs,quotes = quotes)


# ...................................function for blogs...................................

@main.route('/blog/new/', methods = ['GET','POST'])
@login_required
def new_blog():
    form = BlogForm()
    # my_upvotes = Upvote.query.filter_by(blog_id = Blog.id)
    if form.validate_on_submit():
        blog = form.blog.data
        owner_id = current_user
        category = form.category.data
        print(current_user._get_current_object().id)

        new_blog=Blog(user_id =current_user._get_current_object().id, blog=blog,category=category)
        db.session.add(new_blog)
        db.session.commit()
        
        
        return redirect(url_for('main.index'))
    return render_template('blog.html',form=form)
# .................................comment function...............................................

@main.route('/comment/new/<int:blog_id>/', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForms()
    blog=Blog.query.get(blog_id)
    if form.validate_on_submit():
        comment = form.comment.data

        new_comment =Comment(comment=comment, user_id = current_user._get_current_object().id, blog_id =blog_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', blog_id= blog_id))

    all_comments =Comment.query.filter_by(blog_id = blog_id).all()
    return render_template('comment.html', form = form, comment = all_comments, blog = blog )

    
# #............................... detete function to delete the posted blog....................................
@main.route('/details/<int:blog_id>/delete',methods=['POST'])
@login_required
def delete(blog_id):
    current_blog = Blog.query.filter_by(id = blog_id).first()
    if current_blog.user != current_user:
        abort(403)
    db.session.delete(current_blog)
    db.session.commit()

    return redirect(url_for('.index'))
#     # ..................................detete comment.............................
@main.route('/details/<int:comment_id>/delete_comment',methods=['GET','POST'])
@login_required
def delete_comment(comment_id):
    current_comment = Comment.query.filter_by(id = comment_id).first()
    if current_comment.user != current_user:
        abort(403)
    db.session.delete(current_comment)
    db.session.commit()

    return redirect(url_for('main.index'))

# # ............ function to view all details but by writer...........................

@main.route('/details/<int:blog_id>/comment',methods=['POST','GET'])
@login_required
def comment(blog_id):
    current_blog=Blog.query.filter_by(id = blog_id).first()
    if request.method == "POST":
        comment = request.form.get("comment")
        new_comment = Comment(comment = comment,user = current_user,blog = current_blog)
        db.session.add(new_comment)
        db.session.commit()
    blog= Blog.query.get_or_404(blog_id)
    comments = Comment.get_comments(blog_id)

    title = 'welcome to details'
    return render_template('details.html',title = title,blog = blog,comments=comments)

# # .............................update profile.............................
@main.route('/details/<int:blog_id>/update',methods=['POST','GET'])
@login_required
def update(blog_id):
    current_blog = Blog.query.filter_by(id = blog_id).first()
    if current_blog.user != current_user:
        abort(403)
    form = BlogUploadForm()
    if form.validate_on_submit():
        current_blog.blog= form.blog.data
        current_blog.category = form.category.data
        db.session.commit()
        return redirect(url_for('.index'))
    elif request.method == 'GET':
        form.category.data = current_blog.category
        form.blog.data = current_blog.blog
    return render_template('blog.html',form = form)