from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import re
from unicodedata import normalize
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


filepath = "whatsapp_session.txt"
driver = webdriver


def crear_driver_session():

    with open(filepath) as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)
                
    org_command_execute = RemoteWebDriver.execute

    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver



def check_mensajes(chat):
    
    try:
        numMens = chat.find_element(By.CLASS_NAME,"_1pJ9J").text
        
        msLeer = re.findall('\d+', numMens)
        
        if len(msLeer) !=0:
            pending = True
            
        else:
            pending = False
            
            
    except:
        pending = False
        
    return pending



def buscar_chats():
    print("BUSCANDO CHATS")
    sleep(2)
    
    print(len(driver.find_elements(By.CLASS_NAME,"_1RAKT")))
    # si la longitud es 0 es porque tengo chat abierto, si es dif de 0 es porque no hay chat abierto
    if len(driver.find_elements(By.CLASS_NAME,"zaKsw")) == 0: #cuando ninguno esta abierto (ventana de la derecha)
        
        print("CHAT ABIERTO")
        message = identificar_mensaje()
                                
        if message != None:
            return True
    else:
        
        chats = driver.find_elements(By.CLASS_NAME,"_1Oe6M") # el cuadro del primer chat a la izquierda
                
        #print("len chats: ",len(chats))
        for chat in chats:
            print("DETECTANDO chats")
            print("mensajes sin leer: ",len(chats))


            porresponder = check_mensajes(chat) # Verificar si existen mensajes por leer
            
            # Condicion para entrar en cada conversacion (Solo entra si existen mensajes sin leer)
            if porresponder:
                
                # Si existen mensajes sin responder debemos dar click sobre ese chat.            
                chat.click()  # Se da click sobre la conversacion.
                sleep(2)
                return True
            else:
                print("CHATS ATENDIDOS")
                continue
                

    return False



def normalizar(message: str):
    message = re.sub(r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
                    normalize("NFD", message), 0, re.I)
    
    return normalize('NFC', message)


def identificar_mensaje():
    
    element_box_message = driver.find_elements(By.CLASS_NAME,"_27K43")
    
    posicion = len(element_box_message) -1
    
    element_message = element_box_message[posicion].find_elements(By.CLASS_NAME, "_21Ahp")
    
    message = element_message[0].text.lower().strip()
    print("MENSAJE RECIBIDO:", message)
    
    return normalizar(message)


def preparar_respuesta(message: str):
    print("PREPARANDO LA RESPUESTA")
    
    response = bot(message)
    enviar_respuesta(response)
    #return responses

def enviar_foto(foto: str):
    try:
        print("Intentando enviar foto:", foto)
        # Hacer clic en el icono de adjuntar en el chat de WhatsApp
        attach_icon = WebDriverWait(driver, timeout=3).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span'))
        attach_icon.click()
        
        # Seleccionar la opción de adjuntar imagen en la ventana emergente
        file_input = WebDriverWait(driver, timeout=10).until(lambda driver: driver.find_element(By.XPATH, '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]'))
        file_input.send_keys(foto)
        
        # Hacer clic en el botón de enviar imagen
        send_button = WebDriverWait(driver, timeout=10).until(lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]'))
        send_button.click()
        
        # Esperar 1 segundo y cerrar la ventana emergente
        time.sleep(1)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
        print("Foto enviada exitosamente!")
        
    except TimeoutException:
        print("Error: No se pudo encontrar el elemento en el tiempo de espera")
        
    except ElementNotInteractableException:
        print("Error: Elemento no interactuable")
        
    except Exception as e:
        print("Error inesperado:", e)


def enviar_sticker(sticker: str):
    print("sticker :", sticker)
    WebDriverWait(driver, timeout= 3).until(lambda driver: driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[1]/button[2]')).click()
    sleep(1)
    WebDriverWait(driver, timeout= 3).until(lambda driver: driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[1]/button[4]')).click()
    WebDriverWait(driver, timeout= 3).until(lambda driver: driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[2]/div/div[3]/div/div/div[1]/div/div[3]')).click()
    sticker_path = '//*[@id="main"]/footer/div[2]/div/div[3]/div/div/div[2]/div[2]/div/div/div/div[{}]'.format(sticker)
    #print("sticker_path :", sticker_path)
    sleep(2)
    WebDriverWait(driver, timeout= 3).until(lambda driver: driver.find_element(By.XPATH, sticker_path)).click()
    #Cierra
    WebDriverWait(driver, timeout= 3).until(lambda driver: driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[1]/button[1]')).click()
    sleep(1)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()


def enviar_respuesta(respuesta: str):
    chatbox = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    res = ''.join(respuesta)
    if res.startswith("foto_"):
        enviar_foto(res.replace('foto_',''))
    elif res.startswith("sticker_"):
        enviar_sticker(res.replace('sticker_',''))
    else:
        print("respuesta : ", respuesta)
        chatbox.send_keys(respuesta, Keys.ENTER)
        sleep(2)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

def procesar_mensaje(message: str):
    chatbox = driver.find_element(By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    
    preparar_respuesta(message)
    #print("RESPONSE:", response)
    
    #chatbox.send_keys(response, Keys.ENTER)
    #sleep(2)
    #webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    
    
    
def whatsapp_bot_init():
    global driver
    driver = crear_driver_session()

    esperando=1
    
    while esperando== 1:
        esperando=len(driver.find_elements(By.CLASS_NAME,"_1meIt"))
        sleep(5)
        print("login_sucess: ", esperando)
        
    while True:
        if not buscar_chats(): # busca si hay chats, y si tienen mensajes sin leer
            sleep(5)

            # aqui debo hacer un control para que retroceda atras donde no hay chats abiertos
            # y lo vamos a hacer regrescando la pagina
            continue
        
        message = identificar_mensaje()

        if message == None:
            continue
        else:
            procesar_mensaje(message)
            
            
            
            
from keep_session import start_keep_session
from chatbot import bot


if __name__ == '__main__':
    start_keep_session()
    sleep(4)
    whatsapp_bot_init()