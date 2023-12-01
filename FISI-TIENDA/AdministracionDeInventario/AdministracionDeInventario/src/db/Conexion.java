package db;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class Conexion {
    Connection conectar = null;

    String user = "";
    String password = "";
    String bdname = "";
    String ip = "";
    String port = "";

    String con = "";
    
    private void cargarDatosBD(){
        Properties prop = new Properties();
        InputStream input = null;

        try {
            input = Conexion.class.getClassLoader().getResourceAsStream("resources/config.properties");
            prop.load(input);

            user = prop.getProperty("db.username");
            password = prop.getProperty("db.password");
            bdname = prop.getProperty("db.bdname");
            ip = prop.getProperty("db.ip");
            port = prop.getProperty("db.port");
            
            con = "jdbc:postgresql://" + ip + ":" + port + "/" + bdname;

        } catch (IOException ex) {
            System.out.println("Error en carga de credenciales: "+ex.toString());
        } finally {
            if (input != null) {
                try {
                    input.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }
    
    
    public Connection establecerConexion() {
        cargarDatosBD();
        try {
            Class.forName("org.postgresql.Driver");
            conectar = DriverManager.getConnection(con, user, password);
            System.out.println( "Conexion a la base de datos correcta");
        } catch (Exception e) {
            System.out.println( "Error al conectarse a la base de datos\nError: " + e.toString());
        }
        return conectar;
    }

    public ResultSet ejecutarSelect(String consulta) {
        ResultSet resultado = null;
        try {
            PreparedStatement statement = conectar.prepareStatement(consulta);
            resultado = statement.executeQuery();
        } catch (SQLException e) {
            System.out.println( "Error al ejecutar la consulta SELECT\nError: " + e.toString());
        }
        return resultado;
    }

    public int ejecutarUpdate(String consulta) {
        int filasAfectadas = 0;
        try {
            PreparedStatement statement = conectar.prepareStatement(consulta);
            filasAfectadas = statement.executeUpdate();
        } catch (SQLException e) {
            System.out.println("Error al ejecutar la consulta UPDATE/DELETE/INSERT\nError: " + e.toString());
        }
        return filasAfectadas;
    }
}
