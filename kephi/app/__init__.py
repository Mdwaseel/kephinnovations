from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

#==========================================================
#          Configurations
#==========================================================

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" # database link
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SECRET_KEY'] = "any key"

db = SQLAlchemy(app=app)

from .models import *

#with app.app_context():
#    db.create_all()


main_ = {
    'username':'kephi',
    'password':'kipl@1'
}


#==========================================================

admin = Admin(app=app)

class SecureView(ModelView):
    def is_accessible(self):
        if 'admin' in session:
            return super().is_accessible()
        abort

admin.add_view(SecureView(Contacts, db.session))


#==========================================================
#          App Routes
#==========================================================
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == "POST":
        d = request.form
        print(d)
        name = d.get('name')
        email = d.get('email')
        subject = d.get('subject')
        desc = d.get('description')
        print(desc)

        cont = Contacts(
            name=name,
            email=email,
            subject=subject,
            description = desc
        )

        db.session.add(cont)
        db.session.commit()
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/achievements')
def achievements():
    return render_template('achievements.html')

@app.route('/achievements/<string:file>')
def achievements_posts(file):
    if file:
        return render_template(f'posts/{file}.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/adm/login', methods=['GET',"POST"])
def admin_login():
    if request.method=="POST":
        un = request.form.get('username')
        pswd = request.form.get('pswd')
        if main_['username']==un:
            if main_['password']==pswd:
                session['admin']=True
                return redirect(url_for('panel'))
    return render_template('admin.html')

@app.route('/admin/panel')
def panel():
    if 'admin' in session:
        return render_template('panel.html')
    return redirect(url_for('home'))

@app.route('/admin/logout')
def logout():
    if 'admin' in session:
        session.pop('admin',None)
    return redirect(url_for('home'))


