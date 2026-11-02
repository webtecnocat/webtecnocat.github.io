#!/usr/bin/env python3
"""Genera la web estàtica de Tecnocat a la carpeta web/.

Fonts:
  tecnocat-copia.html          articles i pàgines (JSON incrustat, imatges en base64)
  linkat.tecnocat.eu/          subweb eXeLearning "Linkat per coordinadors"
  webtecnocat.github.io/ia/    subweb eXeLearning "IA"
  presentacions/               presentacions App Inventor (appinv1 i appinv2.tecnocat.eu) i Google Docs antic (PDF)
  recuperat/                   imatges i pàgines recuperades de l'Internet Archive

Ús:  python3 eines/construeix.py
"""
import base64
import hashlib
import html
import json
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

ARREL = Path(__file__).resolve().parent.parent
SORTIDA = ARREL / "docs"
# Adreça pública de la web: la fan servir el sitemap.xml i les etiquetes per compartir a xarxes.
# Si es publica en una altra adreça (per exemple usuari.github.io/tecnocat/), cal canviar-la aquí.
# Si no és una adreça de github.io, l'script també crea el fitxer CNAME del domini propi: mentre
# les DNS del domini no apuntin a GitHub, cal posar aquí l'adreça de github.io.
URL_WEB = "https://webtecnocat.github.io/"
DESCRIPCIO_WEB = ("Apunts i recursos de Josep M Sardà sobre Linkat, App Inventor, programari lliure, "
                  "tecnologia i intel·ligència artificial.")
TEMA = ARREL / "eines" / "assets" / "tema"  # logo, icona i decoracions del tema WordPress original
SUBWEBS = {
    "linkat": (ARREL / "linkat.tecnocat.eu", "Linkat per coordinadors"),
    "ia": (ARREL / "webtecnocat.github.io" / "ia", "Recursos d'IA"),
}
# Presentacions d'App Inventor descarregades d'appinv1/appinv2.tecnocat.eu (octubre 2026)
PRESENTACIONS = ARREL / "presentacions"
# Fitxes de x01 Activitats AppInv2, abans enllaçades amb goo.gl (el servei ja no redirigeix).
# Els PDF són al Drive de josepm.sarda i es van baixar amb GAM des de ci@iesmalgrat.cat.
# El dades.csv (abans a altres.tecnocat.eu) s'ha refet amb el contingut que surt al PDF 03.
GOOGL = {
    "3stcE8": "presentacions/appinventor/01-rutes.pdf",
    "zprrwb": "presentacions/appinventor/02-ruta-entre-dos-llocs.pdf",
    "SO4GOy": "presentacions/appinventor/03-consulta-csv.pdf",
    "a9p5Ge": "presentacions/appinventor/04-farmacies-de-guardia.pdf",
    "AcrWWm": "presentacions/appinventor/dades.csv",
    # Llibreta de notes: plantilla de Google Sheets (de tecnocat.eu@gmail.com). Funciona amb un menú
    # d'Apps Script, per això l'enllaç va a Google i es guarda una còpia en Excel per si de cas.
    "dLHRuL": "https://drive.google.com/embeddedtemplate?id=1oB5lHe2eqrwm03vQ5e5n2kYUqLVKTPjyY6xyjir9uj4",
}
# De linux Mint a Linkat: fitxers a la carpeta pública de Dropbox, tancada el 2017 i sense còpia a l'Internet Archive
GOOGL_PERDUTS = {"sZK4z", "gclMa", "1NK6M", "ACcZv"}
# Presentacions del Google Docs antic, en PDF + una imatge per diapositiva dins presentacions/.
# Les Toshiba es van exportar del Drive de ci@iesmalgrat.cat amb eines/descarrega_toshiba.sh;
# la de Grsync (Utilitats) ve del PDF GRSync.pdf. Clau: id antic de docs.google.com/present
PRESENTACIONS_GOOGLE_DOCS = {
    "dc3n4txz_186s4gzbffp": "utilitats/grsync",
    "ddgzsf4k_56gcf7wrdg": "toshiba/arrancada-rapida-nb200",
    "ddgzsf4k_61c9xvfgf7": "toshiba/crear-nou-usuari",
    "ddgzsf4k_69ndmtzzft": "toshiba/acces-unitat-dades",
    "ddgzsf4k_114dnq322hf": "toshiba/tancar-aplicacio-linkat",
    "ddgzsf4k_124cxd4snhc": "toshiba/actualitzacio-linkat",
    "ddgzsf4k_53cwzmcsws": "toshiba/cerca-mac",
    "ddgzsf4k_48fvbt2gd3": "toshiba/restauracio-nb250",
    "ddgzsf4k_41fjxmfngj": "toshiba/configuracio-wifi",
    "ddgzsf4k_46dcjn6qg7": "toshiba/consideracions-linkat",
    "ddgzsf4k_79f4vtn6gr": "toshiba/fallada-windows-7",
    "ddgzsf4k_121m4wwb4hj": "toshiba/tancar-pulseaudio",
    "ddgzsf4k_103hq4jsgdf": "toshiba/clonezilla-usb",
    "ddgzsf4k_89dfftmjgh": "toshiba/restauracio-toshiba-usb",
}
# Imatges i pàgines recuperades de l'Internet Archive (webs Drupal antigues, octubre 2026)
RECUPERAT = ARREL / "recuperat"
IMATGES_RECUPERADES = {
    "http://tecnocat.eu/sites/default/files/educat1x1/EDUCAT1x1_logo_v3_Escola20.png": "EDUCAT1x1_logo_v3_Escola20.png",
    "http://nou.tecnocat.eu/sites/default/files/AppInventor/Companion10.png": "Companion10.png",
    "http://nou.tecnocat.eu/sites/default/files/AppInventor/Companion12.png": "Companion12.png",
    "http://tecnocat.eu/sites/default/files/styles/large/public/field/image/Selecci%C3%B3_016_1.png?itok=zh9aDAPb": "Seleccio_016_1.png",
    "http://tecnocat.eu/sites/default/files/programari/800px-Mapa-conceptual-del-programari-lliure.svg.png": "Mapa-conceptual-del-programari-lliure.png",
    "http://tecnocat.eu/sites/default/files/linux/hfs/openhfs.png": "openhfs.png",
    "http://tecnocat.eu/sites/default/files/linux/Clonezilla_menu.png": "Clonezilla_menu.png",
    "http://tecnocat.eu/sites/default/files/linux/shedule/schedule2.jpg": "schedule2.jpg",
    "http://tecnocat.eu/sites/default/files/linux/shedule/schedule3.jpg": "schedule3.jpg",
    "http://tecnocat.eu/sites/default/files/linux/carcaters/caracteres1.png": "caracteres1.png",
    "http://tecnocat.eu/sites/default/files/linux/carcaters/caracteres2.png": "caracteres2.png",
}

