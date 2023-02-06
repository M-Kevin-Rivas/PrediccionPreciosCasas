#Tema: Prediccion de precios de Casas
#Nombre : Michael Kevin Rivas Jimenez
#Carrera :  Ing. Sistemas

import requests #util para realizar peticiones y recuperar el html directamente del servidor en una peticion hacia este
from bs4 import BeautifulSoup #util para parsear el codigo html y poder obtener la informacion
from random import randint #necesario para generar tiempos de aleatorios
from time import sleep #se combina con la libreria anterior para que las peticiones hacia al servidor tengan un tiempo de espera antes de obtener el codigo html
from selenium import webdriver #util para simular el comportamiento humano y obtener codigo html de paginas web dinamicas
from selenium.webdriver.common.by import By #ayuda a definir que tipo de lenguaje de expresion se usara para obtener los datos de nodos especificos en codigo html
from selenium.webdriver.chrome.options import Options #utilizado para colocar argumentos en la cabezera de peticiones al servidor para quitar valores por defecto que indican que se esta usando agentes o software que recolectan datos
import io #necesaria para guardar los resultados del scraping en un archivo que se utilizara posteriormente

#Opciones de Chome
#Se plican cuando se utiliza Selenium
#Son parametros que permiten modificar el comportamiento al inicializar el navegador Chrome en modo de prueba cada vez que realiza la peticion al servidor
#Son utiles para optimizar y evitar problemas en las solicitudes al servidor
opts = Options()

#En la peticion al srvidor en el encabezado especificamente colocamos el "User-Agent" para las solicitudes HTTP y no este por defecto en "Robot"
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36") #Agente generado para reemplazar en la cabezera el valor por defecto "Robot"

#Deshabilita el espacio aislado para todos los tipos de procesos que normalmente están aislados
opts.add_argument("--no-sandbox") 

#Evita el aviso de que Chorme no es el navegador por defecto
opts.add_argument("--no-default-browser-check") 

#Omita las tareas de la primera ejecución en Chrome, independientemente de si es o no la primera ejecución, haciendo que arranque un poco mas rapido
opts.add_argument("--no-first-run")

#Esta opcion hace que la variable "navigator.webdriver" indique false que significa que los sistemas antibots cuando lo lean
#Haciendo que Selenium no sea detectado en las peticiones
opts.add_argument("--disable-blink-features=AutomationControlled")

#Ejecuta Chrome en modo headless, es decir, sin una interfaz de usuario o dependencias del servidor de visualización
#Haciendo que sea mas rapido en el scraping y reduciendo errores de visualizacion
opts.add_argument("--headless") 


#En esta seccion del codigo obtenemos los links de las paginas de casas en venta para hacer el web scraping a cada una de ellas

