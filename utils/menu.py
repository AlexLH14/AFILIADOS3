import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from database.db_config import DB_PATH, get_logs, get_comments
from utils.categories import get_categories, get_variants_by_category, get_links_by_category

# Funciones de la base de datos
def obtener_categorias():
    """Obtiene las categorías de la base de datos."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre FROM categorias")
    categorias = cursor.fetchall()
    conexion.close()
    return categorias

def agregar_producto():
    """Agrega un producto a la base de datos."""
    link = entry_link.get().strip()
    categoria_id = combo_categoria.get().split(" - ")[0]
    nombre = entry_nombre.get().strip()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()

    if not link or not categoria_id:
        messagebox.showerror("Error", "El campo 'Link' y 'Categoría' son obligatorios.")
        return

    try:
        categoria_id = int(categoria_id)
    except ValueError:
        messagebox.showerror("Error", "Categoría inválida.")
        return

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO productos (link, categoria_id, nombre, descripcion) VALUES (?, ?, ?, ?)",
            (link, categoria_id, nombre, descripcion)
        )
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        limpiar_campos_producto()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", f"El producto con el link '{link}' ya existe.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al agregar el producto: {e}")

def agregar_categoria():
    """Agrega una categoría a la base de datos."""
    nombre_categoria = entry_categoria_nombre.get().strip()

    if not nombre_categoria:
        messagebox.showerror("Error", "El nombre de la categoría no puede estar vacío.")
        return

    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO categorias (nombre) VALUES (?)", (nombre_categoria,))
        conexion.commit()
        conexion.close()
        messagebox.showinfo("Éxito", "Categoría agregada correctamente.")
        entry_categoria_nombre.delete(0, tk.END)
        actualizar_categorias()
    except Exception as e:
        messagebox.showerror("Error", f"Error al agregar la categoría: {e}")

def mostrar_categorias():
    """Muestra las categorías en la tabla."""
    categorias = obtener_categorias()
    for row in tabla_categorias.get_children():
        tabla_categorias.delete(row)

    for categoria in categorias:
        tabla_categorias.insert("", "end", values=categoria)

def limpiar_campos_producto():
    """Limpia los campos del formulario de productos."""
    entry_link.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_descripcion.delete("1.0", tk.END)
    combo_categoria.set("")

def actualizar_categorias():
    """Actualiza la lista de categorías en el combo."""
    combo_categoria['values'] = [f"{cat[0]} - {cat[1]}" for cat in obtener_categorias()]

def mostrar_variantes():
    """Muestra las variantes por categoría."""
    categoria_id = entry_categoria_variantes.get().strip()

    if not categoria_id:
        messagebox.showerror("Error", "Debes ingresar un ID de categoría.")
        return

    try:
        categoria_id = int(categoria_id)
    except ValueError:
        messagebox.showerror("Error", "El ID de categoría debe ser un número.")
        return

    variantes = get_variants_by_category(categoria_id)
    for row in tabla_variantes.get_children():
        tabla_variantes.delete(row)

    if variantes:
        for variante in variantes:
            tabla_variantes.insert("", "end", values=(variante,))
    else:
        messagebox.showinfo("Información", "No hay variantes registradas para esta categoría.")

def mostrar_logs():
    """Muestra los logs."""
    logs = get_logs()
    for row in tabla_logs.get_children():
        tabla_logs.delete(row)

    if logs:
        for log in logs:
            tabla_logs.insert("", "end", values=log)
    else:
        messagebox.showinfo("Información", "No hay logs registrados.")

def mostrar_comentarios():
    """Muestra los comentarios."""
    comentarios = get_comments()
    for row in tabla_comentarios.get_children():
        tabla_comentarios.delete(row)

    if comentarios:
        for comentario in comentarios:
            video_url = f"https://www.youtube.com/watch?v={comentario[4]}"
            tabla_comentarios.insert("", "end", values=(comentario[0], comentario[1], comentario[2], comentario[3], video_url, comentario[5]))
    else:
        messagebox.showinfo("Información", "No hay comentarios registrados.")

# Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Gestión de Productos y Categorías")
ventana.geometry("1000x800")

# Configuración de pestañas
notebook = ttk.Notebook(ventana)
notebook.pack(fill="both", expand=True)

# Pestaña: Agregar Producto
frame_productos = ttk.Frame(notebook)
notebook.add(frame_productos, text="Agregar Producto")

tk.Label(frame_productos, text="Link del producto:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_link = tk.Entry(frame_productos, width=50)
entry_link.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame_productos, text="Nombre del producto:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
entry_nombre = tk.Entry(frame_productos, width=50)
entry_nombre.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame_productos, text="Descripción:").grid(row=2, column=0, padx=10, pady=10, sticky="nw")
entry_descripcion = tk.Text(frame_productos, width=50, height=5)
entry_descripcion.grid(row=2, column=1, padx=10, pady=10)

tk.Label(frame_productos, text="Categoría:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
combo_categoria = ttk.Combobox(frame_productos, width=47, state="readonly")
combo_categoria.grid(row=3, column=1, padx=10, pady=10)

btn_agregar_producto = tk.Button(frame_productos, text="Agregar Producto", command=agregar_producto)
btn_agregar_producto.grid(row=4, column=0, columnspan=2, pady=20)

# Pestaña: Agregar Categoría
frame_categorias = ttk.Frame(notebook)
notebook.add(frame_categorias, text="Agregar Categoría")

tk.Label(frame_categorias, text="Nombre de la categoría:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_categoria_nombre = tk.Entry(frame_categorias, width=50)
entry_categoria_nombre.grid(row=0, column=1, padx=10, pady=10)

btn_agregar_categoria = tk.Button(frame_categorias, text="Agregar Categoría", command=agregar_categoria)
btn_agregar_categoria.grid(row=1, column=0, columnspan=2, pady=20)

# Pestaña: Mostrar Categorías
frame_mostrar_categorias = ttk.Frame(notebook)
notebook.add(frame_mostrar_categorias, text="Mostrar Categorías")

tabla_categorias = ttk.Treeview(frame_mostrar_categorias, columns=("ID", "Nombre"), show="headings")
tabla_categorias.heading("ID", text="ID")
tabla_categorias.heading("Nombre", text="Nombre")
tabla_categorias.pack(fill="both", expand=True)

btn_mostrar_categorias = tk.Button(frame_mostrar_categorias, text="Actualizar Categorías", command=mostrar_categorias)
btn_mostrar_categorias.pack(pady=10)

# Pestaña: Mostrar Variantes
frame_variantes = ttk.Frame(notebook)
notebook.add(frame_variantes, text="Mostrar Variantes")

tk.Label(frame_variantes, text="ID de Categoría:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
entry_categoria_variantes = tk.Entry(frame_variantes, width=20)
entry_categoria_variantes.grid(row=0, column=1, padx=10, pady=10)

btn_mostrar_variantes = tk.Button(frame_variantes, text="Mostrar Variantes", command=mostrar_variantes)
btn_mostrar_variantes.grid(row=0, column=2, padx=10, pady=10)

tabla_variantes = ttk.Treeview(frame_variantes, columns=("Variante",), show="headings")
tabla_variantes.heading("Variante", text="Variante")
tabla_variantes.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Pestaña: Mostrar Logs
frame_logs = ttk.Frame(notebook)
notebook.add(frame_logs, text="Mostrar Logs")

tabla_logs = ttk.Treeview(frame_logs, columns=("ID", "Timestamp", "Status", "Message", "Details"), show="headings")
tabla_logs.heading("ID", text="ID")
tabla_logs.heading("Timestamp", text="Timestamp")
tabla_logs.heading("Status", text="Status")
tabla_logs.heading("Message", text="Message")
tabla_logs.heading("Details", text="Details")
tabla_logs.pack(fill="both", expand=True)

btn_mostrar_logs = tk.Button(frame_logs, text="Actualizar Logs", command=mostrar_logs)
btn_mostrar_logs.pack(pady=10)

# Pestaña: Mostrar Comentarios
frame_comentarios = ttk.Frame(notebook)
notebook.add(frame_comentarios, text="Mostrar Comentarios")

tabla_comentarios = ttk.Treeview(
    frame_comentarios,
    columns=("ID", "Comentario", "Producto", "Categoría", "Video URL", "Timestamp"),
    show="headings"
)
tabla_comentarios.heading("ID", text="ID")
tabla_comentarios.heading("Comentario", text="Comentario")
tabla_comentarios.heading("Producto", text="Producto")
tabla_comentarios.heading("Categoría", text="Categoría")
tabla_comentarios.heading("Video URL", text="Video URL")
tabla_comentarios.heading("Timestamp", text="Timestamp")
tabla_comentarios.pack(fill="both", expand=True)

btn_mostrar_comentarios = tk.Button(frame_comentarios, text="Actualizar Comentarios", command=mostrar_comentarios)
btn_mostrar_comentarios.pack(pady=10)

# Inicializar datos
actualizar_categorias()

# Iniciar la ventana
ventana.mainloop()
