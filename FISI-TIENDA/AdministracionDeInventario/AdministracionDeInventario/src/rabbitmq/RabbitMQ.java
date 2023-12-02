/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package rabbitmq;

import com.rabbitmq.client.*;
import com.google.gson.Gson;
import com.google.gson.JsonSyntaxException;

public class RabbitMQ {
    private final static String REQUEST_QUEUE_NAME = "AdministracionDeInventario_request_queue";
    private final static String RESPONSE_QUEUE_NAME = "ProcesamientoDeOrdenes_response_queue";
    
    private final static String PUBLISH_EXCHANGE_NAME = "AdministracionDeInventario_exchange"; 
    private final static String PUBLISH_QUEUE_NAME = "AdministracionDeInventario_publish_queue"; 
    
    private String[][] mensajeRecibido;
    private Channel channel;
    

    public void iniciar() throws Exception {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");

        Connection connection = factory.newConnection();
        channel = connection.createChannel();

        channel.queueDeclare(REQUEST_QUEUE_NAME, false, false, false, null);
        channel.queueDeclare(RESPONSE_QUEUE_NAME, false, false, false, null);
        
        channel.exchangeDeclare(PUBLISH_EXCHANGE_NAME, BuiltinExchangeType.FANOUT); // Intercambio para publicar
    }
    
    public void recibirYProcesarMensaje() throws Exception {
        DeliverCallback deliverCallback = (consumerTag, delivery) -> {
            byte[] body = delivery.getBody();
            String mensaje = new String(body, "UTF-8");
            
            System.out.println("Mensaje resigbido: "+mensaje);
            
            mensajeRecibido = desempaquetarMensaje(mensaje);
            
            System.out.println("Mensaje parseado resigbido: "+mensajeRecibido.toString());
        };
        channel.basicConsume(REQUEST_QUEUE_NAME, true, deliverCallback, consumerTag -> {});
    }

    private String[][] desempaquetarMensaje(String mensaje) {
        String[][] mensajeRecibido;
        try {
            Gson gson = new Gson();
            mensajeRecibido = gson.fromJson(mensaje, String[][].class);
        } catch (JsonSyntaxException e) {
            mensajeRecibido = new String[0][0];
        }
        return mensajeRecibido;
    }
    
    private String empaquetarMensaje(String[][] mensaje) {
        Gson gson = new Gson();
        return gson.toJson(mensaje);
    }
    
    private String empaquetarMensaje(boolean mensaje) {
        Gson gson = new Gson();
        return gson.toJson(mensaje);
    }
    
    public void enviarResultado(boolean resultado) throws Exception {
        
        String respuesta = empaquetarMensaje(resultado);
        
        System.out.println("MENSAJE PARA ENVIAR A RESERVA: " + respuesta);
        
        channel.basicPublish("", RESPONSE_QUEUE_NAME, null, respuesta.getBytes());
        
        System.out.println("MENSAJE ENVIADO" );
    }
    
    public void enviarMensaje(String[][] mensaje) throws Exception {
        
        String mensajeADI = RabbitMQ.this.empaquetarMensaje(mensaje);
        
        System.out.println("MENSAJE PARA ENVIAR A RESERVA: " + mensajeADI);
        
        channel.basicPublish(PUBLISH_EXCHANGE_NAME, PUBLISH_QUEUE_NAME, null, mensajeADI.getBytes());
        
        System.out.println("MENSAJE ENVIADO" );
    }
    
    public String[][] getMensaje() {
        return mensajeRecibido;
    }
    
    public void limpiarMensaje() {
        mensajeRecibido = null;
    }
}
