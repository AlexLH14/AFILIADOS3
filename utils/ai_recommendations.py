import cohere
from database.db_config import insert_log

def generate_recommendation(title, description):
    #co = cohere.Client("An1plkGRHSk5uRBTAsHfBLXh6zeDC66ypTATLpRG")
    co = cohere.Client("ENu8kO7bsExfEaBfJUXksat0BvztlnzzgvhSfftM")
    prompt = (
        f"Escribe una recomendación personal sobre el libro '{title}', en español (variación de México). "
        f"Descripción del libro: {description}. "
        "La recomendación debe ser auténtica y escrita como si estuvieras recomendándola a un amigo. "
        "Destaca por qué el libro es interesante o útil, incluye una breve opinión personal sobre el contenido, "
        "y menciona a quién le recomendarías este libro. Sé conciso, directo y no incluyas despedidas ni frases genéricas como 'inserte su nombre'."
    )

    try:
        response = co.generate(
            model="command-xlarge",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        recommendation = response.generations[0].text.strip()

        # Log de éxito
        insert_log('success', f'Recomendación generada exitosamente para el producto: {title}')
        return recommendation
    except Exception as e:
        # Log de error
        insert_log('error', 'Error al generar recomendación', details=str(e))
        raise  # Relanzar la excepción para que el llamador pueda manejarla
