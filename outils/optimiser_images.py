"""Décline les images du site aux largeurs où elles s'affichent.

    python3 outils/optimiser_images.py

Pour chaque photo de assets/images/ (le .jpg d'origine), écrit à côté :
  - <nom>-<largeur>.avif aux largeurs de LARGEURS_AVIF : le format que
    lisent tous les navigateurs actuels, près de deux fois plus léger que
    le WebP à qualité égale ;
  - <nom>-<largeur>.webp aux largeurs de LARGEURS_WEBP : la relève des
    navigateurs sans AVIF.
Une photo plus étroite que la plus grande largeur est aussi déclinée à
sa propre largeur. Pour chaque logo de partenaire (.png), un seul WebP
sans perte, à la largeur où il s'affiche, trois fois.

Le script n'écrit que ce qui manque : on le relance sans crainte après
avoir ajouté une photo. Pour refaire la déclinaison d'une photo
remplacée, effacer d'abord ses fichiers <nom>-<largeur>.*
L'assemblage (outils/images.py) trouve les fichiers par leur nom et
les sert dans un <picture> ; une variante absente est simplement
omise.
"""

import os
import sys

from PIL import Image, features

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "assets", "images")

# 240 : les vignettes (72 à 112 px affichés, jusqu'à trois pixels par
# point). 720 et 1280 : les téléphones à écran dense, entre deux paliers.
LARGEURS_AVIF = (240, 480, 720, 960, 1280, 1600)
LARGEURS_WEBP = (240, 480, 960, 1600)
# La qualité AVIF se lit sur une autre échelle que celle du WebP :
# 55 rend une photo de chantier sans différence visible avec le WebP à
# 80, pour 45 % d'octets en moins. Les petites tailles montrent plus
# vite leurs défauts : un cran au-dessus.
QUALITE_AVIF = 55
QUALITE_AVIF_PETITE = 62
QUALITE_WEBP = 80
LOGO_LARGEUR = 480

# Un Pillow trop ancien n'écrit pas l'AVIF : le WebP seul, alors.
AVIF = features.check("avif")

# Images qui ne sont pas des photos affichées : l'aperçu de partage
# (lu par les réseaux, en entier) et les icônes.
EXCLUES = {"partage.jpg", "logo.png", "icone-192.png", "icone-512.png"}


def largeurs(ladder, largeur_origine):
    """Les paliers que la photo peut fournir, plus sa propre largeur si
    elle tombe entre deux."""
    retenues = [l for l in ladder if l < largeur_origine]
    if largeur_origine <= ladder[-1]:
        retenues.append(largeur_origine)
    else:
        retenues.append(ladder[-1])
    return sorted(set(retenues))


def a_refaire(cible, source):
    # Sur l'existence seule : les dates des fichiers ne survivent pas à
    # un clonage git, et une déclinaison refaite pour rien changerait le
    # dépôt sans rien changer à l'image.
    return not os.path.exists(cible)


def reduire(image, largeur):
    if largeur == image.width:
        return image
    hauteur = max(1, round(image.height * largeur / image.width))
    return image.resize((largeur, hauteur), Image.Resampling.LANCZOS)


def ecrire(image, chemin, format_, **options):
    temporaire = chemin + ".part"
    image.save(temporaire, format_, **options)
    os.replace(temporaire, chemin)


def decliner_photo(nom):
    source = os.path.join(DOSSIER, nom)
    tronc = os.path.splitext(source)[0]
    faites = []
    with Image.open(source) as ouverte:
        profil = ouverte.info.get("icc_profile")
        image = ouverte.convert("RGB")
    commun = {"icc_profile": profil} if profil else {}
    for largeur in largeurs(LARGEURS_AVIF, image.width) if AVIF else ():
        cible = "%s-%d.avif" % (tronc, largeur)
        if a_refaire(cible, source):
            qualite = QUALITE_AVIF_PETITE if largeur <= 480 else QUALITE_AVIF
            ecrire(reduire(image, largeur), cible, "AVIF",
                   quality=qualite, speed=4, **commun)
            faites.append(os.path.basename(cible))
    for largeur in largeurs(LARGEURS_WEBP, image.width):
        cible = "%s-%d.webp" % (tronc, largeur)
        if a_refaire(cible, source):
            ecrire(reduire(image, largeur), cible, "WEBP",
                   quality=QUALITE_WEBP, method=6, **commun)
            faites.append(os.path.basename(cible))
    return faites


def decliner_logo(nom):
    source = os.path.join(DOSSIER, nom)
    with Image.open(source) as ouverte:
        image = ouverte.convert("RGBA")
    largeur = min(LOGO_LARGEUR, image.width)
    cible = "%s-%d.webp" % (os.path.splitext(source)[0], largeur)
    if not a_refaire(cible, source):
        return []
    ecrire(reduire(image, largeur), cible, "WEBP", lossless=True, method=6)
    return [os.path.basename(cible)]


def main():
    if not AVIF:
        print("Pillow n'écrit pas l'AVIF ici (pip install -U Pillow) : WebP seul.")
    total = []
    for nom in sorted(os.listdir(DOSSIER)):
        if nom in EXCLUES:
            continue
        if nom.endswith(".jpg"):
            faites = decliner_photo(nom)
        elif nom.startswith("logo-") and nom.endswith(".png"):
            faites = decliner_logo(nom)
        else:
            continue
        if faites:
            print("%s : %s" % (nom, ", ".join(faites)))
        total += faites
    print("%d fichier(s) écrit(s)." % len(total) if total
          else "Rien à refaire : toutes les déclinaisons sont à jour.")


if __name__ == "__main__":
    sys.exit(main())