# Enllaços externs morts o caducats (comprovats l'octubre del 2026). None = es deixa el text sense enllaç.
ENLLACOS = {
    # Programari lliure: el "Web" de cada programa, a l'adreça actual del projecte
    "http://www.avast.com/esp/download-avast-home.html": "https://www.avast.com/free-antivirus-download",
    "http://www.7-zip.org/": "https://www.7-zip.org/",
    "http://www.ghisler.com/": "https://www.ghisler.com/",
    "http://www.gimp.org/": "https://www.gimp.org/",
    "http://www.inkscape.org/": "https://inkscape.org/",
    "http://picasa.google.com/": None,
    "http://www.xnview.com/en/index.html": "https://www.xnview.com/",
    "http://infrarecorder.org/": "https://sourceforge.net/projects/infrarecorder/",
    "http://www.mozilla-europe.org/ca/firefox//": "https://www.mozilla.org/ca/firefox/",
    "http://www.mozilla-europe.org/ca/products/thunderbird/": "https://www.thunderbird.net/ca/",
    "http://kompozer.net/": "https://sourceforge.net/projects/kompozer/",
    "http://personales.ya.com/mecanet/main14/index_main14.html/": None,
    "http://sourceforge.net/projects/mecanog/files/": "https://sourceforge.net/projects/mecanog/",
    "http://www.aimp.ru/index.php?do=lang-en/": "https://www.aimp.ru/",
    "http://audacity.sourceforge.net/": "https://www.audacityteam.org/",
    "http://audacity.sourceforge.net/download/windows/": "https://www.audacityteam.org/download/",
    "http://www.formatoz.com/ES_index.html/": "https://www.pcfreetime.com/formatfactory/",
    "http://www.videolan.org/vlc//": "https://www.videolan.org/vlc/",
    "http://www.defraggler.com/": "https://www.ccleaner.com/defraggler",
    "http://www.ghostscript.com/Ghostscript.html": "https://www.ghostscript.com/",
    "http://ghisler.fileburst.com/languages/wcmd_cat.zip": None,
    "http://cdlibre.org/": None,
    "http://www.megaupload.com/?d=7ZUA2L3R": None,
    # Altres pàgines
    "http://clonezilla.org/download/sourceforge/stable/iso-zip-files.php": "https://clonezilla.org/downloads.php",
    "http://127.12.34.56:8080/": None,  # és un exemple d'adreça, no un enllaç
    "http://nou.tecnocat.eu/?q=node/7": "bateries-de-liti-io.html",  # la pàgina recuperada
    "http://www.battery-faq.com/": None,
    "http://mirror1.jarfil.net/androvm.org/Download/androVM_vbox86p_4.1.1_r6.1-20130222-gapps-houdini-flash.ova": None,
}
# Màquina virtual Android 4.2.2 a Drive: el fitxer ja no existeix (i seria massa gran per a GitHub)
ENLLACOS_RATLLATS = {"0B7LZkxjSAxaJeWlqR3lYUG9BM28"}

# Avís de contingut antic. Les entrades antigues porten la data del 2019 perquè és quan es van passar
# a WordPress, però el contingut és del 2009 al 2015. Per això l'avís no es calcula a partir de la data.
AVIS_ANTIC = ('<div class="avis antic">Aquest contingut ve de les primeres versions de Tecnocat, d\'abans del 2019. '
              'Algunes instruccions, enllaços o versions de programes poden haver quedat desfasats.</div>')
SENSE_AVIS = {"retornem", "simbalo", "tecnologia", "tecnologia-industrial"}

# Text alternatiu de les imatges de contingut (per nom de fitxer sense extensió). Les decoratives
# (miniatures de les targetes, fotos d'ambient, vídeos) es deixen amb alt="" a propòsit.
ALTS = {
    "Seleccio_016_1": "Emulador d'Android al costat de l'aplicació MIT App Inventor 2 Companion",
    "Companion10": "Pantalla del MIT App Inventor 2 Companion per connectar amb codi o amb codi QR",
    "Companion12": "App Inventor amb el disseny d'un joc i el mateix joc funcionant a l'emulador",
    "EDUCAT1x1_logo_v3_Escola20": "Logotip d'Educat1x1 i Escola 2.0",
    "els-inicis-deducat-1x1-16": "Miniordinador Toshiba NB200",
    "els-inicis-deducat-1x1-17": "Esquema de la xarxa: Internet, línia DSL, servidor proxy, hub o switch i xarxa interna",
    "installacio-de-fonts-4": "Visor de tipus de lletra amb la vista prèvia de la font Angel Tears i el botó Install Font",
    "la-linkat-5": "Logotip de Linkat edu 18.04",
    "la-linkat-6": "Logotip d'Ubuntu",
    "les-bateries-22": "Recipient ple de piles usades",
    "les-bateries-23": "Esquema de la cel·la d'un acumulador de plom",
    "les-bateries-24": "Secció d'una bateria cilíndrica amb els elèctrodes, el separador i els terminals",
    "les-bateries-25": "Bateria Zebra per a vehicles elèctrics",
    "tux": "Tux, el pingüí de Linux",
    "Mapa-conceptual-del-programari-lliure": "Mapa conceptual del programari lliure",
    "robotica-21": "Braç robòtic connectat a una placa de control per USB",
    "tecnologia-industrial-18": "Gravat antic d'una màquina de vapor al costat de robots industrials actuals",
    "openhfs": "Menú contextual del fitxer hfs.exe amb l'opció Obre amb wine",
    "Clonezilla_menu": "Menú d'arrencada de Clonezilla Live",
    "schedule2": "Cerca del paquet gnome-schedule a la web d'openSUSE",
    "schedule3": "Finestra del Planificador del Gnome per configurar les tasques planificades",
    "caracteres1": "Carpetes amb noms de fitxer amb accents mal codificats",
    "caracteres2": "Les mateixes carpetes amb els accents ja corregits",
}

