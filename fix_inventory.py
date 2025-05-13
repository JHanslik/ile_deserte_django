import os
import django
import sys

# Configuration de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ile_perdue.settings')
django.setup()

# Import des modèles
from survie.models import JoueurState, Choix
from django.contrib.auth.models import User
import logging

# Configurer le logger
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(asctime)s %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('fix_inventory.log')
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Vérifier et corriger les inventaires des joueurs"""
    
    # Récupérer tous les joueurs
    joueurs = JoueurState.objects.all()
    logger.info(f"Nombre de joueurs trouvés: {joueurs.count()}")
    
    for joueur in joueurs:
        logger.info(f"Traitement du joueur: {joueur.user.username}")
        logger.info(f"État actuel - Inventaire: {joueur.inventaire}")
        
        # S'assurer que l'inventaire et scenarios_visites ne sont pas None
        if joueur.inventaire is None:
            joueur.inventaire = []
            logger.info("Inventaire initialisé à une liste vide")
        
        if joueur.scenarios_visites is None:
            joueur.scenarios_visites = []
            logger.info("Scenarios visités initialisé à une liste vide")
        
        # Vérifier si l'utilisateur a visité des scénarios qui donnent des objets
        choix_objets = Choix.objects.exclude(ajoute_objet__isnull=True).exclude(ajoute_objet='')
        
        for choix in choix_objets:
            scenario_id = choix.scenario_id
            
            # Si le joueur a visité ce scénario, il devrait avoir l'objet
            if scenario_id in joueur.scenarios_visites:
                objet = choix.ajoute_objet
                
                # Vérifier si l'objet est dans l'inventaire
                if objet and objet not in joueur.inventaire:
                    logger.info(f"Ajout de l'objet manquant '{objet}' à l'inventaire")
                    joueur.inventaire.append(objet)
                    
        # Sauvegarder les modifications
        joueur.save()
        logger.info(f"État après mise à jour - Inventaire: {joueur.inventaire}")
        
    logger.info("Traitement terminé")

if __name__ == "__main__":
    main() 