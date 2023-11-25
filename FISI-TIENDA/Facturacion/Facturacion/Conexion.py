import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

class Conexion:
    def __init__(self):
        self.conectar = None

    def establecerConexion(self):
        try:
            self.conectar = psycopg2.connect(
                host = os.environ["HOST"],
                user = os.environ["USER"],
                password = os.environ["PASSWORD"],
                database = os.environ["DATABASE"],
                port = os.environ["PORT"]
            )
            return self.conectar
        except Exception as ex:
            print("Error al conectarse a la base de datos\nError:" + str(ex))

    def ejecutar_select(self, consulta):
        resultados = None
        
        if self.conectar:
            try:
                cursor = self.conectar.cursor()
                cursor.execute(consulta)
                resultados = cursor.fetchall()
                print("Resultados"+str(resultados))# Obtener todos los resultados de la consulta SELECT
                cursor.close()
            except Exception as e:
                print("Error al ejecutar la consulta SELECT\nError:", e)
        return resultados
    
    
    def ejecutar_update(self,consulta):
        filas_afectadas = 0

        if self.conectar:
            try:
                cursor = self.conectar.cursor()
                cursor.execute(consulta)
                filas_afectadas = cursor.rowcount
                self.conectar.commit()
                cursor.close()
            except Exception as e:
                print("Error al ejecutar la consulta UPDATE/DELETE/INSERT\nError:", e)
                self.conectar.rollback()
        return filas_afectadas
    
    def ejecutar_insert(self, consulta):
        filas_insertadas = 0
        
        if self.conectar:
            try:
                cursor = self.conectar.cursor()
                cursor.execute(consulta)
                filas_insertadas = cursor.rowcount
                self.conectar.commit()
                cursor.close()
            except Exception as e:
                print("Error al ejecutar la consulta INSERT\nError:", e)
                self.conectar.rollback()
        return filas_insertadas