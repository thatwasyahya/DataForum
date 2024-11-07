# DataForum

DataForum est un outil d'analyse et de visualisation des statistiques des forums, conçu pour comparer et afficher les performances de différents forums en fonction de divers critères. Il permet aux utilisateurs de sélectionner des forums, de comparer leurs données et de visualiser les résultats sous forme de graphiques interactifs.

Vous pouvez consulter la version en ligne du projet ici : [DataForum - Live](https://thatwasyahya.github.io/DataForum/)

## Fonctionnalités

- **Comparaison de forums** : Sélectionnez deux forums pour les comparer en temps réel sur un même graphique.
- **Top 3 Forums** : Affichez un graphique pour les trois forums ayant les meilleures performances, en fonction de leur score de qualité.
- **Visualisation interactive** : Utilisation de Highcharts pour créer des graphiques polaires interactifs.
- **Sélection dynamique** : Utilisez des listes déroulantes pour sélectionner les forums et les comparer facilement.

## Installation

### Prérequis

Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- [Git](https://git-scm.com/)
- Un éditeur de texte, tel que [VS Code](https://code.visualstudio.com/)

### Cloner le projet

Clonez ce dépôt sur votre machine locale en utilisant la commande suivante :

```bash
git clone https://github.com/thatwasyahya/DataForum.git
```

### Ouvrir le projet

Une fois le projet cloné, ouvrez le répertoire du projet dans votre éditeur de texte préféré.

```bash
cd DataForum
```

### Lancer le projet

Le projet est une application statique utilisant HTML, CSS et JavaScript, il n'y a donc pas besoin d'un serveur pour le faire fonctionner. Vous pouvez simplement ouvrir le fichier `index.html` dans votre navigateur.

```bash
open index.html
```

Ou, si vous préférez un serveur local, vous pouvez utiliser des outils comme [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) dans VS Code.

## Utilisation

1. Accédez à l'interface du projet via l'URL locale ou en ligne : [DataForum - Live](https://thatwasyahya.github.io/DataForum/).
2. Utilisez les menus déroulants en haut de la page pour sélectionner les forums que vous souhaitez comparer.
3. Le graphique principal se mettra à jour en temps réel pour comparer les deux forums sélectionnés.
4. En dessous du graphique, vous trouverez les trois forums ayant les meilleures performances, affichés sous forme de graphiques interactifs.

## Structure du projet

- `index.html` :
  - Le fichier principal HTML contenant la structure de l'application.
  - Les styles CSS pour la mise en page et l'apparence.
  - Le code JavaScript qui gère la logique de l'application et les graphiques Highcharts.
- `forum_stats.csv` : Le fichier CSV contenant les données des forums à analyser.
- `traceforum.csv` : Le fichier CSV contenant la table transitions.
- `traceforum.sql` : Le fichier SQL contenant la database avec toutes les tables et les forums.

## Contribuer

1. Fork ce dépôt.
2. Créez une branche pour vos changements : `git checkout -b feature/ma-nouvelle-fonctionnalité`.
3. Faites vos modifications et committez-les : `git commit -am 'Ajout d'une nouvelle fonctionnalité'`.
4. Poussez vos changements vers votre branche : `git push origin feature/ma-nouvelle-fonctionnalité`.
5. Ouvrez une Pull Request pour proposer vos modifications.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Remerciements

- [Highcharts](https://www.highcharts.com/) pour la création de graphiques interactifs.
- [GitHub Pages](https://pages.github.com/) pour l'hébergement de l'application en ligne.
