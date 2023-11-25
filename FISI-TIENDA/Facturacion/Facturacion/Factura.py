from datetime import datetime, timedelta

class Factura:
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
                    self.generarFactura(mensajeRecibido)
                    self.middleware.limpiarMensaje()
        except Exception:
            print("Error en inicar recepcion de mensajes")
            
    def generarFactura(self,mensajeRecibido):
        ids = []
        cantidades = []
        
        for item in mensajeRecibido:
            ids.append(item[0]) 
            cantidades.append(item[1])
         
        try:
            
            factura = "INSERT INTO public.\"Factura\" ( \"ID_Cliente_FK\") VALUES ('1');"
            
            self.bd.ejecutar_insert(factura)
            
            ids_factura = self.bd.ejecutar_select("SELECT \"ID_Factura\" FROM public.\"Factura\";")

            id_factura = max([valor[0] for valor in ids_factura])
            
            fecha = datetime.now()
            fecha_hoy = fecha.strftime('%Y-%m-%d')
            
            #fecha_nueva = fecha_hoy + timedelta(days=7)
            #fecha_pago = fecha_nueva.strftime('%d/%m/%Y')
            
            total = 0.0
            
            print(str(ids))
            print(str(cantidades))
            
            for i in range(len(ids)):
                #self.bd.ejecutar_insert(factura)
    
                cantidad = int(cantidades[i])
                id_articulo = ids[i]
                
                print("ANTES IMORT")
                
                precioU =  self.bd.ejecutar_select("SELECT precio_unitario FROM public.\"Articulo\" WHERE \"ID_Articulo\" = \'"+id_articulo+"\';")

                precioUnitario = precioU[0][0]
                
                print("Resultado precioUnitario: " + str(precioUnitario))
                
                importe = cantidad * precioUnitario
                
                print("DESPUES IMORT: " + str(importe))
                
                total = total + importe
                
                print("TOTAL: " + str(total))
                                
                insert_fact_det = "INSERT INTO public.\"Fact_det\" (\"Cantidad\",\"Fecha_envio\",\"Importe\",\"Articulo_FK\",\"Factura_FK\") VALUES (\'"+str(cantidad)+"\',\'"+str(fecha_hoy)+"\',\'"+str(importe)+"\',\'"+id_articulo+"\',\'"+str(id_factura)+"\');"
                
                print("insert_fact_det: "+insert_fact_det)
                
                self.bd.ejecutar_insert(insert_fact_det)
           
            igv = total + 0.18
            
            importe_total = total + igv
            
            consultaUpdate = "UPDATE public.\"Factura\" SET \"Importe\" = "+str(total)+", \"Total_IGV\" = "+str(igv)+", \"Importe_total\" = "+ str(importe_total)+ " WHERE \"ID_Factura\" = " + str(id_factura) + ";"
                
            print("consultaUpdate: "+consultaUpdate)
                       
            self.bd.ejecutar_update(consultaUpdate)
            
            print("Cambios realizados")
            
            mensaje = id_factura
            
            self.middleware.enviarMensaje( mensaje)
                
        except Exception:
            print("Error al intentar actualziar la BD")
            