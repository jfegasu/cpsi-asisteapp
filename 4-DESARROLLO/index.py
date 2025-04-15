from flask import Flask,Blueprint, render_template,session,request ,redirect,url_for
from flask_session import Session
import pandas as pd
from flask_cors import CORS
from admin.routes import admin 
from entrada.routes import entra 
from park.routes import parq 
from piscina.routes import pisc 
from utils.Utilitarios import CargaMenu,getRol,valideUsuario,crearTabla,Ejecutar
# importar el Blueprint 
# Crear la aplicación Flask **************
app = Flask(__name__) 
app.config['SESSION_TYPE'] = 'filesystem'  # Almacena sesiones en archivos
app.config['SECRET_KEY'] = 'MI_CLAVE_SECRETA'  # Clave para cifrar sesiones
Session(app)

# Registrar el Blueprint en la aplicación 
app.register_blueprint(entra)
app.register_blueprint(admin)
app.register_blueprint(parq)
app.register_blueprint(pisc)
@app.route('/') 
def raiz():   
    return render_template('index0.html')
@app.route('/sinsont') 
def sinsont():   
    return render_template('sinsonte5.htm')
@app.route('/v',methods=['POST']) 
def v(): 
    if request.method == 'POST':
        usua = request.form.get('usua')
        pw = request.form.get('pw')
    esta=valideUsuario(usua,pw)
    print("****",esta)
    if esta:
        rolt=getRol(usua)
        session['rol'] = rolt[5]
        session['username']=rolt[2]
        print("--->",rolt,rolt[2])
        return render_template('index.html')
    else:
        msgito="CLAVE INVALIDA"
        regreso="/logout"
        print("Fallo" )
        return render_template('alertas.html',msgito=msgito)

@app.route('/index',methods=['POST']) 
def index(): 
    
    return render_template('index.html')
@app.route('/menu') 
def menu(): 
    # menu = []
    # a = pd.read_csv('menu.csv')

    # # Convert all rows to a list of lists (faster approach)
    # menu = a.values.tolist()
    rol=session.get('rol')
    if rol != None:
        menu=CargaMenu(rol)     
        return render_template('menu.html',menus=menu,titu='MENU PRINCIPAL')
    return redirect("/")
@app.route('/admin')
def madm():
    menu=CargaMenu('admin')
    # aa=crearTabla('usuario',{"login":"prueba","roll":"root"})
    aux=1
    sql=f"select * from apartamento where idapartamento=%d" % aux
    print(sql)
    aa=Ejecutar(sql)
    # return aa
    return render_template('admin_tabla.html',aa=sql,vcol=vcol,i=len(vcol))

@app.route('/park')
def park():
    menu=CargaMenu('park')
    return render_template('menu.html',menus=menu,titu='MENU PARQUEADERO')
@app.route('/pisci')
def pisc():
    menu=CargaMenu('pisc')
    return render_template('menu.html',menus=menu,titu='MENU PISCINA')
@app.route('/banner') 
def banner(): 
    usuario=session.get('username')
    return render_template('banner.html',usuario=usuario)
@app.route('/centro') 
def centro(): 
    return render_template('centro.html')
@app.route('/footer') 
def footer(): 
    return render_template('footer.html')
@app.route('/logout') 
def logout(): 
    session.clear()  # This will remove all session data
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
