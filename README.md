# Kronos To Calendar

Web scraper in python that accesses Kronos' workforce management web-app via selenium and harvests your working hours in order to add your work
schedule to Google Calendar using Google's API.

While this was incredibly useful while I used Kronos WFM, it is currently obsolete, I don't plan on updating this as I no longer using Kronos.

## How to use:

- Add your Google Calendar credentials.json to the programs directory.
- Create a config.py, replacing the values in the example config.py with your own.
- The included web drivers are for Chrome V89, feel free to replace them with your own.
- Run main.py once to authenticate and generate a token, then run it on a schedule, ideally daily.
- For bonus points make sure your Google Calendar is synched to your phone.
