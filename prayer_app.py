from bs4 import BeautifulSoup
import PySimpleGUI as sg
import datetime
import pygame
from plyer import notification
import time
import os
import shutil
import sys
import multiprocessing
import requests
import json


sg.theme("SystemDefault")

''' adding the program to startup '''
def add_to_startup_windows():
    script_path = os.path.abspath(sys.argv[0])
    startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    target_path = os.path.join(startup_folder, os.path.basename(script_path))
    if not os.path.exists(target_path):
        shutil.copy2(script_path, target_path)

def add_to_startup_macos():
    script_path = os.path.abspath(sys.argv[0])
    startup_folder = os.path.join(os.path.expanduser("~"), 'Library', 'LaunchAgents')
    plist_filename = os.path.basename(script_path).replace('.py', '.plist')
    plist_path = os.path.join(startup_folder, plist_filename)
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>{os.path.basename(plist_filename)}</string>
        <key>ProgramArguments</key>
        <array>
            <string>{sys.executable}</string>
            <string>{script_path}</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
    </dict>
    </plist>
    """
    with open(plist_path, 'w') as plist_file:
        plist_file.write(plist_content)

''' linux startup config '''
def add_to_startup_linux():
    script_path = os.path.abspath(sys.argv[0])
    desktop_path = os.path.join(os.path.expanduser("~"), '.config', 'autostart', os.path.basename(script_path) + '.desktop')
    desktop_content = f"""[Desktop Entry]
    Type=Application
    Exec={sys.executable} {script_path}
    Hidden=false
    NoDisplay=false
    X-GNOME-Autostart-enabled=true
    Name[en_US]={os.path.basename(script_path)}
    Name={os.path.basename(script_path)}
    Comment[en_US]=Your script description
    Comment=Your script description
    """
    with open(desktop_path, 'w') as desktop_file:
        desktop_file.write(desktop_content)


if os.name == 'posix':
    try:
        add_to_startup_linux()
    except OSError:
        add_to_startup_macos()
elif os.name == 'nt':
    add_to_startup_windows()


def play_azan(name):
    pygame.mixer.init()
    pygame.mixer.music.load('azan1.mp3')
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play()
    title = name
    message = f'Time to Pray {name}'
    notification.notify(title=title, message=message, timeout=10)
    time.sleep(120) # make it longer with the pause
    pygame.mixer.music.stop()
    pygame.mixer.quit()


def get_state_country():
        # Create a PySimpleGUI window to get user input
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
            window.close()
            state = values["state"]
            country = values["country"]
            locations = {"state" : state, "country" : country}
            with open("location.json", 'w') as file:
                json.dump(locations, file)
            if state and country:
                url = f"https://aladhan.com/play/{state}/{country}"        
    return url

def gui_process(url):
    url = requests.get(url) # add your state/suburb and country
    soup = BeautifulSoup(url.content, 'html.parser')

    prayer = {}

    prayer_names = soup.find_all('dt')
    prayer_times = soup.find_all('dd')

    prayer_display = [] # to display the output praying times and names

    # Loop through each pair of prayer names and times, and store them in the dictionary
    for name, time in zip(prayer_names, prayer_times):
        prayer[name.text] = time.text
        prayer_display.append([sg.Text(name.text, key=name.text, font=('Helvetica', 10, 'bold')), sg.Text(prayer[name.text], key=prayer[name.text], font=('Helvetica', 10, 'bold'))])

    ''' sets the main gui section here '''
    pray_frame = [
        [sg.Text("Current Time", font=('Helvetica', 10, 'bold')), sg.Text("", key='time_now', font=('Helvetica', 10, 'bold'))],
        [sg.Frame("Prayer Times", layout=prayer_display)]
    ]

    window = sg.Window("", pray_frame, grab_anywhere=True, icon='minaret_prayer_call_sound_islam_adzan_icon_251083.ico', titlebar_icon='adhan-call.png', no_titlebar=True)#'muslim_carpet_prayer_mat_sajadah_icon_251091.ico')

    bg_process = multiprocessing.Process(target=play_azan, args=("Prayer Name",))
    bg_process.daemon = True
    
    while True:
        event, value = window.read(timeout=1000)
        if event == sg.WINDOW_CLOSED:
            break
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

    window.close()

if __name__ == '__main__':
    if os.path.isfile('location.json'):
        with open('location.json', 'r') as file:
            file = json.load(file)
        gui_process(url=f"https://aladhan.com/play/{file['state']}/{file['country']}"  )
    else:
        gui_process(url=get_state_country())
    
