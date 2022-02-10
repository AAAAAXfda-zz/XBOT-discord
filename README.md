[![wakatime](https://wakatime.com/badge/github/HerbeMalveillante/MMOBOT-V3.svg)](https://wakatime.com/badge/github/HerbeMalveillante/MMOBOT-V3)
![lines count badge](https://img.shields.io/tokei/lines/github/herbemalveillante/MMOBOT-V3)
![commit activity badge](https://img.shields.io/github/commit-activity/m/herbemalveillante/MMOBOT-V3)
![last commit badge](https://img.shields.io/github/last-commit/herbemalveillante/MMOBOT-V3)
![code size badge](https://img.shields.io/github/languages/code-size/herbemalveillante/MMOBOT-V3)
![language count badge](https://img.shields.io/github/languages/count/herbemalveillante/MMOBOT-V3)
![top language badge](https://img.shields.io/github/languages/top/herbemalveillante/MMOBOT-V3)
![discord server badge](https://img.shields.io/discord/799331612918939688)

# XBOT-V3
XBOT, mais en nouveau et en mieux (et en français !).

## Quels sont les enjeux de ce projet ?

XBOT v1 était un bot Discord que j'ai créé afin de fournir une experience de MMORPG directement sur discord.
Malheureusement, le bot n'est pas très fun et j'ai du arrêter le développement par manque de temps, le laissant dans un état où il n'est ni fun à jouer, ni terminé. 

Récemment, le développeur de la librairie discord.py, Danny, a annoncé qu'il mettait fin aux mises à jour de la librairie, rendant difficile voir impossible l'implémentation des commandes slash, et rendant la majorité des bots codés avec la librairie inutilisables d'ici avril 2022.

J'ai donc décidé d'utiliser ces contraintes comme un nouveau départ et de recréer MMOBOT en javascript avec la librairie discord.js V13, me permettant non seulement de revoir complètement le gameplay, mais également d'implémenter les commandes slash, les boutons et les barres de menus. Je comptais également mettre en place le bot en français uniquement dans un premier temps.

Seulement, ce changement me demandait d'apprendre le JavaScript, que je ne connais pas complètement, c'était donc un gros projet très chronophage.

Récemment, je suis tombé sur deux modules qui m'ont fait réaliser que recoder MMOBOT en Python était finalement possible : disnake et tinydb. Grâce à disnake, un fork de discord.py qui implémente toutes les nouvelles fonctionnalités de l'API discord, je peux créer un bot sans risque de le voir mourir en avril 2022. Grâce à tinydb, je peux créer une base de données beaucoup plus facilement qu'avec sqlite (que j'utilisais pour la première version) qui me servira pendant toute la phase de développement, avant d'avoir besoin d'utiliser quelque chose de plus robuste.

J'ai donc décidé de tenter de recoder au moins le début de ce que j'ai prévu pour MMOBOT V2 en python grâce à ces librairies, pour voir si c'est plus réalisable qu'en JavaScript. Ce projet s'appelle donc MMOBOT-V3.

## Comment lancer le bot ?

Je déconseille de host le bot vous même, vaut mieux inviter le bot sur votre serveur. Toutefois, si vous voulez vraiment lancer une copie du bot vous même, créez simplement un fichier `token.txt` à la racine du répertoire et mettez votre token dedans. Vous devez également créer un fichier nommé `mail_secret.txt` dans lequel vous devez mettre un mot de passe d'application GMAIL. Attention à bien modifier le fichier `alert.py` pour que le mot de passe corresponde à l'adresse mail que vous voulez utiliser. La base de données se crééra automatiquement quand vous lancerez le fichier `main.py`.


## TODO

### Base de données

- [x] Mettre en place la base de données
- [ ] Ajouter tous les bindings de façon opti


### Town

- [x] Faire le /town
- [x] Pouvoir afficher la ville de quelqu'un d'autre avec un argument
- [ ] Mettre en place une formule permettant de calculer le prix à l'amélioration de chaque bâtiment (ou bien le hardcoder à la main ?)
- [ ] Pouvoir sélectionner un bâtiment pour voir ses stats (remplissage, niveau, prix à l'amélioration, dernière amélioration, etc)
- [ ] Pouvoir améliorer un bâtiment.
- [ ] Ajouter les boosts passifs des bâtiments à boost
- [ ] Créer les sprites des bâtiments (0/90)
- [ ] Implémenter les sprites des bâtiments pour les afficher dans le /town
- [ ] Implémenter l'overview du village


### fish

- [ ] ajouter la possibilité de pêcher des poissons.
- [ ] ajouter la possibilité de voir ses poissons de façon stylée
- [ ] ajouter des sprites / noms pour les poissons
- [ ] ajouter la possibilité d'améliorer ses poissons avec le /trade.


### Stats

- [ ] Mettre en place le tracking du nombre de joueurs et du nombre de serveurs. On peut aussi traquer plein d'autres choses : le nombre de ressources cumulées, de commandes tapées, etc. Logger le maximum de choses. Tout mettre dans un giga fichier csv qui se met à jour toutes les heures.
- [ ] Mettre en place un moyen de visualiser l'uptime du bot sur le dernier mois, la dernière semaine, ou le temps cumulé en uptime.
- [x] Ajouter la commande de stats

### Gameplay

- [ ] Faire en sorte que les bâtiments de ressources se remplissent tout seuls


### Upgrade

- [x] Mettre en place les quatre statistiques du personnage dans la base de données
- [x] Ajouter la canne à pêche
- [ ] Ajouter la possibilité d'améliorer les statistiques et la canne à pêche.

```python
# >o)
# (_> HM
```