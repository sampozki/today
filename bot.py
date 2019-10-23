# -*- coding: utf-8 -*-
# Copyright: Sampo Pelto 2019

from telegram import Bot
from time import gmtime, strftime
from datetime import timedelta, datetime
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

    #tiettyyn kellonaikaan
    forecaster = owm.three_hours_forecast('Tampere,FI')
    tempit = []
    ajat = [1, 5, 12, 17]
    for kellot in ajat:
        time = datetime.now() + timedelta(days=0, hours=kellot)
        weather = forecaster.get_weather_at(time)
        temppis = weather.get_temperature(unit='celsius')['temp']
        tempit.append(str(round(temppis,1)) + "°C")

    condition = str(w).split('status=')[1][:-1].lower().split(",")[0]
    keli = condition

    if condition == "clouds":
        keli = "Pilvistä ☁️☁️"
    elif condition == "fog":
        keli = "Sumuista 🌫️🌫️"
    elif condition == "snow":
        keli = "Lumista ❄️❄️"
    elif condition == "rain":
        keli = "Vetistä 🌧️🌧️"
    elif condition == "clear":
        keli = "Aurinkoista ☀️☀️"
    elif condition == "mist":
        keli = "Usvaista 🌫️🌫️"
    else:
        keli = condition


    return "Sää: {0} ja {1}. ".format(keli, ", ".join(tempit))


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
    paiva = str(soup.find('h2')).split(">")[1].split("</")[0]

    if paiva == "Tänään ei ole liputuspäivä.":
        return paiva
    else:
        return "Tänään on " +  str(soup.find('h2')).split("<strong>")[1].split("</strong>")[0].split(". ")[1] + str(choice([".", "!"]))


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
    # lista = re.sub('\s+', ' ', re.sub(r'<.*?>', "", soup.prettify().split("Tapahtumia")[3].split('id="Syn')[0].replace("</li>", "??!!??"))).replace("<span", "").replace('"> Muokkaa', "").split("??!!??")
    del lista[-1]
    if len(lista) == 0:
        return "Ei faktoja :("
    else:
        return "Päivän fakta:" + str(choice(lista))


def main():

    today = datetime.now()

    cfg = ConfigParser()
    cfg.read('/home/sampo/Coding/python/today/env.cfg')

    bot = Bot(token=cfg['TELEGRAM']['token'])

    # TEStI
    # chat_id = cfg['TELEGRAM']['id']

    # TUOTANTO
    chat_id = cfg['TELEGRAM']['real']

    owm = pyowm.OWM(cfg['PYOWM']['token'])

    viesti = pvm() + "\n" + saa(owm) + "\n" + \
             nimi() + "\n" + fakta(today.day, today.month)

    send(bot, viesti, chat_id)
    # print(viesti)


if __name__ == "__main__":
    main()