# Vídeos que ja no existeixen a YouTube (comprovat amb oEmbed, octubre 2026)
VIDEOS_ESBORRATS = {"BaYmfvzX7vM"}

MESOS = ["gener", "febrer", "març", "abril", "maig", "juny", "juliol",
         "agost", "setembre", "octubre", "novembre", "desembre"]

# Slugs més llegibles per als que venien amb números o amb el pare davant
SLUGS = {"55": "installacio-de-fonts", "tecnologia-industrial--146-2": "arquitectura-bioclimatica"}


def data_ca(d):
    a, m, dia = d.split("-")
    mes = MESOS[int(m) - 1]
    de = "d'" if mes[0] in "aeiou" else "de "
    return f"{int(dia)} {de}{mes} de {a}"


def slug_nou(s):
    if s in SLUGS:
        return SLUGS[s]
    return s.split("--")[-1]


def slug_cat(c):
    t = c.lower()
    for a, b in zip("àèéíïòóúüç·", "aeeiiooouc-"):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def text_pla(h):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", h, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t)).strip()


# ---------------------------------------------------------------- imatges

class Imatges:
    def __init__(self, dest):
        self.dest = dest
        self.vistes = {}

    def desa(self, mime, b64, nom):
        dades = base64.b64decode(b64)
        h = hashlib.sha1(dades).hexdigest()
        if h not in self.vistes:
            ext = {"jpeg": "jpg", "svg+xml": "svg"}.get(mime, mime)
            fitxer = f"{nom}-{len(self.vistes) + 1}.{ext}"
            (self.dest / fitxer).write_bytes(dades)
            self.vistes[h] = "imatges/" + fitxer
        return self.vistes[h]

    def extreu(self, h, nom):
        return re.sub(
            r'src="data:image/([a-z+]+);base64,([^"]+)"',
            lambda m: f'src="{self.desa(m.group(1), m.group(2), nom)}" loading="lazy"',
            h)


# ---------------------------------------------------------------- vídeos i incrustats

def video_youtube(src, titol):
    src = html.unescape(src)
    m = re.search(r"/embed/([A-Za-z0-9_-]+)", src)
    vid = m.group(1) if m else ""
    m = re.search(r"[?&]list=([A-Za-z0-9_-]+)", src)
    llista = m.group(1) if m else ""
    if vid in VIDEOS_ESBORRATS:
        return ('<div class="avis">Aquest vídeo ja no està disponible a YouTube '
                '(l\'han esborrat o fet privat).</div>')
    if vid:
        enllac = f"https://www.youtube.com/watch?v={vid}" + (f"&list={llista}" if llista else "")
        incr = f"https://www.youtube-nocookie.com/embed/{vid}?rel=0" + (f"&list={llista}" if llista else "")
        fons = f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy">'
        etiqueta = "Mira el vídeo"
    else:
        enllac = f"https://www.youtube.com/playlist?list={llista}"
        incr = f"https://www.youtube-nocookie.com/embed/videoseries?list={llista}&rel=0"
        fons = '<span class="llista">Llista de reproducció</span>'
        etiqueta = "Obre la llista de vídeos"
    return (f'<a class="video" href="{html.escape(enllac)}" target="_blank" rel="noopener" '
            f'data-embed="{html.escape(incr)}" title="{html.escape(titol)}">{fons}'
            f'<span class="play" aria-hidden="true"></span><span class="peu">{etiqueta} a YouTube</span></a>')


def visor_diapos(nom):
    """Presentació com a imatges (una per diapositiva) amb fletxes; tecnocat.js en fa el pas."""
    imatges = sorted((PRESENTACIONS / nom).glob("*.jpg"),
                     key=lambda f: int(re.search(r"(\d+)$", f.stem).group(1)))
    n = len(imatges)
    imgs = "".join(f'<img src="presentacions/{nom}/{f.name}" alt="Diapositiva {i} de {n}"'
                   f'{" class=\"vista\"" if i == 1 else ""} loading="lazy">' for i, f in enumerate(imatges, 1))
    return (f'<div class="diapos"><div class="diapos-marc">{imgs}</div>'
            f'<div class="diapos-ctrl"><button type="button" class="ant" aria-label="Diapositiva anterior">‹</button>'
            f'<span class="num">1 / {n}</span>'
            f'<button type="button" class="seg" aria-label="Diapositiva següent">›</button>'
            f'<a href="presentacions/{nom}.pdf" target="_blank">PDF</a></div></div>')


