#Tema: Prediccion de precios de Casas
#Nombre : Michael Kevin Rivas Jimenez
#Carrera :  Ing. Sistemas
import requests
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import io

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36") #Agente generado para reemplazar en la cabezera el valor por defecto "Robot"
opts.add_argument("--no-sandbox") #
opts.add_argument("--no-default-browser-check") #
opts.add_argument("--no-first-run") #
opts.add_argument("--disable-blink-features=AutomationControlled") #
opts.add_argument("--headless") #para que no se vea la ventana al ejecutarse

headers = {
    "user-agent": "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
}
URL_inicio="https://www.infocasas.com.bo/venta/casas"
paginas=30
lista_Paginas=[]
for x in range(20,paginas):
    URL_x = URL_inicio + "/pagina"+str(x)
    lista_Paginas.append(URL_x)

lista_DOMs_Casas=[]

for lista_casas in lista_Paginas:
    pagina = requests.get(lista_casas, headers=headers)
    lista_DOMs_Casas.append(pagina)

lista_URLs_paginas = []
for dom in lista_DOMs_Casas:
    sleep(randint(2,5))
    soup = BeautifulSoup(dom.text)
    casas = soup.find_all('a', class_="lc-cardCover")
    for casa in casas:
         lista_URLs_paginas.append("https://www.infocasas.com.bo"+casa.get('href'))

for link in lista_URLs_paginas:
    sleep(randint(3,6)) #Para realizar peticiones de forma aleatoria y evitar ser detectados como robots
    try:
        driver = webdriver.Chrome('./chromedriver', chrome_options=opts) #Se carga el driver con las configuraciones para Chrome para utilizar selenium en Chrome
        driver.get(link) # Inicia y Carga el DOM
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

        driver.quit()
        data= str(referencia)+";"+ str(titulo)+";"+str(estado_casa)+";"+str(ubicacion)+";"+str(anio)+";"+str(habitaciones)+";"+str(banios)+";"+str(m2Terreno)+";"+str(nroPlantas)+";"+str(m2Edificados)+";"+str(garajes)+";"+str(precio)+"\n"
        print(data)
        with io.open("scraping_casas.csv", "a", encoding="utf8") as f1:
            f1.write(data)
            f1.close()
    except Exception as e:
        print(e)
