from bs4 import BeautifulSoup
import PySimpleGUI as sg
import datetime
import pygame
from plyer import notification
import time
import os
import multiprocessing
import requests
import json
from PIL import Image, ImageDraw
import pystray

sg.theme("SystemDefault")

def play_azan(name):
    pygame.mixer.init()
    pygame.mixer.music.load('azan1.mp3')
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()
    title = name
    message = f'Time to Pray {name}'
    notification.notify(title=title, message=message, timeout=10)
    time.sleep(120) 
    pygame.mixer.music.stop()
    pygame.mixer.quit()

def get_state_country():
    layout = [
        [sg.Text("Enter State: "), sg.InputText(key="state")],
        [sg.Text("Enter Country: "), sg.InputText(key="country")],
        [sg.Button("Submit", key='Submit')]
    ]

    window = sg.Window("State and Country Input", layout, icon='minaret_prayer_call_sound_islam_adzan_icon_251083.ico')
    
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == "Submit":
            try:
                window.close()
                state = values["state"]
                country = values["country"]
                locations = {"state" : state, "country" : country}
                with open("location.json", 'w') as file:
                    json.dump(locations, file)
                if state and country:
                    url = f"https://aladhan.com/play/{state}/{country}"        
                return url
            except UnboundLocalError:
                print("Error")
                return get_state_country()
            
''' creating the system icon '''
def create_image(width, height, color2):
    # Generate an image and draw a pattern
    image = Image.open('minaret_prayer_call_sound_islam_adzan_icon_251083.png')
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height),fill=color2)
    return image

def on_clicked(icon, item):
    # Execute different actions based on the menu item text
    if item.text == 'Edit location':
        return get_state_country()
    elif item.text == 'Close':
        icon.stop()
    elif item.text == 'times':
        try:
            scraper = Praying_times_scraper(url=f"https://aladhan.com/play/{file['state']}/{file['country']}")
            scraper.small_popup_window()
        except TypeError:
            scraper = Praying_times_scraper(url=get_state_country())
            scraper.small_popup_window()
# Create the menu items
menu_items = [
    pystray.MenuItem("times", lambda icon, item: on_clicked(icon, item)),
    pystray.MenuItem('Edit location', lambda icon, item: on_clicked(icon, item)),
    pystray.MenuItem('Close', lambda icon, item: on_clicked(icon, item))
]

icon = pystray.Icon('Prayer Times', create_image(64, 64, 'black'), 'Prayer Times', menu_items)

class Praying_times_scraper:
    def __init__(self, url):
        self.url = url                
    
    def small_popup_window(self):
        url = requests.get(self.url)
        soup = BeautifulSoup(url.content, 'html.parser')

        prayer = {}

        prayer_names = soup.find_all('dt')
        prayer_times = soup.find_all('dd')

        for name, time in zip(prayer_names, prayer_times):
            prayer[name.text] = time.text

        prayer_display = []

        for name, time in prayer.items():
            prayer_display.append([sg.Text(name, key=name, font=('Helvetica', 10, 'bold')), 
                                   sg.Text(time, key=time, 
                                           font=('Helvetica', 10, 'bold'))])
            

        pray_frame = [
            [sg.Text("Current Time", font=('Helvetica', 10, 'bold')), sg.Text("", key='time_now', font=('Helvetica', 10, 'bold'))],
            [sg.Frame("Prayer Times", layout=prayer_display)],
        ]


        screen_width, screen_height = sg.Window.get_screen_size()
        
        window = sg.Window("", pray_frame, grab_anywhere=False, location=(int(screen_width-200), screen_height-320),no_titlebar=False,
                           icon='minaret_prayer_call_sound_islam_adzan_icon_251083.ico')

        bg_process = multiprocessing.Process(target=play_azan, args=("Prayer Name",))
        bg_process.daemon = True
        
        while True:
            event, value = window.read(timeout=1000)
            if event == sg.WINDOW_CLOSED:
                return icon
            time_now = datetime.datetime.now().strftime('%H:%M')
            window['time_now'].update(time_now)
            for name, time_text in prayer.items():
                prayer_time = datetime.datetime.strptime(time_text, '%H:%M').time()
                current_time = datetime.datetime.strptime(time_now, '%H:%M').time()
                if prayer_time == current_time:
                    bg_process.start()
                    window[name].update(text_color="red")
                    window[time_text].update(text_color="red")
                    play_azan(name)
                    return True
                elif prayer_time > current_time:
                    window[name].update(text_color="green")
                    window[time_text].update(text_color="green")
                else:
                    window[name].update(text_color="red")
                    window[time_text].update(text_color="red")

if __name__ == "__main__":
    if os.path.isfile('location.json'):
        with open('location.json', 'r') as file:
            file = json.load(file)
        scraper = Praying_times_scraper(url=f"https://aladhan.com/play/{file['state']}/{file['country']}")
    else:
        scraper = Praying_times_scraper(url=get_state_country())
    icon.run()
