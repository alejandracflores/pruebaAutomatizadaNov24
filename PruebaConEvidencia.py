##########################################################
##   REALIZACIÓN DE DE PRUEBA AUTOMÁTICA CON EVIDENCIA  ##
##########################################################

# IMPORTAR LIBERIAS Y COMPONENTES
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Configuración del desarrollador
def configurar_desarrollador():
    global desarrollador
    desarrollador = input("Por favor, ingresa tu nombre: ")
    print(f"Hola {desarrollador}! Iniciando prueba automatizada...")

# Variables globales
desarrollador = ""  # Se configurará mediante la función
fecha_inicio = time.strftime("%Y-%m-%d %H:%M:%S")
fecha_fin = ""
ruta_base = 'C:\\Users\\Usuario\\Downloads\\RESULTADOS\\'
evidencias = []
fecha_inicio = time.strftime("%Y-%m-%d %H:%M:%S")
fecha_fin = ""
ruta_base = 'C:\\Users\\Usuario\\Downloads\\RESULTADOS\\'
evidencias = []

# Crear carpeta con fecha y hora específica
carpeta_prueba = time.strftime("%Y-%m-%d_%H-%M-%S")
ruta_Reporte = os.path.join(ruta_base, carpeta_prueba)

if not os.path.exists(ruta_Reporte):
    os.makedirs(ruta_Reporte)

#######################
# CREACION DE METODOS
#######################

# METODO DE INICIAR NAVEGADOR
def iniciar_navegador():
    # Crear instancia del servicio de mSeDGEDriver
    driver_path = "C:\\Users\\Usuario\\Downloads\\Instaladores y Programas\\msedgedriver.exe"
    service = Service(driver_path)  # Crear instancia del navegador usando el servicio
    driver = webdriver.Edge(service=service)
    # Maximizar la ventana del navegador
    driver.maximize_window()
    return driver

# METODO GENERAR REPORTE
def cerrar_navegador(driver):
    driver.quit()

# METODO ACCEDER PAGINA PRINCIPAL UNIVERSIDAD
def acceder_pagina_principal(driver):
    global ruta_Reporte
    url_principal = "https://www.umng.edu.co"
    driver.get(url_principal)
    time.sleep(2)  # Esperar a que cargue la página
    driver.save_screenshot(os.path.join(ruta_Reporte, "paso1.png"))  # Tomar pantallazo como evidencia y guardarlo
    evidencias.append("Paso: 1")
    evidencias.append("Fecha y hora: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    evidencias.append("Acceso a la página principal: Correcto")

# METODO NAVEGAR A BIBLIOTECA EN LINEA
def navegar_a_biblioteca(driver):
    global ruta_Reporte
    evidencias.append("Paso: 2")
    evidencias.append("Fecha y hora: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        # Esperar hasta que el enlace sea clickeable
        enlace_biblioteca = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Biblioteca"))
        )
        enlace_biblioteca.click()
        time.sleep(2)
        driver.save_screenshot(os.path.join(ruta_Reporte, "paso2.png"))  # Tomar pantallazo como evidencia
        evidencias.append("Navegación a la biblioteca en línea: Correcto")
    except NoSuchElementException:
        evidencias.append("Navegación a la biblioteca en línea: Fallido")
        driver.quit()
        return False
    return True

# METODO SELECCIONAR BIBLIOTECA ESPECIFICA
def seleccionar_biblioteca_especifica(driver):
    global ruta_Reporte
    evidencias.append("Paso: 3")
    evidencias.append("Fecha y hora: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        # Acceder directamente a la página del catálogo
        driver.get("https://catalogo.unimilitar.edu.co/")

        # Esperar a que el campo de búsqueda esté presente y sea interactuable
        campo_busqueda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "translControl1"))
        )

        # Verificar que estamos en la página correcta
        if "catalogo.unimilitar.edu.co" in driver.current_url:
            time.sleep(2)  # Pequeña pausa para asegurar que la página esté completamente cargada
            driver.save_screenshot(os.path.join(ruta_Reporte, "paso3.png"))
            evidencias.append("Acceso al catálogo de biblioteca: Correcto")
            return True
        else:
            evidencias.append("Acceso al catálogo de biblioteca: Fallido - URL incorrecta")
            return False

    except Exception as e:
        evidencias.append(f"Acceso al catálogo de biblioteca: Fallido - {str(e)}")
        return False

