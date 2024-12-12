from scraping.get_title import get_product_title
from utils.ai_recommendations import generate_recommendation
from scraping.youtube import search_and_play_youtube_video
from utils.categories import (
    select_random_category,
    select_random_variant,
    select_random_link
)
from database.db_config import start_db

start_db()

# Selección aleatoria de categoría
categoria = select_random_category()
if categoria:
    categoria_id, categoria_nombre = categoria

    # Selección aleatoria de variante
    search_variant = select_random_variant(categoria_id)

    # Selección aleatoria de link y producto ID
    link_data = select_random_link(categoria_id)
    if link_data:
        producto_id, selected_link, titulo_producto, descripcion_producto = link_data

        if search_variant:
            # Obtener el título del producto
            print(titulo_producto)
            #titulo_producto = get_product_title(selected_link)

            # Generar comentario con Cohere
            try:
                recommendation = generate_recommendation(titulo_producto, descripcion_producto)
                print(f"Comentario generado:\n{recommendation}")
                print("pruebas ----------------------------")

                # Publicar comentario en YouTube
                search_and_play_youtube_video(search_variant, recommendation, producto_id, categoria_id, selected_link)
            except Exception as e:
                print("Error al generar recomendación:", e)
        else:
            print("No se encontraron variantes para la categoría seleccionada.")
    else:
        print("No se encontraron productos para la categoría seleccionada.")
else:
    print("No hay categorías disponibles en la base de datos.")