def incrustat(etiqueta, titol):
    src = re.search(r'src="([^"]*)"', etiqueta)
    src = html.unescape(src.group(1)) if src else ""
    if "youtube.com/embed" in src:
        return video_youtube(src, titol)
    if "docs.google.com" in src and "present" in src:
        m = re.search(r"id=([a-z0-9_]+)", src)
        pdf = PRESENTACIONS_GOOGLE_DOCS.get(m.group(1) if m else "")
        if pdf:
            return visor_diapos(pdf)
        return ('<div class="avis">Aquí hi havia una presentació del Google Docs antic. '
                'Google la va retirar i ja no es pot veure.</div>')
    if "linkat.tecnocat.eu" in src:
        return ('<a class="targeta-enllac" href="linkat/index.html"><b>Linkat per coordinadors</b>'
                '<span>Material del curs, 12 pràctiques</span></a>')
    if "forms.gle" in src or "docs.google.com/forms" in src:
        return ""
    if "symbaloo.com" in src:
        return '<div class="avis">El tauler de Symbaloo que hi havia aquí ja no està disponible.</div>'
    if "altres.tecnocat.eu/AppLinkat2" in src:
        return ('<div class="presentacio"><iframe src="presentacions/appinv2/index.html" '
                'title="Presentació App Inventor a la Linkat" allowfullscreen loading="lazy"></iframe></div>')
    if "altres.tecnocat.eu" in src:
        return '<div class="avis">Aquesta presentació estava a altres.tecnocat.eu, que ja no funciona.</div>'
    return etiqueta


def posa_alts(h):
    def alt(m):
        src = re.search(r'src="imatges/(?:recuperades/)?([^"]+)"', m.group(0))
        text = ALTS.get(Path(src.group(1)).stem) if src else None
        return m.group(0).replace('alt=""', f'alt="{html.escape(text)}"') if text else m.group(0)
    return re.sub(r'<img\b[^>]*\balt=""[^>]*>', alt, h)


def imatge_recuperada(m):
    fitxer = IMATGES_RECUPERADES.get(html.unescape(m.group(1)))
    return f'<img src="imatges/recuperades/{fitxer}" alt="" loading="lazy">' if fitxer else m.group(0)


def neteja_cos(h, titol, mapa_urls):
    # Incrustats: iframe/embed/object + l'enllaç "↗ Obre..." que hi afegia la còpia
    h = re.sub(r'<p class="embed-link">.*?</p>', "", h, flags=re.S)
    h = re.sub(r"<iframe\b[^>]*>.*?</iframe>", lambda m: incrustat(m.group(0), titol), h, flags=re.S)
    h = re.sub(r"<embed\b[^>]*>", lambda m: incrustat(m.group(0), titol), h)

    # Primer h1 igual que el títol: ja el posem nosaltres
    m = re.search(r"<h1[^>]*>(.*?)</h1>", h, flags=re.S)
    if m and text_pla(m.group(1)).lower() == text_pla(titol).lower():
        h = h[:m.start()] + h[m.end():]

    # Enllaços a les subwebs i a la mateixa web
    h = re.sub(r'href="https?://linkat\.tecnocat\.eu/?"', 'href="linkat/index.html"', h)
    h = re.sub(r'href="https?://webtecnocat\.github\.io/ia/?"', 'href="ia/index.html"', h)
    h = re.sub(r'href="https?://altres\.tecnocat\.eu/AppLinkat2/?(index\.html)?"', 'href="presentacions/appinv2/index.html"', h)
    h = re.sub(r'href="https?://appinv1\.tecnocat\.eu/?"', 'href="presentacions/appinv1/index.html"', h)
    h = re.sub(r'href="https?://appinv2\.tecnocat\.eu/?"', 'href="presentacions/appinv2/index.html"', h)
    h = re.sub(r'<a href="https?://goo\.gl/(\w+)"[^>]*>(.*?)</a>',
               lambda m: "(fitxer perdut)" if m.group(1) in GOOGL_PERDUTS else m.group(0), h, flags=re.S)
    h = re.sub(r'(<a href="https?://goo\.gl/dLHRuL"[^>]*>).*?</a>',
               r'\1Plantilla full de notes 2015-16</a> (si no podeu fer servir Google, hi ha una '
               r'<a href="presentacions/llibreta-de-notes/plantilla-full-de-notes.xlsx">còpia en Excel</a>, '
               r'sense el menú que genera els fulls)', h, flags=re.S)
    h = re.sub(r'(?:https?://)?goo\.gl/(\w+)', lambda m: GOOGL.get(m.group(1), m.group(0)), h)
    for vella, nova in mapa_urls.items():
        h = h.replace(f'href="{vella}"', f'href="{nova}"')
    h = re.sub(r'<span class="img-missing">[^<]*<a href="([^"]+)"[^>]*>[^<]*</a></span>', imatge_recuperada, h)
    h = h.replace('class="img-missing">Imatge no disponible (ja no existeix al servidor antic):',
                  'class="img-missing">Imatge perduda:')
    # Wikispaces va tancar el 2018 i l'Internet Archive no en té còpia. Els "Característiques"
    # ratllats ja marcaven l'enllaç com a mort: es treuen. La resta es deixa com a text.
    h = re.sub(r'(&nbsp;)?<a href="https?://[\w.]*wikispaces\.com/[^"]*"[^>]*>[^<]*<s>.*?</a>', "", h, flags=re.S)
    h = re.sub(r'<a href="https?://[\w.]*wikispaces\.com/[^"]*"[^>]*>(.*?)</a>', r"\1", h, flags=re.S)
    h = re.sub(r'<a href="([^"]+)"[^>]*>(.*?)</a>', enllac_extern, h, flags=re.S)
    # Restes del tema WordPress
    h = re.sub(r"</div><!-- \.entry-summary -->", "", h)
    return h.strip()


def enllac_extern(m):
    href = html.unescape(m.group(1))
    if href in ENLLACOS:
        nou = ENLLACOS[href]
        return m.group(2) if nou is None else m.group(0).replace(m.group(1), html.escape(nou), 1)
    if "redlink=1" in href:  # pàgines de la Viquipèdia que no existeixen
        return m.group(2)
    if any(x in href for x in ENLLACOS_RATLLATS):
        return f"<s>{m.group(2)}</s>"
    return m.group(0)


