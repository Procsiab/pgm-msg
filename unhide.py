#!/usr/bin/env python3

from sys import exit, argv
from os import path
import logging
logging.basicConfig(format='\n[%(asctime)s] (%(levelname)s)\n - %(message)s',
                    level=logging.WARNING)


# Decodifica il file cercando un messaggio valido
def unhide_message(pgm):
    # Apri file immagine
    FILE_NAME = pgm
    IMAGE_FILE = open(FILE_NAME, "r")

    # Leggi tutte le linee (pixel) del file, rimuovi le prime 4
    IMAGE = IMAGE_FILE.readlines()
    IMAGE = IMAGE[4:]

    # Converti le stringhe che compongono l'immagine in interi
    CIPHERTEXT = []
    for pixel in IMAGE:
        if len(pixel) > 0 and pixel.strip() != "":
            value = int(pixel.strip())
            CIPHERTEXT.append(value)

    # Leggi il bit meno significativo (LSB) di gruppi di 7 byte dal ciphertext
    # salva ciascuna lettera in una stringa e stampala quando incontri il
    # terminatore
    position = 0
    letter_buffer = 0
    message_buffer = ""
    for byte in CIPHERTEXT:
        logging.info("Scanning: position %d\tvalue %d" % (position, byte))
        if byte & 1 != 0:
            logging.info("\tLSB = 1")
            letter_buffer += (2**position)
        else:
            pass
            logging.info("\tLSB = 0")
        position += 1

        if position > 6:
            logging.info("==> Read character: %c (%r)" % (chr(letter_buffer),
                                                          letter_buffer))
            if letter_buffer > 0 and letter_buffer < 128:
                logging.info(chr(letter_buffer))
                message_buffer += chr(letter_buffer)
            elif letter_buffer == 0:
                logging.info("EOM")
                print(message_buffer)
                exit(0)
            else:
                logging.warning("Invalid char", hex(letter_buffer))
            position = 0
            letter_buffer = 0
    logging.error("No string terminator found!")
    logging.error("\tmessage buffer:\n %s" % message_buffer)
    exit(1)

# Funzione principale, esegue decodifica dell'immagine
def main():
    if len(argv) > 1:
        filename = argv[1]
        if path.isfile(filename):
            unhide_message(filename)
        else:
            logging.error("File not found: %s" % filename)
    else:
        logging.error("Usage: unhide <PGM file path>")


# Avvia funzione principale se il file viene eseguito
if __name__ == "__main__":
    main()
