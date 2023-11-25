import pika
import json

REQUEST_QUEUE_NAME = "AdministracionDeInventario_request_queue"
RESPONSE_QUEUE_NAME = "ProcesamientoDeOrdenes_response_queue"
CONSUME_EXCHANGE_NAME = "CuentaXCobrar_exchange"

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue = REQUEST_QUEUE_NAME)
channel.queue_declare(queue = RESPONSE_QUEUE_NAME)
channel.exchange_declare(exchange=CONSUME_EXCHANGE_NAME, exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue
channel.queue_bind(exchange=CONSUME_EXCHANGE_NAME, queue=queue_name)
       
mensajeRecibido_ADI = None
mensajeRecibido_CxC = None
consume_ADI = True
consume_CxC = True

def callback1(ch, method, properties, body):
    global mensajeRecibido_ADI, consume_ADI
    mensajeRecibido_ADI = parsear_mensaje(body)
    print("mensajeRecibido_ADI: " + str(mensajeRecibido_ADI))
    if mensajeRecibido_ADI is not None:
        consume_ADI = False

def callback2(ch, method, properties, body):
    global mensajeRecibido_CxC, consume_CxC
    mensajeRecibido_CxC = parsear_mensaje(body)
    print("mensajeRecibido_CxC: " + str(mensajeRecibido_CxC))
    if mensajeRecibido_CxC is not None:
        consume_CxC = False

def recibirYProcesarMensajeADI():
    global mensajeRecibido_ADI
    channel.basic_consume(queue=RESPONSE_QUEUE_NAME, on_message_callback=callback1, auto_ack=True)
    print("Esperando mensajes ADI...")
    while True:
        channel.connection.process_data_events()
        if not consume_ADI:
            break
    print("Deteniendo consumo ADI.")

def recibirYProcesarMensajeCxC():
    global mensajeRecibido_CxC
    channel.basic_consume(queue=queue_name, on_message_callback=callback2, auto_ack=True)
    print("Esperando mensajes CxC...")
    while True:
        channel.connection.process_data_events()
        if not consume_CxC:
            break
    print("Deteniendo consumo CxC.")

def parsear_mensaje(mensaje):
        try:
            mensajeRecibido = json.loads(mensaje)
        except json.JSONDecodeError as e:
            mensajeRecibido = None
        return mensajeRecibido
    
def desparsear_mensaje(mensaje):
    return json.dumps(mensaje)

def publish_message(data):
    message_body = desparsear_mensaje(data)
    
    channel.basic_publish(exchange='', routing_key=REQUEST_QUEUE_NAME, body=message_body)
    print(" Sen envio al ADI")