def actualitza_programari(h):
    """Programari lliure (2009): els "Descarrega" baixaven versions antigues; queda només la web de cada programa."""
    h = re.sub(r'<a [^>]*>(Descarrega[^<]*|Traduccions)</a>(&nbsp;|\s)*', "", h)
    h = re.sub(r"<p>(&nbsp;|\s)+", "<p>", h)
    h = h.replace("<p>Web</p>", "")  # programes que ja no tenen web (Picasa, Mecanet)
    # CD Libre era un recull de programes en CD que ja no existeix
    h = h.replace(" Softcatalà, altres llocs on podeu trobar programari lliure és a “http://cdlibre.org/”&gt; CD Libre.",
                  " Softcatalà.", 1)
    h = h.replace("Picasa&nbsp;</strong>és", "Picasa&nbsp;</strong>(Google el va abandonar el 2016) és", 1)
    m = re.search(r"</p>", h)
    return (h[:m.end()] + '<div class="avis">Els enllaços de descàrrega originals eren de versions del 2009. '
            'Ara cada programa enllaça a la seva web, on hi ha la versió actual.</div>' + h[m.end():])


# ---------------------------------------------------------------- plantilla

MENU = [
    ("Inici", "index.html", []),
    ("Linkat", "la-linkat.html", [
        ("Linux", "linux.html", []),
        ("Introducció a la Linkat", "linkat/index.html", []),
        ("De linux Mint a Linkat", "de-linux-mint-a-linkat.html", []),
        ("Instruccions i comandes", "instruccions-i-comandes.html", []),
        ("Instal·lació de fonts", "installacio-de-fonts.html", []),
        ("Utilitats", "utilitats.html", []),
        ("Educat1x1", "educat1x1.html", [
            ("Els inicis", "els-inicis-deducat-1x1.html", []),
            ("Toshiba NB200", "toshiba-nb200.html", []),
            ("Toshiba NB250", "toshiba-nb250.html", []),
        ]),
    ]),
    ("App Inventor", "app-inventor.html", [
        ("Presentació App Inventor", "presentacio-app-inventor.html", []),
        ("x01 Activitats AppInv2", "x01-activitats-appinv2.html", []),
        ("App Inventor virtualitzar MIT Companion", "app-inventor-virtualitzar-mit-companion.html", []),
    ]),
    ("Programari", "programari.html", [
        ("Llibreta de notes", "llibreta-de-notes.html", []),
        ("Clonezilla", "clonezilla.html", []),
        ("Libreoffice", "libreoffice.html", []),
        ("Programari lliure", "programari-lliure.html", []),
    ]),
    ("Tecnologia", "tecnologia.html", [
        ("Tecnologia Industrial", "tecnologia-industrial.html", [
            ("Arquitectura bioclimàtica", "arquitectura-bioclimatica.html", []),
            ("Energia elèctrica", "energia-electrica.html", []),
        ]),
        ("Robòtica", "robotica.html", []),
        ("Les bateries", "les-bateries.html", [
            ("Bateries de Liti-Ió: consells", "bateries-de-liti-io.html", []),
        ]),
    ]),
    ("Recursos IA", "ia/index.html", []),
]


def menu_html(items, pre, actual, nivell=0):
    out = []
    for nom, url, fills in items:
        cls = []
        if fills:
            cls.append("te-fills")
        if url == actual:
            cls.append("actiu")
        c = f' class="{" ".join(cls)}"' if cls else ""
        sub = f'<ul class="submenu">{menu_html(fills, pre, actual, nivell + 1)}</ul>' if fills else ""
        out.append(f'<li{c}><a href="{pre}{url}">{html.escape(nom)}</a>{sub}</li>')
    return "".join(out)


def form_cerca(pre):
    return (f'<form class="cerca" action="{pre}cerca.html" role="search">'
            f'<input type="search" name="q" placeholder="Cerca…" aria-label="Cerca a la web">'
            f'<button type="submit" aria-label="Cerca">⌕</button></form>')


def capcalera(pre, actual):
    return f'''<header class="cap">
  <div class="logo"><a href="{pre}index.html"><img src="{pre}imatges/tema/logo.png" alt="Tecnocat" width="391" height="49"></a>
    <p class="lema">Una mica de tot</p></div>
  <nav class="menu-principal" aria-label="Menú principal">
    <button class="obre-menu" aria-expanded="false">☰ Menú</button>
    <ul class="menu">{menu_html(MENU, pre, actual)}<li class="menu-cerca">{form_cerca(pre)}</li></ul>
  </nav>
</header>'''


def peu(pre):
    return f'''<footer class="peu-web">
  <p class="nom">Tecnocat.eu</p>
  <p>Continguts de Josep M Sardà · <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ca">CC BY-NC-SA 4.0</a></p>
</footer>
<script src="{pre}assets/cerca-dades.js"></script>
<script src="{pre}assets/tecnocat.js"></script>'''


def metadades(titol, cami, desc, imatge=""):
    """Descripció per als cercadors i etiquetes Open Graph (títol, text i imatge en compartir un enllaç)."""
    desc = html.escape(desc or DESCRIPCIO_WEB)
    imatge = URL_WEB + (imatge or "imatges/tema/logo.png")
    return (f'\n<meta name="description" content="{desc}">'
            f'\n<meta property="og:site_name" content="Tecnocat">'
            f'\n<meta property="og:title" content="{html.escape(titol)}">'
            f'\n<meta property="og:description" content="{desc}">'
            f'\n<meta property="og:url" content="{URL_WEB}{cami}">'
            f'\n<meta property="og:image" content="{imatge}">'
            f'\n<meta property="og:locale" content="ca_ES">')


def descripcio(text, n=155):
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0] + "…"


def cap_document(titol, pre, extra=""):
    return f'''<!doctype html>
<html lang="ca">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titol)}</title>
<link rel="icon" href="{pre}imatges/tema/icona.ico">
<link rel="stylesheet" href="{pre}assets/fonts.css">
<link rel="stylesheet" href="{pre}assets/estil.css">{extra}
</head>'''


