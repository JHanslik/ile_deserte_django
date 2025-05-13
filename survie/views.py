from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Scenario, Choix, JoueurState
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import logging

# Configurer le logger
logger = logging.getLogger('survie')

# Create your views here.

# Obtenir l'utilisateur anonyme ou créer un nouvel utilisateur anonyme
def get_or_create_anonymous_user(request):
    if request.user.is_authenticated:
        return request.user
    
    # Si session_key n'existe pas, Django en créera une automatiquement lors de l'accès
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key
    
    username = f"anonymous_{session_key}"
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'email': f"{username}@example.com",
            'password': 'unusable_password'  # Ces utilisateurs ne se connecteront jamais directement
        }
    )
    
    return user

@require_POST
def choisir_action(request, scenario_id, choix_id):
    # Récupérer le scénario et le choix
    scenario = get_object_or_404(Scenario, id=scenario_id)
    choix = get_object_or_404(Choix, id=choix_id, scenario=scenario)
    
    # Récupérer ou créer l'utilisateur anonyme et son état
    user = get_or_create_anonymous_user(request)
    
    # Récupérer ou créer l'état du joueur
    joueur_state, created = JoueurState.objects.get_or_create(
        user=user,
        defaults={
            'scenario_actuel': Scenario.objects.filter(est_debut=True).first() or scenario,
            'faim': 100,
            'energie': 100,
            'moral': 100,
            'inventaire': [],
            'scenarios_visites': []
        }
    )
    
    # Log pour déboggage
    logger.info(f"État avant choix - User: {user.username}, Inventaire: {joueur_state.inventaire}")
    
    # Vérifier si le joueur a l'objet requis
    if choix.requiert_objet and choix.requiert_objet not in joueur_state.inventaire:
        # Vérifier si c'est un cas de plusieurs objets requis
        objets_requis = [o.strip() for o in choix.requiert_objet.split(',')]
        if not all(obj in joueur_state.inventaire for obj in objets_requis):
            return JsonResponse({
                "erreur": f"Vous avez besoin de {', '.join(objets_requis)} pour faire ce choix."
            }, status=400)
    
    # Appliquer les effets du choix
    joueur_state.faim = max(0, min(100, joueur_state.faim + choix.delta_faim))
    joueur_state.energie = max(0, min(100, joueur_state.energie + choix.delta_energie))
    joueur_state.moral = max(0, min(100, joueur_state.moral + choix.delta_moral))
    
    # Ajouter l'objet à l'inventaire si nécessaire
    if choix.ajoute_objet and choix.ajoute_objet not in joueur_state.inventaire:
        logger.info(f"Ajout d'objet à l'inventaire: {choix.ajoute_objet}")
        # Vérifier si inventaire est None ou non initialisé
        if joueur_state.inventaire is None:
            joueur_state.inventaire = []
        
        # Ajouter l'objet
        joueur_state.inventaire.append(choix.ajoute_objet)
        logger.info(f"Objet ajouté: {choix.ajoute_objet}")
    
    # Ajouter ce scénario aux scénarios visités
    if scenario.id not in joueur_state.scenarios_visites:
        # Vérifier si scenarios_visites est None ou non initialisé
        if joueur_state.scenarios_visites is None:
            joueur_state.scenarios_visites = []
            
        joueur_state.scenarios_visites.append(scenario.id)
    
    # Mettre à jour le scénario actuel
    if choix.scenario_suivant:
        # Vérifier si le scénario suivant requiert un objet
        if choix.scenario_suivant.requiert_objet and choix.scenario_suivant.requiert_objet not in joueur_state.inventaire:
            # Vérifier si c'est un cas de plusieurs objets requis
            objets_requis = [o.strip() for o in choix.scenario_suivant.requiert_objet.split(',')]
            if not all(obj in joueur_state.inventaire for obj in objets_requis):
                return JsonResponse({
                    "erreur": f"Vous avez besoin de {', '.join(objets_requis)} pour accéder à cet endroit."
                }, status=400)
        
        joueur_state.scenario_actuel = choix.scenario_suivant
        
        # Mettre à jour la progression si c'est un scénario clé
        # Exemple simple: la progression augmente en fonction du nombre de scénarios différents visités
        total_scenarios = Scenario.objects.count()
        joueur_state.progression = min(100, int((len(joueur_state.scenarios_visites) / total_scenarios) * 100))
    
    # Log après modification
    logger.info(f"État après choix - User: {user.username}, Inventaire: {joueur_state.inventaire}")
    
    # Sauvegarder les modifications
    try:
        joueur_state.save()
        logger.info(f"État sauvegardé avec succès - User: {user.username}, Inventaire: {joueur_state.inventaire}")
    except Exception as e:
        logger.error(f"Erreur lors de la sauvegarde - User: {user.username}, Erreur: {str(e)}")
        return JsonResponse({"erreur": "Erreur de sauvegarde"}, status=500)
    
    # Vérifier après sauvegarde que l'inventaire est bien mis à jour
    joueur_state_apres = JoueurState.objects.get(user=user)
    logger.info(f"État après sauvegarde (DB) - User: {user.username}, Inventaire: {joueur_state_apres.inventaire}")
    
    # Log après sauvegarde
    logger.info(f"État après sauvegarde - User: {user.username}, Inventaire: {joueur_state.inventaire}")
    
    # Vérifier les conditions de fin du jeu
    game_over = False
    victory = False
    
    # Fin par manque de ressources
    if joueur_state.faim <= 0 or joueur_state.energie <= 0 or joueur_state.moral <= 0:
        game_over = True
    
    # Victoire si on atteint un scénario de fin
    if joueur_state.scenario_actuel.est_fin:
        game_over = True
        victory = True
    
    # Préparer la réponse
    response_data = {
        "message": choix.texte,
        "etat": {
            "faim": joueur_state.faim,
            "energie": joueur_state.energie,
            "moral": joueur_state.moral,
            "inventaire": joueur_state.inventaire,
            "progression": joueur_state.progression
        },
        "game_over": game_over,
        "victory": victory
    }
    
    # Ajouter les informations du scénario suivant si disponible
    if choix.scenario_suivant:
        response_data["suivant"] = {
            "id": choix.scenario_suivant.id,
            "texte": choix.scenario_suivant.texte
        }
    
    return JsonResponse(response_data)

