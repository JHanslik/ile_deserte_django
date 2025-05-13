from django.contrib import admin
from .models import Scenario, Choix, JoueurState

@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'texte', 'created_at', 'updated_at')
    search_fields = ('texte',)
    list_filter = ('created_at', 'updated_at')

@admin.register(Choix)
class ChoixAdmin(admin.ModelAdmin):
    list_display = ('texte', 'scenario', 'delta_faim', 'delta_energie', 'delta_moral', 'scenario_suivant')
    list_filter = ('scenario', 'scenario_suivant')
    search_fields = ('texte',)

@admin.register(JoueurState)
class JoueurStateAdmin(admin.ModelAdmin):
    list_display = ('user', 'scenario_actuel', 'faim', 'energie', 'moral')
    list_filter = ('scenario_actuel',)
    search_fields = ('user__username',)
