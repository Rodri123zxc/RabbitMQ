package administraciondeinventario;

import db.Conexion;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.sql.ResultSet;
import java.sql.SQLException;
import rabbitmq.RabbitMQ;

public class Validacion {
    private RabbitMQ middleware;
    private Conexion bd;
    
    public Validacion(RabbitMQ middleware, Conexion bd) {
        this.middleware = middleware;
        this.bd = bd;
    }
    
    public void iniciarSistema (){
        try {
            middleware.iniciar();
        } catch (Exception ex) {
            System.out.println("Error en iniciar el middleware");
        }
        
        try{
            while(true){
                middleware.recibirYProcesarMensaje();  
                String[][] mensajeRecibido = middleware.getMensaje();
                
                if (mensajeRecibido != null) {
                    validarInventario(mensajeRecibido);
                    middleware.limpiarMensaje();
                }
            }
        } catch (Exception ex){
            System.out.println("Error en iniciar recepcion de mensajes");
        }
    }

    public void validarInventario(String[][] mensajeRecibido) throws Exception{
        boolean validado = false;
        
        List<String> ids = new ArrayList<>();
        List<Integer> cantidades = new ArrayList<>();
        List<Integer> disponibles = new ArrayList<>();
        
        for (String[] item : mensajeRecibido) {
            if (item.length > 0) {
                ids.add(item[0]);
                cantidades.add(Integer.valueOf(item[2]));
            }
        }
        
        String idsString = String.join(",", ids);

        String consultaSelect = "SELECT \"ID_Articulo\", cantidad_existente FROM public.\"Articulo\" WHERE \"ID_Articulo\" IN (" + idsString + ")";

        ResultSet resultadoSelect = bd.ejecutarSelect(consultaSelect);

        try {
            while (resultadoSelect.next()) {
                int idArticulo = resultadoSelect.getInt("ID_Articulo");
                int cantidadExistente = resultadoSelect.getInt("cantidad_existente");
                
                disponibles.add(cantidadExistente);
            }
        } catch (SQLException e) {
            System.out.println("Error al procesar los resultados\nError: " + e.toString());
        }

        for (int i = 0; i < cantidades.size(); i++) {
            int cantidad = cantidades.get(i);
            int disponible = disponibles.get(i);
            if (cantidad <= disponible) {
                validado = true;
            }
            else{
                validado = false;
                break;
            }
        }
       
        if(validado){
            System.out.println("resultado bueno: ");  
            middleware.enviarResultado(true);
            System.out.println("Se envio resultado: ");  
            middleware.enviarMensaje(mensajeRecibido);
        }
        else{
            System.out.println("resultado malo ");  
            middleware.enviarResultado(false);
        }
        
        System.out.println("Se realizo la validacion y el resutlado fue: "+validado);
    }   
}
