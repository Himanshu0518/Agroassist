from flask import Blueprint, render_template
#import json
blog_bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static', url_prefix='/blog')


#with open('config.json','r') as c:
  #  params = json.load(c)["params"]

 
@blog_bp.route('/')
def home():
    return render_template('blog_index.html')  # This template is in blogs/templates/

@blog_bp.route('/about')
def about():
    return render_template('about.html')  # This is blog's about page

@blog_bp.route('/post')
def post():
    return render_template('post.html')  