#Aplicamos la libreria request, porque la informacion de las paginas que se requiere esta en el codigo html y es mas rapido que Selenium
#Volvemos a defirnir el "user-agent" para las peticiones con la libreria request, que es muy aparte las peticiones con Selenium
headers = {
    "user-agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
#Inicializamos con la URL Semilla de donde generaremos las paginas para recolectar los links de paginas de casas en venta
#En esta URL se encuentra la lista de ventas de casas y que puede redireccionar a una pagina en detalle de la venta de una casa en especifica
URL_inicio="https://www.infocasas.com.bo/venta/casas" 

paginas=51 #Cantidad de paginas a recorrer desde la URL semilla para obtener las listas de casas en venta, el numero es la cantidad de paginas que tiene el sitio web
#Creamos una lista donde generamos las URLs con todas las lista de casas en venta por pagina que se van añadiendo a la lista
lista_Paginas=[]
for x in range(1,paginas):
    URL_x = URL_inicio + "/pagina"+str(x)
    lista_Paginas.append(URL_x)

#A paritr de la anterior lista generamos una nueva lista donde se guardaran los links especificos de cada anuncio de una venta especifica
lista_DOMs_Casas=[]
#Aplicamos la funcion "requests" para realizar la peticion al servidor y obtener los html de las paginas que contienen las listas de ventas de casas
for lista_casas in lista_Paginas:
    sleep(randint(2,5)) #Tiempo de espera entre 2 y 5 segundo para las peticiones y evitar que consideren un bot
    pagina = requests.get(lista_casas, headers=headers) #Recuperamos el codigo html
    lista_DOMs_Casas.append(pagina) #y lo guardamos en la lista

#A partir de la lista anterior empezamos a recolectar las URLs de las paginas en detalle individual de cada ventas de casas
lista_URLs_paginas = []
#Recorriendo y parseando el HTML recuperado en la iteracion anterior, obtenemos 
for dom in lista_DOMs_Casas:
    soup = BeautifulSoup(dom.text) #parseamos el codigo HTML
    casas = soup.find_all('a', class_="lc-cardCover") #buscamos dentro del DOM en la etiqueta a con el atributo "lc_cardCover"
    for casa in casas:
         lista_URLs_paginas.append("https://www.infocasas.com.bo"+casa.get('href')) #Recuperamos y completamos el link de una pagina de detalle de una venta de una casa

#En esta seccion empieza el scraping con Selenium

#creamos un archivo con el nombre "scraping_casas.csv", el parametro "a" para que añada sobre lo que tenga y no lo sobrescriba y generarlo en formato UTF-8
with io.open("scraping_casas.csv", "a", encoding="utf8") as f1:
    #Al crear, la primera fila tendra el nombre de las columnas o variables que se obtienen en el scraping
    f1.write("referencia;titulo_anuncio;estado_casa;ubicacion;año_construccion;nro_baños;m2_terreno;nro_plantas;m2_edificados;nro_garajes;precio_venta\n")

#A partir de la lista generada con los links individuales de cada pagina del detalle de una venta de casa en particular se realiza el scraping
for link in lista_URLs_paginas:
    sleep(randint(3,6)) #Para realizar peticiones con un timepo de espera entre 3 y 6 segundo y evitar ser detectados como robots
    #Colocamos las peticiones en un bloque try-expect en caso de que no se cargara la pagina y no se rompa el codigo
    try:
        driver = webdriver.Chrome('./chromedriver', chrome_options=opts) #Se carga el driver con las configuraciones para Chrome para utilizar selenium en Chrome
        driver.get(link) # Inicia y carga el DOM de la pagina dinamica de una venta de casa en especifico 
        #A partir de este punto se recolecta de forma especifica las variables de interes
        #Cada una esta en un bloque try-except, esto es debido a que puede darse el caso de que no se cargue ese parte en el DOM y genere un error, asi pues se evita que se rompa el codigo y siga recolectando
        try:
            habitaciones = driver.find_element(By.XPATH,'//div[contains(@class,"technical-sheet")]/div[11]/div[3]/*').text
            print("nro habitaciones: "+str(habitaciones))
        
        except:
            habitaciones = None
            print("nro habitaciones: "+str(habitaciones))

        try:
            banios= driver.find_element(By.XPATH,'//div[contains(@class,"technical-sheet")]/div[6]/div[3]/*').text
            print("nro de banios: "+str(banios))
        except:
            banios= None
            print("nro de banios: "+str(banios))

        try:
            m2Terreno= driver.find_element(By.XPATH,'//div[contains(@class,"technical-sheet")]/div[9]/div[3]/*').text
            print("m2Terreno: "+str(m2Terreno))
        except:
            m2Terreno= None
            print("m2Terreno: "+str(m2Terreno))
    
        try:
            nroPlantas= driver.find_element(By.XPATH,'//div[contains(@class,"technical-sheet")]/div[13]/div[3]/*').text
            print("nro de plantas: "+str(nroPlantas))
        except:
            nroPlantas= None
            print("nro de banios: "+str(nroPlantas))
    
        try:
            m2Edificados= driver.find_element(By.XPATH,'//div[contains(@class,"technical-sheet")]/div[7]/div[3]/*').text
            print("m2 Edificados: "+str(m2Edificados))
        except:
            m2Edificados= None
            print("m2 Edificados: "+str(m2Edificados))
    
        try:
            garajes= driver.find_element(By.XPATH,'//div[@class="jsx-952467510 technical-sheet"]/div[12]/div[3]/*').text
            print("nro de garajes: "+str(garajes))
        except:
            garajes= None
            print("nro de garajes: "+str(garajes))
        
        try:
            referencia = driver.find_element(By.XPATH,'//div[contains(@class,"technical-sheet")]/div[1]/div[3]/*').text
            print("referencia: "+str(referencia))
    
        except:
            referencia = None
            print("nro habitaciones: "+str(referencia))

        try:
            estado_casa= driver.find_element(By.XPATH,'//div[contains(@class,"technical-sheet")]/div[4]/div[3]/*').text
            print("Estado de la casa: "+str(estado_casa))
    
        except:
            estado_casa = None
            print("Estado de la casa: "+str(estado_casa))

        try:
            anio= driver.find_element(By.XPATH,'//div[contains(@class,"technical-sheet")]/div[10]/div[3]/*').text
            print("año: "+str(anio))
    
        except:
            referencia = None
            print("año: "+str(anio))

        try:
            ubicacion= driver.find_element(By.XPATH,'//span[@class="ant-typography property-location-tag"]').text
            print("ubicacion: "+str(ubicacion))
    
        except:
            ubicacion= None
            print("ubicacion: "+str(ubicacion))

        try:
            precio= driver.find_element(By.XPATH,'//span[@class="ant-typography price"]').text
            print("precio: "+str(precio))
    
        except:
            precio= None
            print("precio: "+str(precio))

        try:
            titulo= driver.find_element(By.XPATH,'//h1[@class="ant-typography property-title"]').text
            print("titulo: "+str(titulo))
    
        except:
            precio= None
            print("titulo: "+str(titulo))
        
        #por cada peticion y recoleccion de pagina creamos una peticion iniciando Chrome, para que no se sature, se finaliza  con esta opcion
        driver.quit()
        
        #Genereamos una cadena con las variables que obtenimos en el scraping que estan sepradas por ";"
        data= str(referencia)+";"+ str(titulo)+";"+str(estado_casa)+";"+str(ubicacion)+";"+str(anio)+";"+str(habitaciones)+";"+str(banios)+";"+str(m2Terreno)+";"+str(nroPlantas)+";"+str(m2Edificados)+";"+str(garajes)+";"+str(precio)+"\n"
        print(data)
        
        #Guardamos la cadena en el archivo previamente creado
        with io.open("scraping_casas.csv", "a", encoding="utf8") as f1:
            f1.write(data)
            f1.close()
    #En caso de que no se carge la pagina simplemente seguira con la ejecucion con la siguiente
    except Exception as e:
        print(e)
