# Instruccions per acabar de passar la web a tecnocat.eu

Estat a 2 de novembre de 2026: la web està publicada a https://webtecnocat.github.io/ i funciona. Falta passar-la al domini tecnocat.eu i fer neteja.

Ara mateix tecnocat.eu i tots els subdominis (www, linkat, appinv1, appinv2, tecnocat2019) apunten al servidor d'IONOS (217.160.0.2), on hi ha el WordPress antic. El domini també té el correu configurat a IONOS (registres MX a mx00.ionos.es i mx01.ionos.es).

## 1. Mirar el correu @tecnocat.eu

Entra al panell d'IONOS (https://my.ionos.es) i mira si hi ha alguna bústia de correu @tecnocat.eu i si algú la fa servir.

- Canviar la web de lloc (pas 2) no afecta el correu. Els registres MX no s'han de tocar.
- El risc és al pas 6: si canvies el contracte a "només domini", les bústies poden desaparèixer. Si hi ha correu que cal guardar, s'ha de copiar o moure abans.

## 2. Canviar les DNS a IONOS

Al panell d'IONOS, ves a Dominis i SSL › tecnocat.eu › DNS.

1. Esborra el registre A de `tecnocat.eu` (el que apunta a 217.160.0.2, també pot sortir com a `@`).
2. Afegeix quatre registres A per a `tecnocat.eu` (`@`), un per a cada adreça:
   - 185.199.108.153
   - 185.199.109.153
   - 185.199.110.153
   - 185.199.111.153
3. Canvia el registre de `www`: esborra l'A que apunta a 217.160.0.2 i crea un CNAME de `www` cap a `webtecnocat.github.io`.
4. No toquis els registres MX, TXT ni el d'`autodiscover`, que són del correu.

Si IONOS no et deixa canviar el registre A perquè diu que el domini està connectat a l'allotjament, primer has de desconnectar-lo de l'allotjament (a la mateixa pantalla del domini, "Ús del domini" o "Destinació") i després ja el pots editar.

El canvi pot trigar des d'uns minuts fins a unes hores. Per comprovar-ho, al terminal:

```
dig +short tecnocat.eu
dig +short www.tecnocat.eu
```

El primer ha de donar les quatre adreces 185.199.x.153 i el segon ha de començar per `webtecnocat.github.io.`. Mentre surti 217.160.0.2, encara no ha canviat.

## 3. Regenerar la web amb el domini i pujar-la

Només quan el pas 2 ja funcioni. Si no, GitHub enviaria les visites de webtecnocat.github.io a un domini que encara mostra el WordPress antic.

Ho pot fer Claude, o tu mateix al terminal:

```
cd ~/Gemini/tecnocat
sed -i 's|^URL_WEB = .*|URL_WEB = "https://tecnocat.eu/"|' eines/construeix.py
python3 eines/construeix.py
git add -A
git commit -m "Passa la web al domini tecnocat.eu"
git push
```

L'script crearà el fitxer `docs/CNAME` amb `tecnocat.eu`. El commit i el push es fan amb la compte webtecnocat, sense tocar la de cap d'estudis.

## 4. Activar el domini a GitHub

Entra a GitHub amb Google (tecnocat.eu@gmail.com) i obre el repositori `webtecnocat/webtecnocat.github.io`.

1. Ves a Settings › Pages. A "Custom domain" hi hauria de sortir `tecnocat.eu`. Si no hi és, escriu-lo i prem Save.
2. Espera que la comprovació de DNS surti en verd. Pot trigar una estona.
3. Marca "Enforce HTTPS". Si l'opció surt desactivada, és que GitHub encara està fent el certificat: torna-hi al cap d'una hora.

Comprova que https://tecnocat.eu/, https://www.tecnocat.eu/, https://tecnocat.eu/linkat/ i https://tecnocat.eu/ia/ funcionen, i que https://webtecnocat.github.io/ porta a tecnocat.eu.

## 5. Redirigir els subdominis antics

GitHub Pages no pot servir els subdominis antics, però a IONOS es poden convertir en una redirecció web. A cada subdomini, tria "Redirecció" (o "Reenviament") cap a aquestes adreces:

- linkat.tecnocat.eu → https://tecnocat.eu/linkat/
- appinv1.tecnocat.eu → https://tecnocat.eu/presentacions/appinv1/
- appinv2.tecnocat.eu → https://tecnocat.eu/presentacions/appinv2/
- tecnocat2019.tecnocat.eu → https://tecnocat.eu/

Les adreces antigues dels articles (com `/2019/09/21/clonezilla/`) ja tenen una pàgina dins la web que porta a la nova.

## 6. Canviar el contracte d'IONOS

Quan tot funcioni i hagis resolt el correu (pas 1), canvia el contracte a "només domini" o cancel·la l'allotjament. Mantenir només el domini costa entre 5 i 15 € l'any. Abans de cancel·lar, si vols, baixa una còpia del WordPress des del panell, encara que el contingut ja és tot a la web nova.

## 7. Altres coses pendents

- Arreglar `/ia/`, que ara dona error 404. El repositori `ia` publicava amb una GitHub Action i, encara que s'ha fet "Unpublish site", GitHub continua reservant-li l'adreça `/ia/`. Cal canviar-li el nom: al repositori `webtecnocat/ia`, Settings › General › Repository name, posar `ia-antic` i prémer Rename. Després, https://webtecnocat.github.io/ia/ (o https://tecnocat.eu/ia/ després del canvi de domini) ha de mostrar la versió integrada, amb la capçalera i el menú de Tecnocat. Si la versió antiga sortís a `/ia-antic/`, a Settings › Actions › General del mateix repositori es poden desactivar les Actions. El repositori no s'ha d'esborrar.
- Decidir què es fa amb el repositori `Web` (https://webtecnocat.github.io/Web/), que és una altra web d'eXeLearning sobre Linkat, Epoptes, impressores, pissarres digitals i serveis del Departament. No és dins la web nova. Es pot deixar com està, posar-hi un enllaç des del menú o integrar-la com `ia` i `linkat`. No en desactivis la publicació si no l'has integrada abans.
- Esborrar la carpeta `web/` de l'ordinador. És la versió antiga de `docs/`, ja no es fa servir i no es puja a GitHub: `rm -rf ~/Gemini/tecnocat/web`
- Posar una contrasenya nova a la compte webtecnocat de GitHub ("Forgot password", que l'envia a tecnocat.eu@gmail.com). Ara només s'hi pot entrar amb Google.