# METODO REALIZAR BUSQUEDA
def realizar_busqueda(driver):
    global ruta_Reporte
    evidencias.append("Paso: 4")
    evidencias.append("Fecha y hora: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        # Esperar a que el campo de búsqueda esté presente
        campo_busqueda = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "translControl1"))
        )

        # Limpiar el campo de búsqueda por si acaso
        campo_busqueda.clear()

        # Ingresar el término de búsqueda
        campo_busqueda.send_keys("Python")

        # Encontrar y hacer clic en el botón de búsqueda
        boton_busqueda = driver.find_element(By.ID, "searchsubmit")
        boton_busqueda.click()

        # Esperar a que los resultados se carguen (esperamos el elemento que muestra el número de resultados)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "numresults"))
        )

        # Esperar un momento adicional para asegurar que la página se renderice completamente
        time.sleep(3)

        # Tomar la captura de pantalla
        driver.save_screenshot(os.path.join(ruta_Reporte, "paso4.png"))
        evidencias.append("Búsqueda realizada: Correcto")
        return True

    except Exception as e:
        evidencias.append(f"Búsqueda realizada: Fallido - {str(e)}")
        driver.save_screenshot(os.path.join(ruta_Reporte, "paso4_error.png"))
        return False

    except Exception as e:
        evidencias.append(f"Búsqueda realizada: Fallido - {str(e)}")
        return False

# METODO VERIFICAR RESULTADOS
def verificar_resultados(driver):
    global ruta_Reporte
    evidencias.append("Paso: 5")
    evidencias.append("Fecha y hora: " + time.strftime("%Y-%m-%d %H:%M:%S"))
    try:
        # Esperar a que el elemento con los resultados esté presente
        resultados_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "numresults"))
        )

        # Obtener el texto del elemento
        texto_resultados = resultados_elemento.text

        # Verificar si hay resultados usando el texto
        if "resultados" in texto_resultados.lower():
            # Extraer el número de resultados
            numero_resultados = int(''.join(filter(str.isdigit, texto_resultados.split()[3])))
            evidencias.append(f"Número de resultados encontrados: {numero_resultados}")

            # Tomar captura de pantalla
            driver.save_screenshot(os.path.join(ruta_Reporte, "paso5.png"))
            evidencias.append("Verificación de resultados: Correcto")
            return True
        else:
            evidencias.append("No se encontraron resultados en la búsqueda.")
            driver.save_screenshot(os.path.join(ruta_Reporte, "paso5_sin_resultados.png"))
            return False

    except Exception as e:
        evidencias.append(f"Verificación de resultados: Fallida - {str(e)}")
        return False

# METODO GENERAR REPORTE
def generar_reporte():
    with open(os.path.join(ruta_Reporte, "reporte_prueba.txt"), "w", encoding="utf-8") as archivo:
        archivo.write(f"Desarrollador de la prueba: {desarrollador}\n")
        archivo.write(f"Fecha y hora de inicio: {fecha_inicio}\n")
        archivo.write(f"Fecha y hora de finalización: {fecha_fin}\n")
        archivo.write("\nEvidencias de la prueba:\n")
        for evidencia in evidencias:
            archivo.write(f"- {evidencia}\n")
    print("Reporte de prueba generado correctamente.")

# METODO DE INICIAR EJECUCION
def Ejecutar_prueba_automatizada():
    global fecha_fin
    manejador = iniciar_navegador()
    try:
        acceder_pagina_principal(manejador)
        if not navegar_a_biblioteca(manejador):
            return
        if not seleccionar_biblioteca_especifica(manejador):
            return
        if not realizar_busqueda(manejador):
            return
        if not verificar_resultados(manejador):
            return
    finally:
        cerrar_navegador(manejador)
        fecha_fin = time.strftime("%Y-%m-%d %H:%M:%S")
        generar_reporte()

##############
## PROGRAMA
##############
# INICIO EJECUCION DEL PROGRAMA EN PYTHON
if __name__ == "__main__":
    configurar_desarrollador()
    Ejecutar_prueba_automatizada()