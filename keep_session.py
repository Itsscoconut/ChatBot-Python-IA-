from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By



#from webdriver_manager.microsoft import EdgeChromiumDriverManager

#driver = webdriver.Edge(EdgeChromiumDriverManager().install())


edge_path = 'driver/msedgedriver'
service = Service(executable_path=edge_path)
driver = webdriver.Edge(service = service)
# conexion con web.whatsapp a traves del driver usando selenium
#driver = webdriver.Edge(executable_path='msedgedriver.exe') #./
executor_url = driver.command_executor._url
session_id = driver.session_id
driver.get("https://web.whatsapp.com/")
print("Session ID 1: " + session_id)
print("Executor URL: " + executor_url)

with open("./whatsapp_session.txt", "w") as text_file:
    text_file.write("{}\n".format(executor_url))
    text_file.write(session_id)


def new_command_execute(self, command, params=None):
        if command == "newSession":
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

def create_driver_session(session_id, executor_url):
    from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

    org_command_execute = RemoteWebDriver.execute
    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver

def start_keep_session():
        driver2 = create_driver_session(session_id, executor_url)
        print("Driver 2 URL: " + driver2.current_url)

# _________________________________MAIN________________________

# Driver program
if __name__ == '__main__':
    start_keep_session()
    
    
    
    
    
    
    
    
