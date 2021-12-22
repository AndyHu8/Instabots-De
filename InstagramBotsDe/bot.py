from selenium import webdriver
from selenium.webdriver.common import keys

#Vereinfachte Schreibweisen
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys #zB ESC oder Enter fürs abschicken
import time #Cooldown zw. den Likes => Blocking

class Instabot():
    def __init__(self, username, password): #Konstruktor
        self.username = username
        self.password = password

        #Browser Objekt (startet kl. Chrome Browser und führt alle Sache da drin aus)
        self.browser = webdriver.Chrome("./chromedriver.exe")

    def WaitForObject(self, type, string):
        return WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((type, string)))

    def WaitForObjects(self, type, string):
        return WebDriverWait(self.browser, 3).until(EC.presence_of_all_elements_located((type, string)))
    
    #Login Fkt.
    def login(self):
        self.browser.get("https://instagram.com/accounts/login") #Zeige diese Seite an

        login_objects = self.WaitForObjects(By.CSS_SELECTOR, "input._2hvTZ.pexuQ.zyHYP") #Holen uns die Inputs mit Classes von Insta Seite => in Array (2 Inputs)

        cookieFenster = self.WaitForObject(By.CSS_SELECTOR, "button.aOOlW.bIiDR").click()   
        login_objects[0].send_keys(self.username)
        login_objects[1].send_keys(self.password)
        #login_objects[0].send_keys(keys.ENTER)
        loginButton = self.WaitForObjects(By.CSS_SELECTOR, "button.sqdOP.L3NKy.y3zKF")
        loginButton[0].click()
        time.sleep(3)
        LoginSpeichernFenster = self.WaitForObject(By.CSS_SELECTOR, "button.sqdOP.yWX7d.y3zKF").click()
        benachFenster = self.WaitForObject(By.CSS_SELECTOR, "button.aOOlW.HoLwm").click()

    def search_hastag(self, hashtag):
        self.browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")

        self.browser.execute_script("window.scrollTo(0, 4000)") #Weiter scrollen um weitere Bilder zu laden
        all_photos = self.WaitForObjects(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")
        for photo in all_photos:
            photo.click()
            gefaelltMir = self.WaitForObjects(By.CSS_SELECTOR, "[aria-label='Gefällt mir']")
            gefaelltMir[1].click()
            self.WaitForObject(By.CSS_SELECTOR, "[aria-label='Schließen']").click()
            time.sleep(5)

Bot = Instabot("testbot_chn", "WoJiaoChina1803%%")
Bot.login()
Bot.search_hastag("china")