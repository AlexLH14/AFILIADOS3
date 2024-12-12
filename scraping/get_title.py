#'''

from selenium import webdriver
from database.db_config import insert_log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from urllib.parse import urlparse

from selenium.webdriver.chrome.options import Options

def get_product_title(url):
    """Determina la plataforma con base en la URL final y obtiene el título del producto."""
    driver = get_remote_driver()  # Inicia el driver remoto
    try:
        # Abre la URL y deja que se redireccione
        driver.get(url)
        time.sleep(3)  # Tiempo para permitir redirecciones (ajustable según la conexión)

        # Obtén la URL final después de redireccionamiento
        final_url = driver.current_url
        domain = urlparse(final_url).netloc
        print(f"URL final detectada: {final_url}")

        # Decide la plataforma basada en el dominio final
        if "amazon" in domain:
            return get_product_title_amazon(final_url, driver)  # Pasa el driver
        elif "mercadolibre" in domain:
            return get_product_title_mercadolibre(final_url, driver)  # Pasa el driver
        else:
            raise ValueError(f"URL no soportada: {final_url}. Solo Amazon o Mercado Libre son válidos.")
    except Exception as e:
        print(f"Error al procesar la URL: {e}")
        return f"Error al procesar la URL: {e}"
    finally:
        driver.quit()


def get_remote_driver():
    """Configura un controlador remoto para Selenium."""
    options = Options()
    options.add_argument("--start-maximized")  # Maximiza la ventana
    options.add_argument("--disable-gpu")  # Deshabilita la GPU

    # Configuración del WebDriver remoto
    driver = webdriver.Remote(
        command_executor="http://host.docker.internal:4444",  # Sin /wd/hub
        options=options
    )
    return driver

def get_product_title_amazon(url, driver):
    print("Iniciando get_title amazon----------")
    try:
        # Asume que ya estás en la página de Amazon
        skip_captcha(driver)

        titulo_elemento = driver.find_element(By.ID, "productTitle")
        titulo = titulo_elemento.text.strip() if titulo_elemento else "No se encontró el título del producto"
        print(titulo)

        insert_log('success', f'Título obtenido exitosamente: "{titulo}" para la URL: {url}')
        return titulo
    except Exception as e:
        insert_log('error', 'Error al obtener el título del producto', details=str(e))
        return f"Error al obtener el producto: {e}"




def skip_captcha(driver):
    """Función para manejar el captcha en Amazon"""
    try:
        # Espera a que el botón "Try different image" sea visible y clickeable
        retry_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Try different image')]"))
        )
        retry_button.click()
        print("Captcha: Se hizo clic en 'Probar una imagen diferente'.")
    except TimeoutException:
        # Si no se encuentra el botón dentro del tiempo esperado, refresca la página
        print("Captcha: No se encontró el botón en el tiempo esperado. Refrescando la página...")
        driver.refresh()
        time.sleep(2)  # Agregar una pausa breve después de refrescar


def get_product_title_mercadolibre(url, driver):
    print("Iniciando mercadolibre----------")
    try:
        # Asume que ya estás en la página de Mercado Libre
        titulo_elemento = driver.find_element(By.CLASS_NAME, "ui-pdp-title")
        titulo = titulo_elemento.text.strip() if titulo_elemento else "No se encontró el título del producto"
        print(titulo)

        insert_log('success', f'Título obtenido exitosamente: "{titulo}" para la URL: {url}')
        return titulo
    except Exception as e:
        insert_log('error', 'Error al obtener el título del producto', details=str(e))
        return f"Error al obtener el producto: {e}"



'''
from selenium import webdriver
from database.db_config import insert_log
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from urllib.parse import urlparse


def get_product_title(url):
    domain = urlparse(url).netloc
    if "amazon" in domain:
        return get_product_title_amazon(url)
    elif "mercadolibre" in domain:
        return get_product_title_mercadolibre(url)
    else:
        raise ValueError("URL no soportada. Solo Amazon o Mercado Libre son válidos.")
def get_product_title_amazon(url):
    driver = webdriver.Chrome()
    driver.maximize_window()
    print("iniciando get_title.py----------")

    # Obtener y mostrar la versión y la ruta del ChromeDriver
    driver_version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
    driver_path = driver.service.path
    print(f"Versión de ChromeDriver: {driver_version}")
    print(f"Ruta de ChromeDriver: {driver_path}")

    try:
        driver.get(url)
        time.sleep(3)

        skip_captcha(driver)

        titulo_elemento = driver.find_element(By.ID, "productTitle")
        titulo = titulo_elemento.text.strip() if titulo_elemento else "No se encontró el título del producto"
        print(titulo)

        insert_log('success', f'Título obtenido exitosamente: "{titulo}" para la URL: {url}')
        return titulo
    except Exception as e:
        insert_log('error', 'Error al obtener el título del producto', details=str(e))
        return f"Error al obtener el producto: {e}"
    finally:
        driver.quit()



def skip_captcha(driver):
    """Función para manejar el captcha en Amazon"""
    try:
        # Espera a que el botón "Try different image" sea visible y clickeable
        retry_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Try different image')]"))
        )
        retry_button.click()
        print("Captcha: Se hizo clic en 'Probar una imagen diferente'.")
    except TimeoutException:
        # Si no se encuentra el botón dentro del tiempo esperado, refresca la página
        print("Captcha: No se encontró el botón en el tiempo esperado. Refrescando la página...")
        driver.refresh()
        time.sleep(2)  # Agregar una pausa breve después de refrescar
def get_product_title_mercadolibre(url):
    print("Iniciando mercadolibre.py----------")
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        driver.get(url)
        time.sleep(3)

        titulo_elemento = driver.find_element(By.CLASS_NAME, "ui-pdp-title")
        titulo = titulo_elemento.text.strip() if titulo_elemento else "No se encontró el título del producto"
        print(titulo)

        insert_log('success', f'Título obtenido exitosamente: "{titulo}" para la URL: {url}')
        return titulo
    except Exception as e:
        insert_log('error', 'Error al obtener el título del producto', details=str(e))
        return f"Error al obtener el producto: {e}"
    finally:
        driver.quit()
'''