# Tecnocat

Còpia estàtica de tecnocat.eu, l'antiga web WordPress, amb les dues subwebs fetes amb eXeLearning:

- `linkat/` és el curs "Linkat per coordinadors" (abans a linkat.tecnocat.eu).
- `ia/` són els recursos d'IA (abans a webtecnocat.github.io/ia).

Tot és HTML, CSS i una mica de JavaScript. No cal cap servidor ni base de dades.

## Com es publica a GitHub Pages

Aquesta carpeta és `docs/` dins del repositori `webtecnocat/webtecnocat.github.io`. A GitHub, a Settings → Pages, està triat "Deploy from a branch", branca `main` i carpeta `/docs`. La web es veu a https://webtecnocat.github.io/.

Si vols que surti a tecnocat.eu, a la mateixa pantalla hi ha l'apartat "Custom domain". Cal posar-hi el domini i afegir els registres DNS que indica GitHub al proveïdor del domini.

El `sitemap.xml`, el `robots.txt` i les etiquetes que fan sortir el títol i la imatge quan es comparteix un enllaç porten l'adreça de `URL_WEB`. Si la web es publica en una altra adreça, cal canviar `URL_WEB` a `eines/construeix.py` i tornar-la a generar.

Amb una adreça que no sigui de github.io, l'script crea també el fitxer `CNAME` amb el domini. GitHub el fa servir per saber quin domini propi té la web. Mentre les DNS del domini no apuntin a GitHub, `URL_WEB` ha de ser l'adreça de github.io; si no, GitHub enviaria les visites a un domini que encara no funciona.

Les adreces de l'antic WordPress (com `/2019/09/21/clonezilla/`) tenen una pàgina que porta a la nova, perquè no fallin els enllaços antics ni els resultats de Google.

## Vídeos

Els vídeos de YouTube surten com una miniatura. Quan la web està publicada (https), en clicar-hi es reprodueixen dins la pàgina. Si obres els fitxers directament des de l'ordinador (file://), YouTube no permet reproduir-los incrustats i el clic obre el vídeo a YouTube en una pestanya nova.

## Com es regenera

Aquesta carpeta la genera `eines/construeix.py` a partir de la còpia original. No editis els fitxers a mà si després has de tornar a generar-la, perquè es perdrien els canvis.
