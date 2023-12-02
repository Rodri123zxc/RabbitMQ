import os
import RabbitMQ
import threading
import re
from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from dotenv import load_dotenv
from RabbitMQ import recibirYProcesarMensajeADI, recibirYProcesarMensajeCxC, publish_message


cliente = None

app = Flask(__name__)
load_dotenv()

def get_connection():
    return connect(
        user = os.environ["USER"],
        password = os.environ["PASSWORD"],
        dbname = os.environ["DATABASE"],
        host = os.environ["HOST"],
        port = os.environ["PORT"]
    )


data_usuario = None


@app.get('/api/verificar-sesion')
def verificar_sesion():
    global data_usuario
    return jsonify(data_usuario)
    
@app.post('/api/cerrar-sesion')
def cerrar_sesion():
    global data_usuario
    data_usuario = None

@app.get('/api/articulos')
def get_productos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM public."Articulo" ORDER BY "ID_Articulo" ASC ')
    articulos = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(articulos)


@app.post('/api/pagar')
def pagar():
    data = request.json
    print(data)
    
    RabbitMQ.publish_message(data)
    
    validarInventario = None
    resultado_final = None
    
    thread_adi = threading.Thread(target=RabbitMQ.recibirYProcesarMensajeADI)
    
    thread_adi.start()
    thread_adi.join()
    
    validarInventario = RabbitMQ.mensajeADI
    print("validarInventario: " + str(validarInventario)) 
    
    if validarInventario:
        print("VERDADEROOO")
        thread_cxc = threading.Thread(target=RabbitMQ.recibirYProcesarMensajeCxC)
        thread_cxc.start()
        thread_cxc.join()
        
        print("VERDADEROOO Y PARO EL CONSUMO DE CXC")
        resultado_final = RabbitMQ.mensajeCxC
        print("resultado_final: " + str(resultado_final))
        
        RabbitMQ.mensajeADI = None
        RabbitMQ.mensajeCxC = None
        
        validarInventario = None
        if resultado_final:
            return jsonify({'success': True, 'message': 'Pago exitoso', 'resultado_final': resultado_final})
        else:
            return jsonify({'success': False, 'message': 'Pago fallido'})
    else:
        print("FALSO")
        validarInventario = None
        RabbitMQ.mensajeADI = None
        RabbitMQ.mensajeCxC = None
        return jsonify({'success': False, 'message': 'Algunos items no estan disponibles'})


def validar_correo(correo):
    expresion_regular = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(expresion_regular, correo) is not None

def validar_ruc(ruc):
    return re.match(r"^0?\d{1,11}$", str(ruc)) is not None

def validar_telefono(telefono):
    return re.match(r"^[0-9]{9}$", str(telefono)) is not None
    
@app.post('/api/registro')
def registro_cliente():
    data = request.json
    nombres = data['nombres']
    apellidos = data['apellidos']
    correo = data['correo']
    contrasena = data['contrasena']
    direccion = data['direccion']
    ciudad = data['ciudad']
    ruc = data['ruc']
    telefono = data['telefono']
    
    print("Nombres: "+nombres)
    print("Apellidos: "+apellidos)
    print("Correo: "+correo)
    print("Contrasena: "+contrasena)
    print("Direccion: "+direccion)
    print("Ciudad: "+ciudad)
    print("Ruc: "+ruc)
    print("Telefono: "+telefono)
    
    if (not nombres or not apellidos or not correo or not contrasena or not direccion or not ciudad or not ruc or not telefono) :
        return jsonify({'success': False, 'message': 'Por favor, completa todos los campos.'})
 
    if not validar_correo(correo):
        return jsonify({'success': False, 'message': 'Correo no valido'})
    
    if not validar_ruc(ruc):
        return jsonify({'success': False, 'message': 'Ruc no valido'})
    
    if not validar_telefono(telefono):
        return jsonify({'success': False, 'message': 'Telefono no valido'})
    
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    query = 'SELECT * FROM public."Cliente" WHERE ' + \
    '"Nombres" = \'' + nombres + '\' AND ' + \
    '"Apellidos" = \'' + apellidos + '\' AND ' + \
    '"Calle" = \'' + direccion + '\' AND ' + \
    '"Ciudad" = \'' + ciudad + '\' AND ' + \
    '"RUC" = \'' + ruc + '\' AND ' + \
    '"Celular" = \'' + telefono + '\' AND ' + \
    '"Correo" = \'' + correo + '\' AND ' + \
    '"Contraseña" = \'' + contrasena + '\';'
    
    cur.execute(query)
    
    usuario_existente = cur.fetchone()

    cur.close()
    conn.close()
    
    if usuario_existente:
        return jsonify({'success': False, 'message': 'Usuario ya registrado.'})

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('INSERT INTO "Cliente" '+
                '("Nombres", "Apellidos", "Calle", "Ciudad", "RUC", "Celular", "Correo", "Contraseña")'+
                ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            (nombres, apellidos, direccion, ciudad, ruc, telefono, correo, contrasena))
    
    conn.commit()
    cur.close()
    conn.close()
    
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    
    print(query)
    
    cur.execute(query)
     
    data_usuario = cur.fetchone()
    
    print()
    
    cur.close()
    conn.close()
    
    if data_usuario:
       return jsonify({'success': True, 'message': 'Usuario registrado exitosamente.', 'data_usuario': data_usuario})

    return jsonify({'success': False, 'message': 'Error en las entradas'})


@app.post('/api/login')
def login_cliente():
    global data_usuario
    data = request.json
    correo = data['correo']
    contrasena = data['contrasena']
    
    if (not correo or not contrasena) :
        return jsonify({'success': False, 'message': 'Por favor, completa todos los campos.'})
 
    if not validar_correo(correo):
        return jsonify({'success': False, 'message': 'Correo no valido'})

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)

    cur.execute('SELECT * FROM "Cliente" WHERE "Correo" = \''+correo+'\' AND "Contraseña" = \''+contrasena+'\';')
    
    data_usuario = cur.fetchone()

    cur.close()
    conn.close()

    if data_usuario:
       return jsonify({'success': True, 'message': 'Inicio de sesión exitoso.', 'data_usuario': data_usuario})

    return jsonify({'success': False, 'message': 'Credenciales incorrectas.'})
    
@app.get('/')
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True)