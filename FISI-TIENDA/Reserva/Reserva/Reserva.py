from Reservacion import Reservacion
from RabbitMQ import RabbitMQ
from Conexion import Conexion

if __name__ == '__main__':
    conexionBD = Conexion()
    conexionBD.establecerConexion()
    
    rabbitmq = RabbitMQ()

    reservacion = Reservacion(rabbitmq,conexionBD)

    reservacion.iniciarSistema()