def pagina(titol, cos, actual="", cami="", desc="", imatge=""):
    extra = metadades(titol, cami, desc, imatge) if cami else '\n<meta name="robots" content="noindex">'
    return (cap_document(titol, "", extra) + '\n<body>\n' + capcalera("", actual)
            + f'\n<div class="contenidor"><main class="principal">{cos}</main></div>\n'
            + peu("") + "\n</body>\n</html>\n")


def targeta(p):
    img = (f'<a class="imatge" href="{p["url"]}"><img src="{p["thumb"]}" alt="" loading="lazy"></a>'
           if p.get("thumb") else "")
    cats = " ".join(f'<a class="cat" href="categoria-{slug_cat(c)}.html">{html.escape(c)}</a>' for c in p["c"])
    return f'''<article class="targeta">{img}
<div class="targeta-cos"><div class="info">{cats}
<h2 class="titol-entrada"><a href="{p["url"]}">{html.escape(p["t"])}</a></h2>
<span class="meta">josepm · <time datetime="{p["d"]}">{data_ca(p["d"])}</time></span></div>
<div class="forma1"></div>
<p class="resum">{html.escape(p["resum"])}</p>
<p class="mes"><a class="btn" href="{p["url"]}">Llegeix més</a></p></div></article>'''


def avis_antic(p):
    antic = p["k"] == "page" or p["d"] < "2020"
    return AVIS_ANTIC if antic and p["s"] not in SENSE_AVIS else ""


def llistat(titol, posts, subtitol=""):
    sub = f'<p class="subtitol">{subtitol}</p>' if subtitol else ""
    cap = f'<header class="cap-llistat"><h1>{html.escape(titol)}</h1>{sub}</header>' if titol else ""
    return cap + '<div class="graella">' + "".join(targeta(p) for p in posts) + "</div>"


# ---------------------------------------------------------------- subwebs eXeLearning

def processa_subweb(carpeta, origen, nom, index_cerca):
    dest = SORTIDA / carpeta
    shutil.copytree(origen, dest)
    for css in ("base.css", "content.css", "nav.css"):
        (dest / css).unlink(missing_ok=True)
    for f in sorted(dest.glob("*.html")):
        s = f.read_text(encoding="utf-8", errors="replace")
        # Fora els estils d'eXe (els substitueix assets/exe.css) i l'script remot del tema CEDEC
        s = re.sub(r'<link[^>]*href="(base|content|nav)\.css"[^>]*>\s*', "", s)
        s = re.sub(r'<script[^>]*_cedec_js\.js"[^>]*>\s*</script>\s*', "", s)
        s = re.sub(r'<meta http-equiv="content-type"[^>]*>', '<meta charset="utf-8">', s)
        extra = ('<link rel="stylesheet" href="../assets/fonts.css">'
                 '<link rel="stylesheet" href="../assets/estil.css"><link rel="stylesheet" href="../assets/exe.css">')
        cos = re.search(r'id="main"[^>]*>(.*?)(<div id=.bottomPagination|<div id="siteFooter"|$)', s, re.S)
        titol = re.search(r"<title>(.*?)</title>", s, re.S)
        titol = html.unescape(titol.group(1)).split("|")[0].strip() if titol else nom
        s = re.sub(r'<meta name="description"[^>]*>\s*', "", s)  # la d'eXe és la mateixa a totes les pàgines
        extra += metadades(titol if titol == nom else f"{titol} · {nom}", f"{carpeta}/{f.name}", descripcio(text_pla(cos.group(1) if cos else "")))
        if "viewport" not in s:
            extra += '<meta name="viewport" content="width=device-width, initial-scale=1">'
        s = s.replace("</head>", extra + "\n</head>", 1)
        s = re.sub(r'<link rel="shortcut icon"[^>]*>', '<link rel="icon" href="../imatges/tema/icona.ico">', s)
        # Capçalera de Tecnocat a dalt i peu a baix
        actiu = "linkat/index.html" if carpeta == "linkat" else "ia/index.html"
        s = re.sub(r"(<body[^>]*>)", lambda m: m.group(1).replace("<body", '<body data-subweb="' + carpeta + '"', 1)
                   + "\n" + capcalera("../", actiu)
                   + f'\n<p class="engruna"><a href="../index.html">Inici</a> › <a href="index.html">{html.escape(nom)}</a></p>',
                   s, count=1)
        s = s.replace("</body>", peu("../") + "\n</body>", 1)
        if carpeta == "linkat":  # curs de Linkat 11.04 a 14.04 (2013-2015)
            s = s.replace('<div id="main">', '<div id="main">' + AVIS_ANTIC.replace("de les primeres versions de Tecnocat, d'abans del 2019",
                          "d'un curs fet entre el 2013 i el 2015, amb les versions de Linkat d'aquells anys"), 1)
        # Text alternatiu: miniatures de les galeries i la insígnia de la llicència
        practica = html.unescape(re.search(r"<title>(.*?)</title>", s, re.S).group(1)).split("|")[0].strip()
        s = re.sub(r'<img alt="" ([^>]*src="[A-Za-z]+?0*(\d+)Thumbnail\.png")',
                   lambda m: f'<img alt="Captura {m.group(2)}: {html.escape(practica)}" {m.group(1)}', s)
        s = s.replace('<img src="ccJosepM88x31.png"', '<img alt="Llicència Creative Commons, Josep M Sardà" src="ccJosepM88x31.png"')
        # La guia de Clonezilla de la XTEC ja no existeix: porta a la de Tecnocat
        s = re.sub(r'<a href="http://www\.xtec\.cat/web/at_usuari/guiesprogramari/clonezilla">[^<]*</a>',
                   '<a href="../clonezilla.html">Clonezilla a Tecnocat</a>', s)
        f.write_text(s, encoding="utf-8")

        cos = re.search(r'id="main"[^>]*>(.*?)(<div id=.bottomPagination|<div id="siteFooter"|</section>\s*</div>\s*<div id=.bottomPagination)', s, re.S)
        titol = re.search(r"<title>(.*?)</title>", s, re.S)
        index_cerca.append({
            "u": f"{carpeta}/{f.name}",
            "t": html.unescape(titol.group(1)).split("|")[0].strip() if titol else f.name,
            "x": text_pla(re.sub(r'<div class="avis antic">.*?</div>', "", cos.group(1) if cos else s))[:4000],
        })


