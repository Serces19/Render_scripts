import sqlite3
from sqlite3 import Error


class manager_db():
    def __init__(self):

        self.TIMER = 30
        self.DB_path = 'C:/Users/sergi/.nuke/Manager_panel/db/Manager.db'
        
        # conectar con la base de datos 
        self.conn = sqlite3.connect(self.DB_path)
        self.cur = self.conn.cursor()

    ##################################################################
    ### Metodos

    def leer_datos(self):
        # Crear tabla si no existe
        self.cur.execute('''
                         CREATE TABLE IF NOT EXISTS to_render 
                         ( comando TEXT UNIQUE NOT NULL)
        ''') 
        try:
            # Ejecuta una consulta para obtener todos los registros de la tabla
            self.cur.execute("SELECT * FROM to_render")
            records = self.cur.fetchall()
            result = list()
            for item in records:
                result.append(item[0])
                print(item[0])
            print('result: ', result)
            return result
        
        finally:
            
            # Cierra la conexión a la base de datos
            self.conn.close()

