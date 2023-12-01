package administraciondeinventario;

import db.Conexion;
import rabbitmq.RabbitMQ;

public class AdministracionDeInventario {
    public static void main(String[] args) {
        System.out.println("HOLA ANDERSON");
        
        Conexion conexionBD = new Conexion();
        conexionBD.establecerConexion();
        
        RabbitMQ rabbitmq = new RabbitMQ();
        
        Validacion validacion = new Validacion(rabbitmq,conexionBD);
        
        validacion.iniciarSistema();
    }       
}