def redireccio(titol, desti, profunditat):
    """Pàgina mínima a l'adreça antiga de WordPress que porta a la nova."""
    rel = "../" * profunditat + desti
    return f'''<!doctype html>
<html lang="ca">
<head>
<meta charset="utf-8">
<title>{html.escape(titol)} · Tecnocat</title>
<link rel="canonical" href="{URL_WEB}{desti}">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={rel}">
</head>
<body><p>Aquesta pàgina ara és a <a href="{rel}">{html.escape(titol)}</a>.</p></body>
</html>
'''


def optimitza_imatges(minim=250_000):
    """Els PNG grossos (captures de pantalla i imatges d'IA) passen a WebP, que ocupa molt menys i es veu igual."""
    canvis = {}
    for f in SORTIDA.rglob("*.png"):
        if f.stat().st_size < minim or "presentacions" in f.relative_to(SORTIDA).parts:
            continue
        webp = f.with_suffix(".webp")
        subprocess.run(["cwebp", "-quiet", "-q", "85", "-m", "6", str(f), "-o", str(webp)], check=True)
        if webp.stat().st_size < f.stat().st_size * 0.7:
            canvis[f.name] = webp.name
            f.unlink()
        else:
            webp.unlink()
    if not canvis:
        return 0
    patro = re.compile(r'(["/])(' + "|".join(re.escape(n) for n in canvis) + r')(["?#])')
    for f in SORTIDA.rglob("*.html"):
        t = f.read_text(encoding="utf-8", errors="replace")
        nou = patro.sub(lambda m: m.group(1) + canvis[m.group(2)] + m.group(3), t)
        if nou != t:
            f.write_text(nou, encoding="utf-8")
    return len(canvis)


# ---------------------------------------------------------------- principal

