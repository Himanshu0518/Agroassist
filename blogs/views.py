from flask import Blueprint, render_template , session , redirect , url_for,request,flash,current_app
import sqlite3
from werkzeug.utils import secure_filename
import os
from math import ceil
from datetime import datetime 
#import json

blog_bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static', url_prefix='/blog')
page = 0 

UPLOAD_FOLDER = "blogs/static/assets/img/"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

# blog_bp.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[-1].lower() in ALLOWED_EXTENSIONS

def get_db_connection():
    conn = sqlite3.connect("instance/users.db")
    conn.row_factory = sqlite3.Row
    return conn

POSTS_PER_PAGE = 3  # Set how many posts to show per page

@blog_bp.route('/')
def home():
    conn = get_db_connection()

    # Get the page number from the request, default to 1 if not provided
    page = request.args.get('page', 1, type=int)

    # Calculate offset for pagination
    offset = (page - 1) * POSTS_PER_PAGE

    # Get total number of posts for pagination calculation
    total_posts = conn.execute("SELECT COUNT(*) FROM blog").fetchone()[0]
    total_pages = ceil(total_posts / POSTS_PER_PAGE)  # Calculate total pages

    # Fetch posts for the current page with LIMIT and OFFSET
    posts = conn.execute("""
        SELECT blog.*, user.username AS username
        FROM blog 
        LEFT JOIN user ON blog.user_id = user.id 
        ORDER BY blog.created_at DESC
        LIMIT ? OFFSET ?;
    """, (POSTS_PER_PAGE, offset)).fetchall()

    conn.close()

    return render_template('blog_index.html', posts=posts, page=page, total_pages=total_pages)

@blog_bp.route('/myBlog')
def myBlog():
    if "user_name" not in session:
        flash("Login Required!")
        return redirect(url_for('login', next=request.url))
    conn = get_db_connection()
    posts = conn.execute("SELECT blog.* FROM blog WHERE user_id = ?",(session["user_id"],)).fetchall()
    conn.close()
    
    return render_template('MyBlogs.html',myPosts=posts)  # This is blog's about page

@blog_bp.route('/post/<int:postId>')  # Accept postId as a URL parameter
def post(postId):
    conn = get_db_connection()
    
    post = conn.execute("SELECT blog.* FROM blog WHERE id = ?", (postId,)).fetchone()
    
    if not post:
        conn.close()
        return "Post not found", 404  # Handle missing posts properly

    # Fetch username before closing the connection
    user_id = post["user_id"]  # Use dictionary-style access
    username = conn.execute("SELECT username FROM user WHERE id = ?", (user_id,)).fetchone()
    
    conn.close()

    return render_template('post.html', post=post, posted_by=username["username"] if username else "Unknown User")

@blog_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    if "user_id" not in session:
        flash("Login required!")
        return redirect(url_for('login', next=request.url))
    
    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        content = request.form["content"]
        image_url = None
        user_id = session['user_id']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO blog (title, subtitle, content, user_id, created_at) VALUES (?, ?, ?, ?, ?)",
            (title, subtitle, content, user_id, datetime.now().strftime("%B %d, %Y"))
        )
        conn.commit()
        post_id = cur.lastrowid  # Get the last inserted post ID

        # Handle image upload
        if "image" in request.files:
            file = request.files["image"]
            if file.filename == '':
                print("No selected file!")
            if file and allowed_file(file.filename):
                filename = f"bg_{post_id}.jpg"
               
                user_folder = os.path.join(current_app.root_path, UPLOAD_FOLDER, f"user_{user_id}")
                os.makedirs(user_folder, exist_ok=True)
                filepath = os.path.join(user_folder, filename)
                file.save(filepath)
                image_url = url_for('blog.static', filename=f'assets/img/user_{user_id}/{filename}')

                # Update blog entry with image path
                cur.execute("UPDATE blog SET image = ? WHERE id = ?", (image_url, post_id))
                conn.commit() 

        conn.close()
        flash("Post created successfully!")
        return redirect(url_for('blog.home'))
    
    return render_template('create_post.html')

@blog_bp.route('/edit/<int:postId>', methods=['GET', 'POST'])
def edit_post(postId):
    if "user_id" not in session:
        flash("Login required!")
        return redirect(url_for('login', next=request.url))

    conn = get_db_connection()
    post = conn.execute("SELECT * FROM blog WHERE id = ?", (postId,)).fetchone()
    
    if not post:
        conn.close()
        return "Post not found", 404

    if post["user_id"] != session["user_id"]:
        conn.close()
        flash("You are not allowed to edit this post!")
        return redirect(url_for('blog.home'))

    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        content = request.form["content"]
        
        post_id = postId
        user_id = session['user_id']
        cur = conn.cursor()
        
        if "image" in request.files:
            file = request.files["image"]
            if file.filename == '':
                print("No selected file!")
            if file and allowed_file(file.filename):
                filename = f"bg_{post_id}.jpg"
               
                user_folder = os.path.join(current_app.root_path, UPLOAD_FOLDER, f"user_{user_id}")
                os.makedirs(user_folder, exist_ok=True)
                filepath = os.path.join(user_folder, filename)
                file.save(filepath)
                image_url = url_for('blog.static', filename=f'assets/img/user_{user_id}/{filename}')

                # Update blog entry with image path
                cur.execute("UPDATE blog SET image = ? WHERE id = ?", (image_url, post_id))
                conn.commit() 

        conn.execute("UPDATE blog SET title = ?, subtitle = ?, content = ? WHERE id = ?", 
                     (title, subtitle, content, postId))
        conn.commit()
        conn.close()

        flash("Post updated successfully!")
        return redirect(url_for('blog.post', postId=postId))

    conn.close()
    return render_template('edit_post.html', post=post)

@blog_bp.route('/del_post/<int:postId>', methods=["POST"])
def del_post(postId):
    if "user_id" not in session:
        flash("Login required!")
        return redirect(url_for('login', next=request.url))
    
    conn = get_db_connection()
    post = conn.execute("SELECT * FROM blog WHERE id = ?", (postId,)).fetchone()

    if not post:
        conn.close()
        return "Post not found", 404

    if post["user_id"] != session["user_id"]:
        conn.close()
        flash("You are not allowed to delete this post!")
        return redirect(url_for('blog.home'))

    # Delete image file if exists
    if post["image"]:
        image_path = os.path.join(current_app.root_path, post["image"])
        if os.path.exists(image_path):
            os.remove(image_path)

    conn.execute("DELETE FROM blog WHERE id = ?", (postId,))
    conn.commit()
    conn.close()

    flash("Post deleted successfully!")
    return redirect(url_for('blog.home'))