# Portable Gray Map cypher

This funny project comes from a programming challenge exercise that I found interesting (and I still do!), so I decided to share it over GitHub.

## How it works?

Hide an ASCII string inside a PGM picture, encoding the LSB of each pixel as one 
of the seven bits that make up a letter character. To run these scripts a PGM 
file is needed, like the one provided in this repo.

### Usage examples

Hide a message:

```bash
./hide.py "Such encryption, much secure" ./security.pgm
```

Decode a message:

```bash
./unhide.py ./security.pgm
```
