import os
import RabbitMQ
import threading
from flask import Flask, request, jsonify, send_file
from psycopg2 import connect, extras
from dotenv import load_dotenv
from RabbitMQ import recibirYProcesarMensajeADI, recibirYProcesarMensajeCxC, publish_message


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
  
    
    thread_cxc = threading.Thread(target=RabbitMQ.recibirYProcesarMensajeCxC)
    thread_cxc.start()
  
    thread_cxc.join()
    
    
    validarInventario = RabbitMQ.mensajeRecibido_ADI
    print("validarInventario: " + str(validarInventario))
    
    
    if validarInventario:
        thread_cxc.join()
        resultado_final = RabbitMQ.mensajeRecibido_CxC
        print("resultado_final: " + str(resultado_final))
        RabbitMQ.mensajeRecibido_ADI = None
        RabbitMQ.mensajeRecibido_CxC = None
        
        validarInventario = None
        return jsonify({'success': True, 'message': 'Pago exitoso', 'resultado_final': resultado_final})
    else:
        validarInventario = None
        RabbitMQ.mensajeRecibido_ADI = None
        RabbitMQ.mensajeRecibido_CxC = None
        return jsonify({'success': False, 'message': 'Pago fallido'})
    
    
@app.get('/')
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True)