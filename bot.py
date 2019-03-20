# -*- coding: utf-8 -*-
# Copyright: Sampo Pelto 2019

from telegram import Bot
from time import gmtime, strftime
from configparser import ConfigParser
import pyowm
from bs4 import BeautifulSoup
import requests
import re


def send(bot, msg, chat_id):
    bot.send_message(chat_id=chat_id, text=str(msg))


def pvm():
    return strftime("Tänään on %d.%m. ", gmtime())


def saa(owm):
    observation = owm.weather_at_place('Tampere,FI')
    w = observation.get_weather()

    condition = str(w).split('status=')[1][:-1].lower().split(",")[0]
    keli = condition

    temperature = str(int(w.get_temperature('celsius')['temp'])) + "°C"

    if condition == "clouds":
        keli = "Pilvistä"
    elif condition == "fog":
        keli = "Sumuista"
    elif condition == "snow":
        keli = "Lumista"
    elif condition == "snow":
        keli = "Vetistä"
    elif condition == "clear":
        keli = "Aurinkoista"
    else:
        keli = condition

    return f"Sää: {keli} ja {temperature}. "


def nimi():
    urli = "https://www.nimipaivat.fi"

    soup = BeautifulSoup(requests.get(urli).content, "html.parser")

    kokonainen = str(soup.find('table'))
    nimet = re.findall(r'>([a-zA-Z]*)<\/a>', kokonainen)
    
    if len(nimet) > 1:
        return "Nimipäivät: " + ", ".join(nimet)
    elif len(nimet) == 0:
        return "Nimipäivä: " + ", ".join(nimet)
    return "Ei nimipäiviä!" 


def liputus():

    urli = "https://www.xn--liputuspivt-s8ac.fi/"

    soup = BeautifulSoup(requests.get(urli).content, "html.parser")

    return "Liputuspäivä: " + str(soup.find('h2')).split(">")[1].split("</")[0]


def main():

    cfg = ConfigParser()
    cfg.read('env.cfg')

    bot = Bot(token=cfg['TELEGRAM']['token'])
    chat_id = cfg['TELEGRAM']['id']
    owm = pyowm.OWM(cfg['PYOWM']['token'])

    viesti = pvm() + "\n" + saa(owm) + "\n" + \
             nimi() + "\n" + liputus()

    send(bot, viesti, chat_id)
    print(viesti)


if __name__ == "__main__":
    main()
