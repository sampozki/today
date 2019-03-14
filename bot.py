# -*- coding: utf-8 -*-
# Copyright: Sampo Pelto 2019

import logging
import telegram
from time import gmtime, strftime
from configparser import ConfigParser

cfg = ConfigParser()
cfg.read('env.cfg')


def testsend(bot, msg):
    chat_id = cfg['TELEGRAM']['id']
    bot.send_message(chat_id=chat_id, text=str(msg))


def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.ERROR)

    bot = telegram.Bot(token=cfg['TELEGRAM']['token'])

    pvm = strftime("Tänään on %d.%m.", gmtime())
    viesti = "--\n" + pvm + "\nNimipäivät: \nSää: \nLiputuspäivä: \n--"
    testsend(bot, viesti)
    print(viesti)


if __name__ == "__main__":
    main()