def game_view(request):
    # Récupérer ou créer l'utilisateur anonyme et son état
    user = get_or_create_anonymous_user(request)
    
    # Récupérer ou créer l'état du joueur
    joueur_state, created = JoueurState.objects.get_or_create(
        user=user,
        defaults={
            'scenario_actuel': Scenario.objects.filter(est_debut=True).first() or Scenario.objects.first(),
            'faim': 100,
            'energie': 100,
            'moral': 100,
            'inventaire': [],
            'scenarios_visites': []
        }
    )
    
    # Si c'est une nouvelle partie, commencer par le scénario de début
    if created:
        debut_scenario = Scenario.objects.filter(est_debut=True).first()
        if debut_scenario:
            joueur_state.scenario_actuel = debut_scenario
            joueur_state.save()
    
    return render(request, 'survie/game.html')

def scenario_view(request, scenario_id):
    try:
        # Récupérer l'utilisateur et son état
        user = get_or_create_anonymous_user(request)
        joueur_state, created = JoueurState.objects.get_or_create(
            user=user,
            defaults={
                'scenario_actuel': Scenario.objects.get(id=scenario_id),
                'faim': 100,
                'energie': 100,
                'moral': 100,
                'inventaire': [],
                'scenarios_visites': [scenario_id]
            }
        )
        
        scenario = Scenario.objects.get(id=scenario_id)
        choix_disponibles = []
        
        # Récupérer l'inventaire du frontend s'il est envoyé
        # Format attendu : ?inventaire=Bois sec,Pierre à feu
        frontend_inventaire = request.GET.get('inventaire', '')
        if frontend_inventaire:
            # Convertir en liste
            inventaire_joueur = [item.strip() for item in frontend_inventaire.split(',') if item.strip()]
            logger.info(f"Inventaire reçu du frontend: {inventaire_joueur}")
        else:
            # Sinon utiliser l'inventaire de la base de données
            inventaire_joueur = joueur_state.inventaire or []
            logger.info(f"Utilisation de l'inventaire de la BDD: {inventaire_joueur}")
        
        # Log pour déboggage
        logger.info(f"Scenario view - User: {user.username}, Scenario: {scenario_id}, Inventaire utilisé: {inventaire_joueur}")
        
        # Cas particulier pour le scénario 10 (colline)
        a_les_objets_pour_feu = False
        if scenario.id == 10:
            objets_victoire = ['Bois sec', 'Pierre à feu']
            # Vérifier si tous les objets requis sont dans l'inventaire (frontend ou BDD)
            a_les_objets_pour_feu = all(obj in inventaire_joueur for obj in objets_victoire)
            logger.info(f"Scenario colline - Inventaire: {inventaire_joueur}, A les objets pour feu: {a_les_objets_pour_feu}")
        
        # Filtrer les choix en fonction de l'inventaire du joueur
        for c in Choix.objects.filter(scenario=scenario):
            # Log pour déboggage des choix
            logger.info(f"Analyse choix id={c.id}, texte={c.texte}, requiert={c.requiert_objet}")
            
            if not c.requiert_objet:
                # Cas particulier : choix "Allumer un feu de signal (sans les bons objets)" sur la colline
                if scenario.id == 10 and 'sans les bons objets' in c.texte:
                    # On affiche ce choix uniquement si le joueur n'a pas tous les objets requis pour le vrai feu de signal
                    if not a_les_objets_pour_feu:
                        logger.info(f"Affiche choix 'sans les bons objets' car joueur n'a pas tous les objets")
                        choix_disponibles.append({
                            'id': c.id,
                            'description': c.texte,
                            'requiert': c.requiert_objet,
                            'effet_faim': c.delta_faim,
                            'effet_energie': c.delta_energie,
                            'effet_moral': c.delta_moral,
                            'ajoute_objet': c.ajoute_objet
                        })
                else:
                    choix_disponibles.append({
                        'id': c.id,
                        'description': c.texte,
                        'requiert': c.requiert_objet,
                        'effet_faim': c.delta_faim,
                        'effet_energie': c.delta_energie,
                        'effet_moral': c.delta_moral,
                        'ajoute_objet': c.ajoute_objet
                    })
            else:
                # Supporte plusieurs objets requis séparés par une virgule
                objets_requis = [o.strip() for o in c.requiert_objet.split(',')]
                logger.info(f"Objets requis: {objets_requis}, inventaire: {inventaire_joueur}")
                
                if all(obj in inventaire_joueur for obj in objets_requis):
                    logger.info(f"Condition remplie - ajout du choix id={c.id}")
                    choix_disponibles.append({
                        'id': c.id,
                        'description': c.texte,
                        'requiert': c.requiert_objet,
                        'effet_faim': c.delta_faim,
                        'effet_energie': c.delta_energie,
                        'effet_moral': c.delta_moral,
                        'ajoute_objet': c.ajoute_objet
                    })
        
        # Si on est sur le scénario de la colline, ajouter un log détaillé
        if scenario.id == 10:
            logger.info(f"Choix disponibles sur la colline: {[c['id'] for c in choix_disponibles]}")
        
        data = {
            'id': scenario.id,
            'description': scenario.texte,
            'est_fin': scenario.est_fin,  # Victoire/défaite uniquement par scénario de fin
            'choix': choix_disponibles,
            'etat': {
                'faim': joueur_state.faim,
                'energie': joueur_state.energie,
                'moral': joueur_state.moral,
                'inventaire': joueur_state.inventaire or [],  # On renvoie l'inventaire de la BDD ici
                'progression': joueur_state.progression
            }
        }
        return JsonResponse(data)
    except Scenario.DoesNotExist:
        return JsonResponse({'error': 'Scénario non trouvé'}, status=404)

def choix_view(request, choix_id):
    try:
        choix = Choix.objects.get(id=choix_id)
        data = {
            'id': choix.id,
            'effet_faim': choix.delta_faim,
            'effet_energie': choix.delta_energie,
            'effet_moral': choix.delta_moral,
            'ajoute_objet': choix.ajoute_objet,
            'requiert_objet': choix.requiert_objet,
            'prochain_scenario': choix.scenario_suivant.id if choix.scenario_suivant else None
        }
        return JsonResponse(data)
    except Choix.DoesNotExist:
        return JsonResponse({'error': 'Choix non trouvé'}, status=404)
