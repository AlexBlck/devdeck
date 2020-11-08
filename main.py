import logging
import sys
import threading

from StreamDeck.DeviceManager import DeviceManager

from dev_deck import DevDeck
from main_deck_controller import MainDeckController

if __name__ == "__main__":
    root = logging.getLogger('devdeck')
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    streamdecks = DeviceManager().enumerate()

    for index, deck in enumerate(streamdecks):
        deck.open()
        root.info('Connecting to deck: %s (S/N: %s)', deck.id(), deck.get_serial_number())

        dev_deck = DevDeck(deck)
        dev_deck.set_active_deck(MainDeckController())

        for t in threading.enumerate():
            if t is threading.currentThread():
                continue

            if t.is_alive():
                t.join()
