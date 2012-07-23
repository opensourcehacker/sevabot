# -*- coding: utf-8 -*-

import time
from bot import Sevabot

def main():

    print("Starting bot")

    sevabot = Sevabot()

    interval = 1
    while(True):
        time.sleep(interval)
        sevabot.runCron(interval)

if __name__ == "__main__":
    main()