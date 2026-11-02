# Tecnocat: còpia estàtica de tecnocat.eu

Projecte per passar l'antiga web WordPress de tecnocat.eu, i les seves subwebs, a una web estàtica publicada a GitHub Pages.

Estat a 2 de novembre de 2026: la web està acabada i comprovada, a la carpeta `docs/`. Es publica al repositori `webtecnocat/webtecnocat.github.io`, a l'adreça https://webtecnocat.github.io/.

## Què hi ha a cada carpeta

- `docs/`: la web acabada. És el que publica GitHub Pages.
- `eines/construeix.py`: l'script que genera `docs/` a partir dels originals. S'executa amb `python3 eines/construeix.py`.
- `eines/assets/`: estils, JavaScript, fonts i imatges del tema.
- `eines/descarrega_toshiba.sh` i `eines/descarrega_fonts.py`: scripts que es van fer servir per baixar les presentacions de Toshiba i les fonts. Només calen per tornar-les a baixar.
- `tecnocat-copia.html`: la còpia del WordPress (articles i pàgines).
- `linkat.tecnocat.eu/`: el curs "Linkat per coordinadors" (eXeLearning).
- `webtecnocat.github.io/ia/`: els recursos d'IA (eXeLearning).
- `presentacions/`: presentacions d'App Inventor, de Toshiba i de Grsync, fitxes d'activitats i la plantilla de la llibreta de notes.
- `recuperat/`: imatges i pàgines recuperades de l'Internet Archive.

`docs/` ja té tot el contingut de les altres carpetes, però les guardem al repositori per poder tornar a generar la web amb l'script.

## Publicació a GitHub

- Compte: webtecnocat. S'hi entra amb Google (tecnocat.eu@gmail.com).
- Els commits es fan amb el nom webtecnocat i el correu privat 90789856+webtecnocat@users.noreply.github.com, configurats només dins d'aquest repositori. La resta de l'ordinador continua amb la compte de cap d'estudis.
- Des d'aquest ordinador es connecta per SSH amb l'àlies `github-webtecnocat` (definit a `~/.ssh/config`), i per això el remot és `git@github-webtecnocat:webtecnocat/webtecnocat.github.io.git`.
- A GitHub, Settings → Pages: "Deploy from a branch", branca `main`, carpeta `/docs`.

La compte té dos repositoris més, que GitHub continua servint a la seva adreça: `ia` (https://webtecnocat.github.io/ia/, el mateix contingut que `docs/ia/`) i `Web` (https://webtecnocat.github.io/Web/, una altra web d'eXeLearning sobre Linkat, Epoptes, impressores, pissarres digitals i serveis del Departament, que no és en aquest projecte). Encara s'ha de decidir què es fa amb `Web`.

Per canviar la web: editar els originals o l'script, executar `python3 eines/construeix.py` i fer commit i push.

Si es passa al domini tecnocat.eu, cal tornar a posar `URL_WEB = "https://tecnocat.eu/"` al principi de `eines/construeix.py` i regenerar la web, que llavors crea el fitxer `CNAME`. Però només quan les DNS ja apuntin a GitHub (vegeu l'apartat següent); si no, GitHub enviaria les visites a un domini que encara no funciona.

## El domini tecnocat.eu

El domini i l'allotjament són a IONOS, però són dues coses separades. Es pot cancel·lar l'allotjament i mantenir només el domini, que és molt més barat, i fer que apunti a GitHub Pages.

Passos, en aquest ordre:

1. Publicar la web a GitHub Pages i comprovar que funciona a l'adreça de github.io.
2. Mirar si algú fa servir correu @tecnocat.eu. El domini té el correu configurat a IONOS (registres MX). Si s'hi fa servir algun compte, el correu s'ha de conservar o moure abans de cancel·lar res.
3. A IONOS, al DNS del domini, canviar els registres:
   - Registres A de `tecnocat.eu`: 185.199.108.153, 185.199.109.153, 185.199.110.153 i 185.199.111.153.
   - Registres AAAA (opcional): 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153 i 2606:50c0:8003::153.
   - Registre CNAME de `www`: `<compte>.github.io`.
4. A GitHub, al repositori, anar a Settings → Pages → Custom domain, escriure `tecnocat.eu` i, quan GitHub hagi comprovat el domini, marcar "Enforce HTTPS". El canvi de DNS pot trigar unes hores.
5. Els subdominis antics (linkat, appinv1, appinv2, tecnocat2019) apunten ara a l'allotjament d'IONOS. GitHub Pages no els pot servir, però a IONOS es poden configurar com a redirecció web: linkat.tecnocat.eu → https://tecnocat.eu/linkat/, appinv1 → https://tecnocat.eu/presentacions/appinv1/, appinv2 → https://tecnocat.eu/presentacions/appinv2/, i tecnocat2019 → https://tecnocat.eu/ (les adreces antigues dels articles ja tenen una pàgina de redirecció dins la web).
6. Quan tot funcioni, canviar el contracte d'IONOS a només domini, o cancel·lar l'allotjament.

Si al final no es manté el domini, la web funciona igual a l'adreça de github.io. Només cal canviar `URL_WEB` i regenerar-la.

### Què costa mantenir només el domini

El preu no és el mateix a tot arreu. El preu de base del .eu el fixa l'organisme que el gestiona, però cada registrador hi posa el seu marge. Molts fan el primer any molt barat i després la renovació puja. Preus trobats l'octubre del 2026:

- IONOS (on és ara): 1 € el primer any i 12 € l'any com a preu de referència, sense IVA (uns 14,5 € amb IVA). No hi ha publicada la tarifa de renovació exacta del .eu. El preu real es pot mirar al panell d'IONOS o a l'última factura del domini.
- Porkbun: uns 5,9 dòlars l'any, igual el primer any que les renovacions.
- Spaceship: uns 5,7 dòlars l'any de renovació, el més barat que es va trobar.
- OVHcloud: uns 9 dòlars l'any de renovació.
- Cloudflare: segons una de les comparatives, no ven dominis .eu.

Mantenir només el domini costa, doncs, entre 5 i 15 € l'any. Traspassar-lo a un altre registrador estalviaria uns 8 € l'any, però caldria moure les DNS i, si es fa servir, el correu @tecnocat.eu. La recomanació és deixar-lo a IONOS i canviar el contracte a només domini.

El titular d'un .eu ha de ser una persona o entitat amb residència a la Unió Europea, i en un traspàs ha de continuar sent el mateix.

Fonts: [IONOS España](https://www.ionos.es/dominios/reservar-dominios), [HostAdvice](https://es.hostadvice.com/hosting-company/ionos-reviews/ionos-domain-registration-review/), [Best .eu Domain Registrars](https://www.best-domain-registrars.com/tlds/eu/), [DEV Community](https://dev.to/paullovelace/4-domain-registrars-ranked-by-renewal-price-october-2026-4eo0), [Circular Media](https://circularmedia.nl/articles/cheapest-domain-registrar-eu-renewals/), [TLDbee](https://www.tldbee.com/cheapest/eu).

## Coses que no s'han pogut recuperar

- El tauler de Symbaloo (article Simbalo).
- Un vídeo de YouTube esborrat.
- La imatge `Schedule008.png` de la pràctica 10 del curs de Linkat.
- Els quatre fitxers de Dropbox de "De linux Mint a Linkat" (tema Gilouche, fons de pantalla, llista d'usuaris i logo d'arrencada). Si apareixen en algun disc, es poden afegir.
- La màquina virtual Android 4.2.2 de "App Inventor virtualitzar MIT Companion".
