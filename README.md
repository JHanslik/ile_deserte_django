# L'Île Perdue - Jeu de Survie

Un jeu d'aventure textuel où vous devez survivre sur une île déserte après un crash d'avion.

## Lancement du jeu

1. Assurez-vous d'avoir Python 3.8+ et Django installés
2. Exécutez la commande suivante pour lancer le serveur :

```bash
python manage.py runserver
```

3. Accédez au jeu dans votre navigateur à l'adresse http://127.0.0.1:8000/

## Nouvelles fonctionnalités

### Système de progression amélioré

- Barre de progression visuelle montrant votre avancement dans le jeu
- Notifications de progression tous les 20% pour vous tenir informé
- Deux chemins vers la victoire : atteindre un scénario de fin OU progression à 100%
- Chaque changement de scénario augmente la progression de 5%

### Équilibrage des statistiques

- Les statistiques diminuent maintenant bien plus lentement pour une expérience moins frustrante :
  - Faim : -0.3 par action (au lieu de -1)
  - Énergie : -0.2 par action (au lieu de -0.5)
  - Moral : -0.2 uniquement en cas de faim ou énergie faible
- Chaque action a un impact mesuré sur la faim, l'énergie et le moral
- Les effets des choix sont clairement affichés avant de les sélectionner
- Indicateurs visuels colorés pour l'état de vos statistiques (vert, jaune, rouge)

### Scénarios enrichis

- Plus de 11 scénarios différents à explorer
- Nombreux choix avec des conséquences variées
- Différentes stratégies de survie possibles

### Installation des nouveaux scénarios

Pour installer les nouveaux scénarios, exécutez :

```bash
python manage.py dbshell < scenarios.sql
```

## Comment jouer

- Vous êtes échoué sur une île déserte et devez survivre
- Chaque choix que vous faites affecte vos statistiques (faim, énergie, moral)
- Si l'énergie tombe à zéro, vous perdez la partie
- Certains objets peuvent être récupérés et utilisés pour débloquer des options
- L'objectif est de survivre et de trouver un moyen de quitter l'île
- Consultez le fichier `astuces_joueurs.md` pour des conseils détaillés

## Lieux à explorer

- La plage de départ
- Une jungle dense avec des fruits
- Une grotte mystérieuse
- Le sommet d'une colline avec vue sur l'île
- Une cabane abandonnée
- Un marécage avec des plantes médicinales
- Une épave de bateau
- Un ancien campement
- Des ruines mystérieuses
- Une falaise côtière avec vue sur l'horizon

## Stratégies

- **Survie de base** : Concentrez-vous sur la nourriture et le repos
- **Exploration** : Découvrez les secrets de l'île
- **Construction** : Créez des abris pour améliorer votre situation
- **Évasion** : Cherchez un moyen de quitter l'île

## Fonctionnalités

- Système de statistiques et d'inventaire
- Progression narrative avec fin atteignable
- Interface intuitive avec retours visuels
- Plusieurs fins possibles selon vos choix
- Notifications pour les événements importants

## Technologies

- Backend : Django/Python
- Frontend : JavaScript
- Base de données : SQLite
