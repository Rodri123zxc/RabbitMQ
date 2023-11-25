from Factura import Factura
from RabbitMQ import RabbitMQ
from Conexion import Conexion

if __name__ == '__main__':
    conexionBD = Conexion()
    conexionBD.establecerConexion()
    
    rabbitmq = RabbitMQ()

    reservacion = Factura(rabbitmq,conexionBD)

    reservacion.iniciarSistema()