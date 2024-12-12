#'''

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from database.db_config import load_record, save_record, insert_comment, insert_log

CHROME_PROFILE_PATH = "C:/Users/alex2/AppData/Local/Google/Chrome/User Data/Profile 2"

from selenium.webdriver.chrome.options import Options

def get_remote_driver():
    """Configura un controlador remoto para Selenium."""
    options = Options()
    options.add_argument("--start-maximized")  # Maximiza la ventana
    options.add_argument("--disable-gpu")  # Deshabilita la GPU
    options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
    # Configuración del WebDriver remoto
    driver = webdriver.Remote(
        command_executor="http://host.docker.internal:4444",  # Sin /wd/hub
        options=options
    )
    return driver


def search_and_play_youtube_video(search_query, comment_text, producto_id, categoria_id, link_producto ):
    driver = get_remote_driver()  # Utiliza el controlador remoto
    time.sleep(5)


    video_log = load_record()

    try:
        driver.get("https://www.youtube.com")
        time.sleep(3)

        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        video_tab = driver.find_element(By.XPATH, "//yt-chip-cloud-chip-renderer[.//yt-formatted-string[text()='Vídeos']]")
        video_tab.click()

        filter_button = driver.find_element(By.ID, 'filter-button')
        filter_button.click()
        time.sleep(5)

        filtro_relevancia = driver.find_element(By.XPATH, "//ytd-search-filter-group-renderer[.//yt-formatted-string[text()='Ordenar por']]//ytd-search-filter-renderer[.//yt-formatted-string[text()='Relevancia']]")
        filtro_relevancia.click()

        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        time.sleep(15)

        videos = driver.find_elements(By.XPATH, "(//a[contains(@href, 'watch') and @id='video-title'])")
        for video in videos:
            video_url = video.get_attribute("href")
            video_id = video_url.split("v=")[-1].split("&")[0]

            if video_id not in video_log:
                video.click()
                time.sleep(5)

                # Concatenar el enlace al comentario para publicarlo en YouTube
                comentario_youtube = f"{comment_text}\n\nEnlace del producto: {link_producto}"
                insert_log('info', f'Intentando comentar en el video: {video_url}')

                if leave_comment(driver, comentario_youtube):
                    video_log_id = save_record(video_id)
                    insert_comment(comment_text, producto_id, video_log_id, categoria_id) #----------------------------
                    insert_log('success', f'Comentario publicado exitosamente en el video: {video_url}')
                    time.sleep(10)
                    return
                else:
                    insert_log('error', f'Error al intentar comentar en el video: {video_url}')
                return
        print("No se encontraron videos nuevos para comentar.")
        insert_log('info', 'No se encontraron videos nuevos para comentar.')

    finally:
        driver.quit()

def leave_comment(driver, comment_text):
    try:
        insert_log('info', 'dentro de leave_comment')
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)

        comment_box = driver.find_element(By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer")
        comment_box.click()
        time.sleep(2)

        input_box = driver.find_element(By.ID, "contenteditable-root")
        input_box.send_keys(comment_text)
        time.sleep(10)

        submit_button = driver.find_element(By.XPATH, "//ytd-button-renderer[@id='submit-button']")
        submit_button.click()
        time.sleep(3)

        print("Comentario publicado exitosamente.")
        return True
    except Exception as e:
        print(f"Error al intentar comentar: {e}")
        insert_log('error', 'Error al intentar publicar un comentario.', details=str(e))
        return False




'''
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from database.db_config import load_record, save_record, insert_comment, insert_log

CHROME_PROFILE_PATH = "C:/Users/alex2/AppData/Local/Google/Chrome/User Data/Profile 2"

def search_and_play_youtube_video(search_query, comment_text, producto_id, categoria_id, link_producto ):
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    time.sleep(5)

    video_log = load_record()

    try:
        driver.get("https://www.youtube.com")
        time.sleep(3)

        search_box = driver.find_element(By.NAME, "search_query")
        search_box.send_keys(search_query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)

        video_tab = driver.find_element(By.XPATH, "//yt-chip-cloud-chip-renderer[.//yt-formatted-string[text()='Vídeos']]")
        video_tab.click()

        filter_button = driver.find_element(By.ID, 'filter-button')
        filter_button.click()
        time.sleep(5)

        filtro_relevancia = driver.find_element(By.XPATH, "//ytd-search-filter-group-renderer[.//yt-formatted-string[text()='Ordenar por']]//ytd-search-filter-renderer[.//yt-formatted-string[text()='Relevancia']]")
        filtro_relevancia.click()

        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ESCAPE)
        time.sleep(15)

        videos = driver.find_elements(By.XPATH, "(//a[contains(@href, 'watch') and @id='video-title'])")
        for video in videos:
            video_url = video.get_attribute("href")
            video_id = video_url.split("v=")[-1].split("&")[0]

            if video_id not in video_log:
                video.click()
                time.sleep(5)

                # Concatenar el enlace al comentario para publicarlo en YouTube
                comentario_youtube = f"{comment_text}\n\nEnlace del producto: {link_producto}"
                insert_log('info', f'Intentando comentar en el video: {video_url}')

                if leave_comment(driver, comentario_youtube):
                    video_log_id = save_record(video_id)
                    insert_comment(comment_text, producto_id, video_log_id, categoria_id) #----------------------------
                    insert_log('success', f'Comentario publicado exitosamente en el video: {video_url}')
                    return
                else:
                    insert_log('error', f'Error al intentar comentar en el video: {video_url}')
                return
        print("No se encontraron videos nuevos para comentar.")
        insert_log('info', 'No se encontraron videos nuevos para comentar.')

    finally:
        driver.quit()

def leave_comment(driver, comment_text):
    try:
        insert_log('info', 'dentro de leave_comment')
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(2)

        comment_box = driver.find_element(By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer")
        comment_box.click()
        time.sleep(2)

        input_box = driver.find_element(By.ID, "contenteditable-root")
        input_box.send_keys(comment_text)
        time.sleep(10)

        submit_button = driver.find_element(By.XPATH, "//ytd-button-renderer[@id='submit-button']")
        submit_button.click()
        time.sleep(3)

        print("Comentario publicado exitosamente.")
        return True
    except Exception as e:
        print(f"Error al intentar comentar: {e}")
        insert_log('error', 'Error al intentar publicar un comentario.', details=str(e))
        return False
'''