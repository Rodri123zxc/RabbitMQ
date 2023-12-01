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
        return jsonify({'success': False, 'message': 'Pago fallido'})
    
    
@app.get('/')
def home():
    return send_file('static/index.html')

if __name__ == '__main__':
    app.run(debug=True)