class Reservacion:
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
                
                if len(mensajeRecibido) > 0 :
                    print("Mensaje recibido: "+ str(mensajeRecibido))
                    self.reservarItems(mensajeRecibido)
                    self.middleware.limpiarMensaje()
        except Exception:
            print("Error en inicar recepcion de mensajes")
            
    def reservarItems(self,mensajeRecibido):
        ids = []
        cantidades = []
        
        for item in mensajeRecibido:
            ids.append(item[0]) 
            cantidades.append(item[2])
            
        try:
            for i in range(len(ids)):
                consultaUpdate = "UPDATE public.\"Articulo\" SET cantidad_existente = cantidad_existente - "+cantidades[i]+" WHERE \"ID_Articulo\" = \'" + ids[i] + "\';"
                self.bd.ejecutar_update(consultaUpdate)
           
            print("Cambios realizados")
            
            mensaje = []
            
            for i in range(len(ids)):
                item = [ids[i],cantidades[i]] 
                print(str(item))   
                mensaje.append(item)
                
            print(str(mensaje))
            
            self.middleware.enviarMensaje(mensaje)
                
        except Exception:
            print("Error al intentar actualziar la BD")
            