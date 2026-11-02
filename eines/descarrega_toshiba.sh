#!/bin/bash
# Exporta a PDF les presentacions de les carpetes Toshiba NB200 i NB250 (Drive de ci@iesmalgrat.cat).
# Fa servir GAM i no canvia cap permís dels fitxers.
# Ús:  bash eines/descarrega_toshiba.sh
set -e
DEST="$(cd "$(dirname "$0")/.." && pwd)/presentacions/toshiba"
mkdir -p "$DEST"
COMPTE=ci@iesmalgrat.cat
GAM=$(command -v gam || echo "$HOME/bin/gam7/gam")

baixa() {  # id nom
  "$GAM" user "$COMPTE" get drivefile "$1" format pdf targetfolder "$DEST" targetname "$2.pdf" overwrite true
}

baixa 1Uk6TWEovf4VrntQOADtblnfy-YrlGL2hPNxs4vLE680 acces-unitat-dades
baixa 1Dz4H1nAZILeRCjO8zCtLSzcjABtGLUBwg8rEyKG63zw arrancada-rapida-nb200
baixa 1hRwLqbjAHFrprjnXWEQGAGlT1x1Vs86z6t7UtxncJSM crear-nou-usuari
baixa 1Zm2kJlp7cuneW-JHVO-5pj0L0q9psMsJ89aEiioUwv0 tancar-aplicacio-linkat
baixa 1gev2pnAeTizfS9vGAwAfC-Na-JVWGgqNsrWswqYNK-k actualitzacio-linkat
baixa 1wcSGpeZYLxl_zmGHiQQXCYdmVNUul1J67_SweFWSmFQ cerca-mac
baixa 1pJuTRFNk6jDoLdCfEvUVzXhwRMiB8bGpOA4tdkJt2Hg restauracio-nb250
baixa 194n5Nr4TCgm91dRrFXLMsGwXbJadL9vS0p5L3I60KUo configuracio-wifi
baixa 1_wuyFQkDWHk2iTJWMBU6SlaiMDrc0fLYEJ3QRTIMtgs consideracions-linkat
baixa 1BBvSjMu0cU2UsAqN1AKsY6ObF27NhbDToUNXdeaCBAg fallada-windows-7
baixa 1hrWBcF1g2EpJtEnOX1-nf325sCHJ_KYZoTVZ9BJ5_oo tancar-pulseaudio
baixa 1XJ3_PEeojX1BSSbVRZe7HgQ-RbyDEZGUgpWujz485i4 clonezilla-usb
baixa 12EDdC_U0b2Kea1KSH7DElHL5on19oqL3HReFYqXZdK8 restauracio-toshiba-usb

ls -la "$DEST"

# Una imatge per diapositiva, per al visor de la web (cal pdftoppm, del paquet poppler-utils)
for pdf in "$DEST"/*.pdf; do
  dir="${pdf%.pdf}"
  rm -rf "$dir" && mkdir -p "$dir"
  pdftoppm -jpeg -jpegopt quality=82 -scale-to-x 800 -scale-to-y -1 "$pdf" "$dir/d"
done
