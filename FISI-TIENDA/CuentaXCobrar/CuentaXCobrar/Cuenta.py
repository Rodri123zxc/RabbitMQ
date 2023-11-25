from datetime import datetime, timedelta

class Cuenta:
    def __init__(self, middleware, bd):
        self.middleware = middleware
        self.bd = bd
        
    def iniciarSistema(self):
        try :
            self.middleware.iniciar()
        except Exception:
            print("Error en inicar middleware")
            
        try :                 
            while (True): 
                self.middleware.recibirYProcesarMensaje()
                mensajeRecibido = self.middleware.getMensaje()
                
                if mensajeRecibido != None :
                    print("Mensaje recibido: "+ str(mensajeRecibido))
                    self.generarCuenta(mensajeRecibido)
                    self.middleware.limpiarMensaje()
        except Exception as e:
            print("Error en inicar recepcion de mensajes: "+str(e))
            
    def generarCuenta(self,mensajeRecibido):

        try:
            
            fecha = datetime.now()
            fecha_hoy = fecha.strftime('%Y-%m-%d')
            fecha_hoy = datetime.strptime(fecha_hoy, '%Y-%m-%d') 
            fecha_nueva = fecha_hoy + timedelta(days=7)

            fecha_pago = fecha_nueva.strftime('%Y-%m-%d')
            
            id_factura = mensajeRecibido
            
            cuentaxcobrar = "INSERT INTO public.\"CuentaxCobrar\" (\"ID_FACTURA_FK\",\"Fecha_cobro\",\"Estado\") VALUES ("+str(id_factura)+",\'"+str(fecha_pago)+"\',\'"+"0"+"\');"
            
            print("cuentaxcobrar" + cuentaxcobrar)
                
            self.bd.ejecutar_insert(cuentaxcobrar)

            mensaje = "Factura n.: "+str(id_factura)+"// Pagar el: " + str(fecha_pago)
            
            print("mensaje: "+mensaje)
            
            self.middleware.enviarMensaje( mensaje)
                
        except Exception:
            print("Error al intentar actualziar la BD")
            