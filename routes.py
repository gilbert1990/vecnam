from jinja2 import Environment, FileSystemLoader
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import user
app=Flask(__name__)
app.secret_key = 'b\x9em\xedu{\x86$:\\D\x7f\xc9AWw\xb7\xe3\x06\xa1\xed\x9c\xf1at\x16\xa0p\xe9\xf5V\x04/'
login_manager = LoginManager()
login_manager.init_app(app)
env = Environment(loader=FileSystemLoader('templates'))

# Modelo de usuario
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Función para cargar un usuario desde el ID 
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    template = env.get_template('index.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html')

#Vista de login
@app.route('/login/<int:rol>')
def login_view(rol):
    template = env.get_template('login.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html',rol=rol)

#Autenticar
@app.route('/auth/<int:rol>',methods=['POST'])
def authentication(rol):
    documento_usuario = request.form['document']
    password = request.form['password']
    auth = user.user_auth(documento_usuario, password, rol)
    if auth['code']==200:
        user_auth=User(documento_usuario)
        login_user(user_auth)
        if(rol==0 or rol==1):
            return redirect(url_for('home'))
        else:
            return redirect(url_for('home_pacient'))
    else:
        template = env.get_template('login.html')
        return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html",rol=rol,alert=auth)
    
#Vista de registro del usuario
@app.route('/register/<int:rol>')
def register_view(rol):
    template = env.get_template('register.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html',rol=rol)

#Vista de registro del usuario
@app.route('/register_user/<int:rol>',methods=['POST'])
def register(rol):
    user_create=user.user_create(request.form['name'], request.form['document'], request.form['date_document'], request.form['email'],rol,request.form['password'],request.form['birthdate'])
    if user_create['code']==200:
        template = env.get_template('login.html')
        return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html",rol=rol,alert=user_create)
    else:
        template = env.get_template('register.html')
        return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html",rol=rol,alert=user_create)

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/home_pacient')
@login_required
def home_pacient():
    user_view=user.getUser(document_user=current_user.id)
    user_type = 'Administrador' if user_view['user'][5] == 1 else 'Paciente' if user_view['user'][5] == 2 else 'Doctor'
    template = env.get_template('info.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html",user=user_view['user'],medicalHistory=user_view['medicalHistory'],familyHistory=user_view['familyHistory'],user_type=user_type)

@app.route('/register_medical/<string:address>',methods=['POST'])
@login_required
def register_medical(address):
    edit=user.registerMedical(address, request.form['alcohol'],request.form['smoke'],request.form['physical_activity'],request.form['contraceptives'],request.form['fracture'],request.form['surgery'])
    return infoAlert(edit)

@app.route('/register_family/<string:address>',methods=['POST'])
@login_required
def register_family(address):
    edit=user.registerFamily(address, request.form['diabetes'],request.form['hypertension'],request.form['heart'],request.form['respiratory'],request.form['alzheimer'],request.form['cardiovascular'],request.form['cancer'])
    return infoAlert(edit)

def infoAlert(alert_function):
    user_view=user.getUser(document_user=current_user.id)
    user_type = 'Administrador' if user_view['user'][5] == 1 else 'Paciente' if user_view['user'][5] == 2 else 'Doctor'
    template = env.get_template('info.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html",user=user_view['user'],medicalHistory=user_view['medicalHistory'],familyHistory=user_view['familyHistory'],user_type=user_type,alert=alert_function)
@app.route('/home')
@login_required
def home():
    template = env.get_template('home.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html")

@app.route('/new_user')
def new_user():
    template = env.get_template('new_user.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html",users=user.lista_usuarios())
@app.route('/permission')
def permission():
    template = env.get_template('permission.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html",users=user.lista_usuarios())
@app.route('/info')
@login_required
def info():
    user_view=user.getUser(document_user=current_user.id)
    user_type = 'Administrador' if user_view['user'][5] == 1 else 'Paciente' if user_view['user'][5] == 2 else 'Doctor'
    template = env.get_template('info.html')
    return template.render(componente='components/navbar.html',scripts='components/scripts.html',alerts="components/alert.html",user=user_view['user'],medicalHistory=user_view['medicalHistory'],familyHistory=user_view['familyHistory'],user_type=user_type)
# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    logout_user()
    return 'Sesión cerrada'


if __name__ == '__main__':
    app.run(debug=True)