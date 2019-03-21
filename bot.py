# -*- coding: utf-8 -*-
# Copyright: Sampo Pelto 2019

from telegram import Bot
from time import gmtime, strftime
import datetime
from configparser import ConfigParser
import pyowm
from bs4 import BeautifulSoup
from random import choice
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

    return "Sää: {0} ja {1}. ".format(keli, temperature)


def nimi():
    urli = "https://www.nimipaivat.fi"

    soup = BeautifulSoup(requests.get(urli).content, "html.parser")

    kokonainen = str(soup.find('table'))
    nimet = re.findall(r'>([a-zA-Z]*)<\/a>', kokonainen)
    
    if len(nimet) > 1:
        return "Nimipäivät: " + ", ".join(nimet)
    elif len(nimet) == 1:
        return "Nimipäivä: " + ", ".join(nimet)
    return "Ei nimipäiviä!" 


def liputus():

    urli = "https://www.xn--liputuspivt-s8ac.fi/"

    soup = BeautifulSoup(requests.get(urli).content, "html.parser")

    return str(soup.find('h2')).split(">")[1].split("</")[0]


def fakta(d, m):
    kuukausidict = {1: 'tammikuuta', 2: 'helmikuuta', 3: 'maaliskuuta', 4: 'huhtikuuta', 5: 'toukokuuta', 6: 'kesäkuuta', 7: 'heinäkuuta', 8: 'elokuuta', 9: 'syyskuuta', 10: 'lokakuuta', 11: 'marraskuuta', 12: 'joulukuuta'}

    urli = "https://fi.m.wikipedia.org/wiki/" + str(d) + "._" + kuukausidict[m]

    soup = BeautifulSoup(requests.get(urli).content, "html.parser")

    lista = []
    a = soup.prettify()
    a = a.split("Tapahtumia")[3].split('id="Syn')[0]
    a = a.replace("</li>", "??!!??")
    a = re.sub('\s+', ' ', re.sub(r'<.*?>', "", a))
    a = a.replace("<span", "").replace('"> Muokkaa', "")
    
    lista = a.split("??!!??")

    return choice(lista)


def main():

    today = datetime.datetime.now()

    cfg = ConfigParser()
    cfg.read('env.cfg')

    bot = Bot(token=cfg['TELEGRAM']['token'])

    # TEStI
    #chat_id = cfg['TELEGRAM']['id']
    
    # TUOTANTO
    chat_id = cfg['TELEGRAM']['real']
    
    owm = pyowm.OWM(cfg['PYOWM']['token'])

    viesti = pvm() + "\n" + saa(owm) + "\n" + \
             nimi() + "\n" + liputus() + "\n" + \
             fakta(today.day, today.month)

    send(bot, viesti, chat_id)
    print(viesti)


if __name__ == "__main__":
    main()
