import pika
import json

class RabbitMQ:
    def __init__(self):
        self.PUBLISH_EXCHANGE_NAME = "Reserva_exchange"
        self.PUBLISH_QUEUE_NAME = "Reserva_queue_exchange"
        
        self.CONSUME_EXCHANGE_NAME = "AdministracionDeInventario_exchange"
        
        self.channel = None
        self.queue_name = None
        self.mensajeRecibido = []

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
            self.mensajeRecibido = self.desempaquetarMensaje(body)
            self.channel.stop_consuming()
        
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        self.channel.start_consuming()
        
    def desempaquetarMensaje(self, mensaje):
        try:
            mensaje_recibido = json.loads(mensaje)
        except json.JSONDecodeError as e:
            mensaje_recibido = []
        return mensaje_recibido
    
    def empaquetarMensaje(self, mensaje):
        return json.dumps(mensaje)
    
    def enviarMensaje(self, mensaje):
        mensaje_r = self.empaquetarMensaje(mensaje)
        self.channel.basic_publish(exchange=self.PUBLISH_EXCHANGE_NAME, routing_key=self.PUBLISH_QUEUE_NAME, body=mensaje_r)

    def getMensaje(self):
        return self.mensajeRecibido

    def limpiarMensaje(self):
        self.mensajeRecibido = []

   