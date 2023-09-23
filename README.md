Prayer Times Application

This application uses Python to display prayer times based on location and provide notifications for prayer times.

Dependencies
BeautifulSoup (bs4)
PySimpleGUI (PySimpleGUI)
Pygame (pygame)
Plyer (plyer)
Requests (requests)
PIL (Pillow - Python Imaging Library)
PyStray (pystray)


Usage

Run the script to start the application.
If a location is not set, a window will prompt for the state and country. Fill in the details and click "Submit."
The application will display the current time and prayer times. The prayer times will change color based on whether they are upcoming or have passed.
When it's time for a prayer, the application will play the Azan (call to prayer) and display a notification.
Functionality
The play_azan function plays the Azan, displays a notification, and stops the Azan after a set time.
The get_state_country function prompts the user to enter the state and country and stores the location in a JSON file.
The create_image function generates an image for the system tray icon.
The on_clicked function handles actions when the system tray icon menu items are clicked.
The Praying_times_scraper class scrapes prayer times from a specified URL and displays them in a window. It also triggers the Azan and updates the display based on prayer times.


Notes

Prayer times are scraped from the "aladhan.com" website.
The application uses a system tray icon to provide a simple interface for accessing prayer times and updating the location.
I still Need to work on making the popup from the Viewing the Praying times nicer and cleaner.
I Had start on system startup but windows was flaging it down as a trojan so I removed it.

![Screenshot from 2023-08-22 13-48-04](https://github.com/Moe-Dahan/Azan-Reminder/assets/83793097/6de863a5-7198-40d8-a6c3-470a178a8742)
![Screenshot from 2023-08-22 13-48-16](https://github.com/Moe-Dahan/Azan-Reminder/assets/83793097/5252f9da-bbc1-4515-82c5-1a20ef34ea24)
![Screenshot from 2023-08-22 13-48-30](https://github.com/Moe-Dahan/Azan-Reminder/assets/83793097/4c338a00-9651-4a93-86fa-147befc572b0)
