import sqlite3
from db_config import get_logs, get_comments, start_db, DB_PATH
from insert_data import insert_category,insert_product,insert_variant
from utils.categories import get_categories, get_links_by_category, get_variants_by_category


# Inicializar la base de datos y crear las tablas si no existen
'''
start_db()
print("Base de datos y tablas inicializadas correctamente.")
'''

# Conectar a la base de datos
'''
conexion = sqlite3.connect(DB_PATH)
cursor = conexion.cursor()

# Mostrar las tablas creadas
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()
conexion.close()

print("Tablas creadas:", tablas)
'''

#CATEGORIAS
#1 smartphones
#2 tenis


#INSERTAR DATOS SI NO EXISTEN USANDO LAS FUNCIONES DE INSERT_DATA
#'''
#insert_category("books_english")
insert_variant("aprender ingles", 1)  # ID de la categoría

'''insert_product(
    "https://go.hotmart.com/N97052740C?dp=1",
    1,
    nombre="APRENDE INGLÉS EN 90 DÍAS",
    descripcion="Curso de inglés en línea con cuentos cortos bilingües y podcast."
)'''

#'''


#VERIFICAR DATOS INSERTADOS
'''
# Verificar categorías
print("Categorías:", get_categories())

# Verificar variantes de búsqueda
print("Variantes de búsqueda:", get_variants_by_category(1))  # 1: ID de la categoría "smartphones"

# Verificar productos
print("Productos:", get_links_by_category(1))  # 1: ID de la categoría "smartphones"
'''

'''
# Obtener y mostrar los comentarios
comentarios = get_comments()
print("Comentarios registrados:")
for comentario in comentarios:
    video_url = f"https://www.youtube.com/watch?v={comentario[4]}"  # Construir el link completo del video
    print(f"ID: {comentario[0]}")
    print(f"Comentario: {comentario[1]}")
    print(f"Producto: {comentario[2]}")
    print(f"Categoría: {comentario[3]}")
    print(f"Video ID: {comentario[4]}")
    print(f"Timestamp: {comentario[5]}")
    print(f"Video URL: {video_url}")  # Mostrar el link del video
    print("-" * 40)
'''
'''
logs = get_logs()
print("Logs registrados:")
for log in logs:
    print(f"ID: {log[0]}")
    print(f"Timestamp: {log[1]}")
    print(f"Status: {log[2]}")
    print(f"Message: {log[3]}")
    print(f"Details: {log[4]}")
    print("-" * 40)
    
#'''