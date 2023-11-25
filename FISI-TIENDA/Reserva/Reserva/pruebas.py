import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='AdministracionDeInventario_request_queue')
channel.queue_declare(queue='AdministracionDeInventario_response_queue')

def publish_message():
    message = input("Enter '1' to send a message: ")
    if message == '1':
        # Array para enviar
        items_seleccionados = [
            ["1", "Cuaderno","2"],
            ["2", "Lapiz", "2"],
            ["3", "Lapicero", "3"],
        ]
        
        # Convertir el array a formato JSON
        message_body = json.dumps(items_seleccionados)
        
        print(str(message_body))
        
        channel.basic_publish(exchange='',
                              routing_key='AdministracionDeInventario_request_queue', 
                              body=message_body)
        print(" [x] Sent array of strings from Python")

publish_message()