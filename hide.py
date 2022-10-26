#!/usr/bin/env python3

from sys import argv
from os import path
import logging
logging.basicConfig(format='\n[%(asctime)s] (%(levelname)s)\n - %(message)s',
                    level=logging.WARNING)


# Nascondi il messaggio msg codificandolo nel file pgm
def hide_message(msg, pgm):
    # Messaggio da cifrare
    PLAINTEXT = msg

    # Apri file immagine
    FILE_NAME = pgm
    IMAGE_FILE = open(FILE_NAME, "r")

    # Leggi tutte le linee (pixel) del file
    IMAGE = IMAGE_FILE.readlines()

    # Converti le stringhe che sono i pixel dell'immagine in interi
    PIXELS = []
    for pixel in IMAGE[4:]:
        value = int(pixel.strip())
        PIXELS.append(value)

    # Codifica il messaggio nella lista di pixel, leggendo i primi 7 bit di
    # ciascuna lettera e cambiando il LSB di ciascun pixel se diverso da quello
    # della lettera
    position = 0
    pixel_cursor = 0
    for letter in PLAINTEXT:
        logging.info("==> Encoding: letter %s" % letter)
        while position < 7:
            letter_bit = 0
            if (ord(letter) & (2**position)) > 0:
                letter_bit = 1
            logging.info("\tLetter bit in position %d: %d" % (position, letter_bit))
            if (PIXELS[pixel_cursor] & 0b00000001) != letter_bit:
                if letter_bit == 1:
                    PIXELS[pixel_cursor] = PIXELS[pixel_cursor] | 0b00000001
                elif letter_bit == 0:
                    PIXELS[pixel_cursor] = PIXELS[pixel_cursor] & 0b11111110
            logging.info("\tPixel value: %d, LSB: %d" % (PIXELS[pixel_cursor],
                                                         PIXELS[pixel_cursor] & 0b00000001))
            position += 1
            pixel_cursor += 1
        position = 0
    # Aggiungi terminatore alla fine del messaggio
    logging.info("==> Encoding terminator")
    while position < 7:
        PIXELS[pixel_cursor] = PIXELS[pixel_cursor] & 0b11111110
        position += 1
        pixel_cursor += 1

    # Riaggiungi i metadati davanti alla lista di linee
    LINES = []
    for i in range(4):
        LINES.append(IMAGE[i])

    # Converti i pixel in linee di testo, inseriscili nella lista di linee
    for pixel in PIXELS:
        value = str(pixel) + '\n'
        LINES.append(value)

    # Riapri il file in scrittura
    IMAGE_FILE.close()
    IMAGE_FILE = open(FILE_NAME, "w")

    # Scrivi tutte le righe nel file
    for line in LINES:
        IMAGE_FILE.write("%s" % line)


# Funzione principale, controlla argomento da riga di comando
def main():
    if len(argv) > 2:
        message = argv[1]
        filename = argv[2]
        if path.isfile(filename):
            hide_message(message, filename)
        else:
            logging.error("File not found: %s" % filename)
    else:
        logging.error("Usage: hide <message string> <PGM file path>")


# Avvia funzione principale se il file viene eseguito
if __name__ == "__main__":
    main()
