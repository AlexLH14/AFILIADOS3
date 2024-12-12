import sqlite3
import random
from database.db_config import DB_PATH

def get_categories():
    """
    Devuelve una lista de todas las categorías desde la base de datos.
    """
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute('SELECT id, nombre FROM categorias')
    categorias = cursor.fetchall()  # Devuelve [(id, nombre), ...]
    conexion.close()
    return categorias

def get_variants_by_category(categoria_id):
    """
    Devuelve una lista de variantes de búsqueda asociadas a una categoría.
    """
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute('SELECT variante FROM variantes_busqueda WHERE categoria_id = ?', (categoria_id,))
    variantes = [fila[0] for fila in cursor.fetchall()]
    conexion.close()
    return variantes

def get_links_by_category(categoria_id):
    """
    Devuelve una lista de links de productos asociados a una categoría.
    """
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute('SELECT link FROM productos WHERE categoria_id = ?', (categoria_id,))
    links = [fila[0] for fila in cursor.fetchall()]
    conexion.close()
    return links

def select_random_category():
    """
    Selecciona aleatoriamente una categoría y devuelve su ID y nombre.
    """
    categorias = get_categories()
    if categorias:
        return random.choice(categorias)  # Devuelve (id, nombre)
    else:
        return None

def select_random_variant(categoria_id):
    """
    Selecciona aleatoriamente una variante de búsqueda asociada a una categoría.
    """
    variantes = get_variants_by_category(categoria_id)
    if variantes:
        return random.choice(variantes)
    else:
        return None

def select_random_link(categoria_id):
    """
    Selecciona aleatoriamente un producto asociado a una categoría y devuelve su ID, link, título y descripción.
    """
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute('SELECT id, link, nombre, descripcion FROM productos WHERE categoria_id = ?', (categoria_id,))
    productos = cursor.fetchall()  # Devuelve [(id, link, nombre, descripcion), ...]
    conexion.close()

    if productos:
        return random.choice(productos)  # Devuelve (id, link, nombre, descripcion)
    else:
        return None

