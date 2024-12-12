import cohere
from database.db_config import insert_log

def generate_recommendation(title, description):
    #co = cohere.Client("An1plkGRHSk5uRBTAsHfBLXh6zeDC66ypTATLpRG")
    co = cohere.Client("ENu8kO7bsExfEaBfJUXksat0BvztlnzzgvhSfftM")
    prompt = (
        f"Escribe una recomendación personal en español sobre el siguiente libro en línea: {title}. "
        f"Descripción del libro: {description}. "
        "La recomendación debe estar escrita en español mexico, mostrando entusiasmo y destacando las razones por las que este libro es interesante o útil. "
        "Incluye una breve opinión personal sobre el contenido y a quién recomendarías este libro. "
        "Sé auténtico y escribe como si estuvieras recomendándolo a un amigo. Responde únicamente en español."
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
