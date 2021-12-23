from selenium import webdriver
from selenium.webdriver.common import keys
import json
import random

#Vereinfachte Schreibweisen
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys #zB ESC oder Enter fürs abschicken
import time #Cooldown zw. den Likes => Blocking
from ConfigLoader import Config

class Instabot():
    def __init__(self, username, password): #Konstruktor
        self.username = username
        self.password = password

        #Browser Objekt (startet kl. Chrome Browser und führt alle Sache da drin aus)
        self.browser = webdriver.Chrome("./chromedriver.exe")
        self.config = Config()

        #Anzahl der Likes und Comments heute
        self.liked_count = 0
        self.commented_count = 0

    def WaitForObject(self, type, string):
        return WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((type, string)))

    def WaitForObjects(self, type, string):
        return WebDriverWait(self.browser, 3).until(EC.presence_of_all_elements_located((type, string)))
    
    #Login Funktion
    def login(self):
        self.browser.get("https://instagram.com/accounts/login") #Zeige diese Seite an

        login_objects = self.WaitForObjects(By.CSS_SELECTOR, "input._2hvTZ.pexuQ.zyHYP") #Holen uns die Inputs mit Classes von Insta Seite => in Array (2 Inputs)

        cookieFenster = self.WaitForObject(By.CSS_SELECTOR, "button.aOOlW.bIiDR").click()   
        login_objects[0].send_keys(self.username)
        login_objects[1].send_keys(self.password)
        #login_objects[0].send_keys(keys.ENTER)
        time.sleep(1)
        loginButton = self.WaitForObjects(By.CSS_SELECTOR, "button.sqdOP.L3NKy.y3zKF")
        loginButton[0].click()
        time.sleep(3)
        LoginSpeichernFenster = self.WaitForObject(By.CSS_SELECTOR, "button.sqdOP.yWX7d.y3zKF").click()
        benachFenster = self.WaitForObject(By.CSS_SELECTOR, "button.aOOlW.HoLwm").click()

    #Fotos sammeln
    def collect_photos(self, hashtag):
        self.browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")

        self.browser.execute_script("window.scrollTo(0, 4000)") #Weiter scrollen um weitere Bilder zu laden
        all_photos = self.WaitForObjects(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")
        all_links = []

        for photo in all_photos:
            link = photo.find_element_by_css_selector('a').get_attribute('href')
            all_links.append(link)
            print("Collected {} Links." .format(len(all_links)))
            self.filter_list(all_links)
            

    #Filtern um nur neue Links zu enthalten
    def filter_list(self, links):
        liked_photos = self.read_liked_photos()
        self.filtered_links = []
        for link in links:
            if link in liked_photos:
                continue #Wenn der schon im geliked vorhanden ist
            self.filtered_links.append(link) #Ansonsten füge hinzu
        
        print("{} Links left after Filtering.." .format(len(self.filtered_links)))

    #Gebe die Liste mit "liked" zurück
    def read_liked_photos(self):
        with open("liked.json") as file:
            data = json.load(file)
        return data["liked"]

    #Nächste "liked" link hinzufügen
    def save_liked_photos(self, link):
        with open("liked.json") as oldfile:
            data = json.load(oldfile)
        data["liked"].append(link)
        with open("liked.json", "w+") as newfile:
            json.dump(data, newfile, indent = -4)

    #Routine: liken, kommentieren und sleep
    def bot_routine(self, comments = False):
        for photo in self.filtered_links:

            #Wenn 100 noch nicht erreicht ist
            if self.liked_count < self.config.likestoday:
                self.browser.get(photo)

                time.sleep(random.randint(2, 5))
                gefaelltMir = self.WaitForObjects(By.CSS_SELECTOR, "[aria-label='Gefällt mir']")
                gefaelltMir[1].click()
                self.liked_count += 1
                self.save_liked_photos(photo)

                #Wenn man kommentieren soll
                if comments:
                    time.sleep(random.randint(3, 6))
                    if self.commented_count < self.config.commentstoday:
                        commentbox = self.WaitForObject(By.CLASS_NAME, "Ypffh")
                        commentbox.click()
                        commentbox = self.WaitForObject(By.CLASS_NAME, "Ypffh")
                        commentbox.clear()
                        commentbox.send_keys(self.config.random_comment())
                        commentbox.send_keys(Keys.ENTER)
                        self.commented_count += 1
                        time.sleep(random.randint(3, 5))
                
                time.sleep(random.randint(10, 80))


Bot = Instabot("testbot_chn", "WoJiaoChina1803%%")
Bot.login()
Bot.collect_photos(Bot.config.random_hashtag())
Bot.bot_routine(True)