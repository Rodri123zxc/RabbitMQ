from Cuenta import Cuenta
from RabbitMQ import RabbitMQ
from Conexion import Conexion

if __name__ == '__main__':
    conexionBD = Conexion()
    conexionBD.establecerConexion()
    
    rabbitmq = RabbitMQ()

    reservacion = Cuenta(rabbitmq,conexionBD)

    reservacion.iniciarSistema()