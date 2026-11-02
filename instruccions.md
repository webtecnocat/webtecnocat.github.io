# Instruccions per acabar de passar la web a tecnocat.eu

Estat a 2 de novembre de 2026: la web nova està acabada i funciona a https://tecnocat.eu/, amb https. També funcionen /linkat/, /ia/ (la versió integrada) i /Web/. www.tecnocat.eu i webtecnocat.github.io porten a tecnocat.eu, i linkat.tecnocat.eu porta a https://tecnocat.eu/linkat/.

## Per comprovar el proper cop (Claude)

A IONOS s'han esborrat els registres DNS d'`appinv1`, `appinv2` i `www.linkat` (A i AAAA). El 2 de novembre, una estona després, els servidors d'IONOS encara donaven 217.160.0.2 per als tres. Cal comprovar:

```
dig +short @ns1102.ui-dns.de appinv1.tecnocat.eu
dig +short @ns1102.ui-dns.de appinv2.tecnocat.eu
dig +short @ns1102.ui-dns.de www.linkat.tecnocat.eu
```

- Si no surt res, ja estan esborrats i això està acabat.
- Si encara surt 217.160.0.2, és que no es va arribar a desar. Cal tornar a la taula de DNS de tecnocat.eu a IONOS, prémer "Restablecer filtro" per veure tots els registres, esborrar els A d'`appinv1`, `appinv2` i `www.linkat`, i assegurar-se que es desa.
- Els registres de `linkat` (sense www) no s'han de tocar, perquè fan la redirecció.

També cal comprovar que http://linkat.tecnocat.eu/ continua portant a https://tecnocat.eu/linkat/.

## Què queda pendent

1. Mirar si algú fa servir el correu @tecnocat.eu. Al panell d'IONOS (https://my.ionos.es), mirar si hi ha bústies creades. El domini té el correu a IONOS (registres MX a mx00.ionos.es i mx01.ionos.es, i també n'hi ha a `linkat` i `apps`). No s'ha de tocar cap registre MX, TXT, `_dmarc`, `_domainkey` ni `autodiscover`.
2. tecnocat2019.tecnocat.eu encara mostra el WordPress antic. De moment es deixa així, per poder-hi entrar si cal. Quan ja no calgui, a "Subdominios" se li ha de posar una redirecció (HTTP o 301, no "con frame") cap a https://tecnocat.eu/, conservant la ruta si IONOS ho permet. Era l'adreça del WordPress antic i hi ha enllaços com tecnocat2019.tecnocat.eu/tecnologia/robotica que la web nova ja sap redirigir.
3. Canviar el contracte d'IONOS a "només domini" o cancel·lar l'allotjament. Només quan estiguin fets els punts 1 i 2. Abans, si vols, baixa una còpia del WordPress des del panell. Mantenir només el domini costa entre 5 i 15 € l'any. Quan es cancel·li l'allotjament, també es poden esborrar els registres `ftp`, `apps` i `www.apps`, que apunten a 217.160.0.2.
4. Treure la versió antiga d'IA que encara surt a https://tecnocat.eu/ia-antic/. Al repositori `webtecnocat/ia-antic`, Settings › Actions › General, desactivar les Actions, o a Settings › Pages fer "Unpublish site". El repositori no s'ha d'esborrar, i no se li ha de tornar a posar el nom `ia`, perquè llavors tornaria a tapar /ia/.
5. Decidir què es fa amb el repositori `Web` (https://tecnocat.eu/Web/), una altra web d'eXeLearning sobre Linkat, Epoptes, impressores, pissarres digitals i serveis del Departament. No és dins la web nova. Es pot deixar com està, posar-hi un enllaç des del menú o integrar-la com `ia` i `linkat`. No se'n pot desactivar la publicació si no s'ha integrat abans.
6. Esborrar la carpeta `web/` de l'ordinador. És la versió antiga de `docs/` i no es puja a GitHub: `rm -rf ~/Gemini/tecnocat/web`
7. Posar una contrasenya nova a la compte webtecnocat de GitHub ("Forgot password", que l'envia a tecnocat.eu@gmail.com). Ara només s'hi pot entrar amb Google.

bloc.tecnocat.eu és una redirecció amb frame cap a http://tecnocat.blogspot.com. No depèn de l'allotjament i es pot deixar.

## Com es canvia la web

Dins de `~/Gemini/tecnocat`: editar els originals o `eines/construeix.py`, executar `python3 eines/construeix.py` i després `git add -A`, `git commit -m "..."` i `git push`. Es puja amb la compte webtecnocat per SSH (àlies `github-webtecnocat`), sense tocar la de cap d'estudis. Més detalls al README.

## Configuració actual (per si cal refer-la)

DNS de tecnocat.eu a IONOS:

- `@`: quatre registres A, 185.199.108.153, 185.199.109.153, 185.199.110.153 i 185.199.111.153.
- `www`: CNAME cap a `webtecnocat.github.io`.
- `linkat`: redirecció d'IONOS cap a https://tecnocat.eu/linkat/ (a "Subdominios").

GitHub, repositori `webtecnocat/webtecnocat.github.io`, Settings › Pages: "Deploy from a branch", branca `main`, carpeta `/docs`, domini `tecnocat.eu` i "Enforce HTTPS" activat. El fitxer `docs/CNAME` el crea l'script perquè `URL_WEB` és `https://tecnocat.eu/`.
