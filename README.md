# Weakness - Archive Password Cracker

Un outil puissant pour craquer les mots de passe d'archives (ZIP, RAR, PDF) en utilisant deux méthodes : brute force et attaque par dictionnaire.

## Fonctionnalités

- 🔓 Cracking de fichiers ZIP
- 🔓 Cracking de fichiers RAR
- 🔓 Cracking de fichiers PDF
- 💪 Brute force (toutes les combinaisons possibles)
- 📚 Attaque par dictionnaire (liste de mots)
- 💻 Interface CLI (ligne de commande)
- 🖥️ Interface GUI (graphique)
- 📊 Logs et progression en temps réel

## Installation

```bash
git clone https://github.com/N9uf-S/Weakness-.git
cd Weakness-
pip install -r requirements.txt
```

## Utilisation

### CLI
```bash
python main.py -f archive.zip -m dictionary -d wordlist.txt
```

### GUI
```bash
python gui.py
```

## Méthodes supportées

- **Brute Force** : Essaie toutes les combinaisons possibles
- **Dictionnaire** : Utilise une liste de mots prédéfinis

## Formats supportés

- ZIP
- RAR
- PDF

## Langage

- Python 3.8+

## Auteur

N9uf_S

## Licence

MIT