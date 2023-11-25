import pika
import json

class RabbitMQ:
    def __init__(self):
        self.PUBLISH_EXCHANGE_NAME = "CuentaXCobrar_exchange"
        self.PUBLISH_QUEUE_NAME = "CuentaXCobrar_exchange"
        self.CONSUME_EXCHANGE_NAME = "Factura_exchange"
        self.channel = None
        self.queue_name = None
        self.mensajeRecibido = None

    def iniciar(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()

        self.channel.exchange_declare(exchange=self.CONSUME_EXCHANGE_NAME, exchange_type='fanout')

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue

        self.channel.queue_bind(exchange=self.CONSUME_EXCHANGE_NAME, queue=self.queue_name)
        print("Inicio el rabbit")
        
    def recibirYProcesarMensaje(self):
        def callback(ch, method, properties, body):
            self.mensajeRecibido = self.parsear_mensaje(body)
            self.channel.stop_consuming()
        
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
        
        
    def parsear_mensaje(self, mensaje):
        try:
            mensaje_recibido = json.loads(mensaje)
        except json.JSONDecodeError as e:
            mensaje_recibido = None
        return mensaje_recibido
    
    def desparsear_mensaje(self, mensaje):
        return json.dumps(mensaje)
    
    def enviarMensaje(self, mensaje):
        mensaje_r = self.desparsear_mensaje(mensaje)
        
        print("mensaje_r: "+str(mensaje_r))
        self.channel.basic_publish(exchange=self.PUBLISH_EXCHANGE_NAME, routing_key=self.PUBLISH_QUEUE_NAME, body=mensaje_r)

    def getMensaje(self):
        return self.mensajeRecibido

    def limpiarMensaje(self):
        self.mensajeRecibido = None

   