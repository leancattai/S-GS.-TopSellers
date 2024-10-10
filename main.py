import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Obtén las credenciales desde las variables de entorno
email = os.getenv('MY_EMAIL')
password = os.getenv('MY_PASSWORD')

# Configura el WebDriver
driver_path = r'C:\Users\Usuario\Desktop\Work Space\Top sellers\chromedriver-win64\chromedriver.exe'
service = Service(executable_path=driver_path)
options = Options()
driver = webdriver.Chrome(service=service, options=options)

try:
    # Accede a la página web
    driver.get("https://gsconectar.web.app/")

    # Espera a que el campo de correo electrónico esté visible y clickeable
    email_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loggedoutEmail"]'))
    )
    email_field.click()
    email_field.send_keys(email)

    # Espera a que el campo de contraseña esté visible y clickeable
    password_field = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loggedoutPass"]'))
    )
    password_field.click()
    password_field.send_keys(password)

    # Opcional: Enviar el formulario
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loggedoutDiv"]/button'))
    )
    submit_button.click()
    time.sleep(10)

except Exception as e:
    print(f"Error: {e}")



# Encuentra y haz clic en el elemento "Tablero Líderes"
# Nota: Deberás inspeccionar la página y ajustar el XPath según sea necesario
try:
    leaders_tab = driver.find_element(By.XPATH, '//*[@id="sideMenuButtons"]/a[6]')  # Ajusta el XPath
    leaders_tab.click()
    leaders_tab.click()

    
except Exception as e:
    print("No se pudo encontrar el elemento 'Tablero Líderes'", e)
    driver.quit()
    exit()

# Espera a que se cargue el contenido del "Tablero Líderes"
time.sleep(10)  # Ajusta el tiempo según sea necesario

# Extrae los datos de la tabla o de los elementos necesarios
data = []
try:
    # Encuentra todas las filas de la tabla
    rows = driver.find_elements(By.XPATH, '//*[@id="leaderDashboard"]/table/tbody/tr')  # Ajusta el XPath para las filas de la tabla
    
    for row in rows:
        # Encuentra todas las celdas (columnas) dentro de cada fila
        cols = row.find_elements(By.XPATH, './/td')  # Utiliza un XPath relativo para las columnas
        data.append([col.text for col in cols])  # Agrega el texto de cada columna a la lista de datos

except Exception as e:
    print("No se pudo extraer los datos de la tabla", e)

# Cierra el WebDriver
driver.quit()

# Verifica los datos extraídos
print(data)

# Crea un DataFrame de Pandas con los datos extraídos
# Asegúrate de ajustar el número de columnas según los datos extraídos
df = pd.DataFrame(data, columns=['Columna1', 'Columna2', 'Columna3'])  # Ajusta los nombres de las columnas según corresponda

# Guarda los datos en un archivo Excel
output_path = 'output_folder/filename.xlsx'  # Cambia la ruta de la carpeta de salida y el nombre del archivo
df.to_excel(output_path, index=False)

print("Datos extraídos y guardados en", output_path)