def main():
    if SORTIDA.exists():
        shutil.rmtree(SORTIDA)
    (SORTIDA / "imatges").mkdir(parents=True)
    (SORTIDA / "assets").mkdir()
    for nom in ("estil.css", "exe.css", "tecnocat.js", "fonts.css"):
        shutil.copy(ARREL / "eines" / "assets" / nom, SORTIDA / "assets" / nom)
    shutil.copytree(ARREL / "eines" / "assets" / "fonts", SORTIDA / "assets" / "fonts")
    shutil.copytree(TEMA, SORTIDA / "imatges" / "tema")

    font = (ARREL / "tecnocat-copia.html").read_text(encoding="utf-8")
    dades = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', font, re.S).group(1))
    dades += json.loads((RECUPERAT / "pagines.json").read_text(encoding="utf-8"))
    # La política de privadesa de WordPress parlava de comentaris i galetes que la web estàtica ja no té
    dades = [i for i in dades if i["s"] != "politica-de-privadesa"]
    shutil.copytree(RECUPERAT / "imatges", SORTIDA / "imatges" / "recuperades")

    imatges = Imatges(SORTIDA / "imatges")
    per_slug = {}
    for it in dades:
        it["slug"] = slug_nou(it["s"])
        if it["slug"] == "linkat":
            it["slug"] = "la-linkat"  # no xocar amb la carpeta linkat/
        it["url"] = it["slug"] + ".html"
        per_slug[it["s"]] = it
    mapa_urls = {}
    for it in dades:
        o = it["o"]
        mapa_urls[o] = it["url"]
        mapa_urls[o.replace("https://", "http://")] = it["url"]

    for it in dades:
        h = imatges.extreu(it["h"], it["slug"])
        m = re.match(r'\s*<figure class="thumb"><img src="([^"]+)"[^>]*></figure>', h)
        it["thumb"] = m.group(1) if m else ""
        if m:
            h = h[m.end():]
        it["cos"] = posa_alts(neteja_cos(h, it["t"], mapa_urls))
        if it["slug"] == "programari-lliure":
            it["cos"] = actualitza_programari(it["cos"])
        if not it["thumb"]:
            m = re.search(r'<img src="(imatges/[^"]+)"', it["cos"])
            it["thumb"] = m.group(1) if m else ""
        paraules = text_pla(it["cos"]).split()
        it["resum"] = " ".join(paraules[:32]) + ("…" if len(paraules) > 32 else "")

    posts = sorted((i for i in dades if i["k"] == "post"), key=lambda p: p["d"], reverse=True)
    pagines = [i for i in dades if i["k"] == "page"]
    cats = {}
    for p in posts:
        for c in p["c"]:
            cats.setdefault(c, []).append(p)

    escriu = lambda nom, txt: (SORTIDA / nom).write_text(txt, encoding="utf-8")

    escriu("index.html", pagina("Tecnocat – Una mica de tot", llistat("", posts), "index.html", "index.html"))
    for c, ps in cats.items():
        escriu(f"categoria-{slug_cat(c)}.html",
               pagina(f"{c} · Tecnocat", llistat(c, ps, "Categoria"), "", f"categoria-{slug_cat(c)}.html",
                      f"Articles de Tecnocat de la categoria {c}."))

    for i, p in enumerate(posts):
        cats_html = " ".join(f'<a class="cat" href="categoria-{slug_cat(c)}.html">{html.escape(c)}</a>' for c in p["c"])
        destacada = f'<figure class="destacada"><img src="{p["thumb"]}" alt=""></figure>' if p["thumb"] and p["thumb"] not in p["cos"] else ""
        nav = '<nav class="nav-entrades">'
        if i + 1 < len(posts):
            nav += f'<a class="ant" href="{posts[i + 1]["url"]}"><small>Entrada anterior</small>{html.escape(posts[i + 1]["t"])}</a>'
        if i > 0:
            nav += f'<a class="seg" href="{posts[i - 1]["url"]}"><small>Entrada següent</small>{html.escape(posts[i - 1]["t"])}</a>'
        nav += "</nav>"
        cos = f'''<article class="entrada">{destacada}
<header class="info">{cats_html}<h1 class="titol-entrada">{html.escape(p["t"])}</h1>
<span class="meta">josepm · <time datetime="{p["d"]}">{data_ca(p["d"])}</time></span><div class="forma1"></div></header>
{avis_antic(p)}<div class="contingut">{p["cos"]}</div></article>{nav}'''
        escriu(p["url"], pagina(f'{p["t"]} · Tecnocat', cos, p["url"], p["url"],
                                       descripcio(p["resum"]), p["thumb"]))

    for p in pagines:
        pare = per_slug.get(p.get("p") or "")
        engruna = f'<p class="engruna"><a href="index.html">Inici</a> › <a href="{pare["url"]}">{html.escape(pare["t"])}</a></p>' if pare else ""
        fills = [q for q in pagines if q.get("p") == p["s"]]
        llista = ""
        if fills:
            llista = '<h2>En aquesta secció</h2><ul class="fills">' + "".join(
                f'<li><a href="{q["url"]}">{html.escape(q["t"])}</a></li>' for q in fills) + "</ul>"
        cos = f'''{engruna}<article class="entrada pagina"><header class="info"><h1 class="titol-entrada">{html.escape(p["t"])}</h1><div class="forma1"></div></header>
{avis_antic(p)}<div class="contingut">{p["cos"]}{llista}</div></article>'''
        escriu(p["url"], pagina(f'{p["t"]} · Tecnocat', cos, p["url"], p["url"],
                                       descripcio(p["resum"]), p["thumb"]))

    escriu("cerca.html", pagina("Cerca · Tecnocat",
                                '<header class="cap-llistat"><h1>Cerca</h1><p class="subtitol" id="cerca-resum"></p>'
                                + form_cerca("").replace('class="cerca"', 'class="cerca cerca-gran"') + '</header>'
                                '<div id="cerca-resultats" class="resultats"></div>'))

    index_cerca = [{"u": i["url"], "t": i["t"], "x": text_pla(i["cos"])[:4000]} for i in posts + pagines]
    for carpeta, (origen, nom) in SUBWEBS.items():
        processa_subweb(carpeta, origen, nom, index_cerca)
    escriu("assets/cerca-dades.js",
           "window.TECNOCAT_CERCA=" + json.dumps(index_cerca, ensure_ascii=False, separators=(",", ":")) + ";\n")

    # Presentacions: es copien tal qual, però amb les fonts locals (fonts.css de cada presentació)
    shutil.copytree(PRESENTACIONS, SORTIDA / "presentacions")
    for f in (SORTIDA / "presentacions").rglob("*.html"):
        t = f.read_text(encoding="utf-8", errors="replace")
        t = re.sub(r'href="https?://fonts\.googleapis\.com/[^"]*"', 'href="fonts.css"', t)
        t = t.replace('href="ai2.appinventor.mit.edu"', 'href="https://ai2.appinventor.mit.edu"')
        f.write_text(t, encoding="utf-8")
    tema = SORTIDA / "presentacions" / "appinv2" / "css" / "theme" / "beige.css"
    tema.write_text(re.sub(r"@import url\(https://fonts\.googleapis\.com/[^)]*\);", "@import url(../../fonts.css);",
                           tema.read_text(encoding="utf-8")), encoding="utf-8")

    convertides = optimitza_imatges()

    # Sitemap per als cercadors: totes les pàgines menys la cerca i la 404
    camins = sorted(str(f.relative_to(SORTIDA)) for f in SORTIDA.rglob("*.html")
                    if f.parts[len(SORTIDA.parts)] not in ("presentacions",) and f.name not in ("cerca.html", "404.html"))
    escriu("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(f"  <url><loc>{URL_WEB}{html.escape(c)}</loc></url>\n" for c in camins) + "</urlset>\n")
    escriu("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {URL_WEB}sitemap.xml\n")
    # Adreces antigues de WordPress (/2019/09/21/clonezilla/, /tecnologia/robotica/...): porten a la nova.
    # Es fan després del sitemap perquè no hi surtin.
    redireccions = 0
    for it in dades:
        if "tecnocat.eu" not in it["o"] or "?" in it["o"]:
            continue
        cami = urlparse(it["o"]).path.strip("/")
        if not cami or (SORTIDA / cami.split("/")[0]).is_file():
            continue
        desti = SORTIDA / cami / "index.html"
        if desti.exists():
            continue
        desti.parent.mkdir(parents=True, exist_ok=True)
        desti.write_text(redireccio(it["t"], it["url"], cami.count("/") + 1), encoding="utf-8")
        redireccions += 1

    domini = urlparse(URL_WEB).hostname
    if not domini.endswith("github.io"):
        escriu("CNAME", domini + "\n")  # GitHub Pages el necessita per al domini propi
    escriu(".nojekyll", "")
    shutil.copy(ARREL / "eines" / "README-web.md", SORTIDA / "README.md")
    # La 404 es pot servir des de qualsevol carpeta (linkat/xxx): amb <base> els enllaços relatius funcionen igual
    escriu("404.html", pagina("No trobat · Tecnocat",
                              '<article class="entrada pagina"><h1 class="titol-entrada">Aquesta pàgina no existeix</h1>'
                              '<p>Potser l\'enllaç és d\'una versió antiga de la web. Prova la <a href="cerca.html">cerca</a> '
                              'o torna a l\'<a href="index.html">inici</a>.</p></article>')
           .replace("<head>", f'<head>\n<base href="{urlparse(URL_WEB).path}">', 1))
    print(f"Fet: {len(posts)} entrades, {len(pagines)} pàgines, {len(imatges.vistes)} imatges, "
          f"{len(index_cerca)} documents a la cerca, {convertides} imatges a WebP, {redireccions} redireccions → {SORTIDA}")


if __name__ == "__main__":
    main()
