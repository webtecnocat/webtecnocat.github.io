#!/usr/bin/env python3
"""Descarrega de Google Fonts les tipografies que fa servir la web, perquè es serveixin des de la mateixa web.

Només cal executar-lo si es canvien les fonts. Deixa els fitxers a:
  eines/assets/fonts.css + eines/assets/fonts/      (web principal i subwebs)
  presentacions/appinv1/fonts.css + fonts/           (Ubuntu, Crimson Text)
  presentacions/appinv2/fonts.css + fonts/           (Lato)

Ús:  python3 eines/descarrega_fonts.py
"""
import re
import urllib.request
from pathlib import Path

ARREL = Path(__file__).resolve().parent.parent
# Amb un navegador modern, Google respon amb fitxers woff2 separats per subconjunts de caràcters
NAVEGADOR = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
SUBCONJUNTS = {"latin", "latin-ext"}

FONTS = [
    ("https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400"
     "&family=Open+Sans:wght@400;600&display=swap", ARREL / "eines" / "assets"),
    ("https://fonts.googleapis.com/css2?family=Ubuntu:wght@700&family=Ubuntu+Mono"
     "&family=Crimson+Text:ital,wght@0,400;0,700;1,400&display=swap", ARREL / "presentacions" / "appinv1"),
    ("https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,400;0,700;1,400;1,700&display=swap",
     ARREL / "presentacions" / "appinv2"),
]


def baixa(url):
    req = urllib.request.Request(url, headers={"User-Agent": NAVEGADOR})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def main():
    for url, dest in FONTS:
        carpeta = dest / "fonts"
        carpeta.mkdir(parents=True, exist_ok=True)
        css = baixa(url).decode("utf-8")
        sortida = []
        noms = {}
        for subconjunt, bloc in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*\{.*?\})", css, re.S):
            if subconjunt not in SUBCONJUNTS:
                continue
            familia = re.search(r"font-family: '([^']+)'", bloc).group(1)
            estil = re.search(r"font-style: (\w+)", bloc).group(1)
            pes = re.search(r"font-weight: (\d+)", bloc).group(1)
            remot = re.search(r"url\((https://[^)]+\.woff2)\)", bloc).group(1)
            nom = f"{familia.lower().replace(' ', '-')}-{pes}{'i' if estil == 'italic' else ''}-{subconjunt}.woff2"
            # Les fonts variables comparteixen fitxer entre gruixos: se'n baixa només un
            nom = noms.setdefault(remot, nom)
            if not (carpeta / nom).exists():
                (carpeta / nom).write_bytes(baixa(remot))
            sortida.append(f"/* {subconjunt} */\n" + bloc.replace(remot, f"fonts/{nom}"))
        (dest / "fonts.css").write_text("\n".join(sortida) + "\n", encoding="utf-8")
        print(f"{dest.relative_to(ARREL)}: {len(sortida)} @font-face, {len(list(carpeta.glob('*.woff2')))} fitxers")


if __name__ == "__main__":
    main()
