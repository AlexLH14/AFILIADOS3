import sqlite3
from db_config import DB_PATH

# Conexión a la base de datos
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

try:
    # Agregar la nueva columna 'descripcion'
    cursor.execute("ALTER TABLE productos ADD COLUMN descripcion TEXT;")
    connection.commit()
    print("Columna 'descripcion' agregada con éxito.")
except Exception as e:
    print(f"Error al agregar la columna: {e}")
finally:
    connection.close()
