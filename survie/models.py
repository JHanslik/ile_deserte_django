from django.db import models
from django.contrib.auth.models import User

class Scenario(models.Model):
    texte = models.TextField(verbose_name="Description du scénario")
    est_debut = models.BooleanField(default=False, verbose_name="Est le scénario de début")
    est_fin = models.BooleanField(default=False, verbose_name="Est un scénario de fin")
    requiert_objet = models.CharField(max_length=100, blank=True, null=True, verbose_name="Objet requis pour ce scénario")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scénario {self.id}: {self.texte[:50]}..."

    class Meta:
        verbose_name = "Scénario"
        verbose_name_plural = "Scénarios"

class Choix(models.Model):
    scenario = models.ForeignKey(
        Scenario, 
        on_delete=models.CASCADE, 
        related_name='choix',
        verbose_name="Scénario associé"
    )
    texte = models.CharField(max_length=200, verbose_name="Description du choix")
    delta_faim = models.IntegerField(default=0, verbose_name="Impact sur la faim")
    delta_energie = models.IntegerField(default=0, verbose_name="Impact sur l'énergie")
    delta_moral = models.IntegerField(default=0, verbose_name="Impact sur le moral")
    ajoute_objet = models.CharField(max_length=100, blank=True, null=True, verbose_name="Objet ajouté à l'inventaire")
    requiert_objet = models.CharField(max_length=100, blank=True, null=True, verbose_name="Objet requis pour ce choix")
    scenario_suivant = models.ForeignKey(
        Scenario, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='choix_menant_ici',
        verbose_name="Scénario suivant"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.texte

    class Meta:
        verbose_name = "Choix"
        verbose_name_plural = "Choix"

class JoueurState(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Joueur"
    )
    scenario_actuel = models.ForeignKey(
        Scenario, 
        on_delete=models.SET_NULL, 
        null=True,
        verbose_name="Scénario actuel"
    )
    faim = models.IntegerField(default=100, verbose_name="Niveau de faim")
    energie = models.IntegerField(default=100, verbose_name="Niveau d'énergie")
    moral = models.IntegerField(default=100, verbose_name="Niveau de moral")
    inventaire = models.JSONField(default=list, blank=True, verbose_name="Inventaire du joueur")
    scenarios_visites = models.JSONField(default=list, blank=True, verbose_name="Scénarios déjà visités")
    progression = models.IntegerField(default=0, verbose_name="Progression dans l'histoire (0-100)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"État de {self.user.username}"

    class Meta:
        verbose_name = "État du joueur"
        verbose_name_plural = "États des joueurs"
