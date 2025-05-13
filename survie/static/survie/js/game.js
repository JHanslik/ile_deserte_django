class Game {
  constructor() {
    this.stats = {
      faim: 100,
      energie: 100,
      moral: 100,
    };
    this.inventaire = [];
    this.progression = 0;
    this.currentScenarioId = 1;
    this.initializeGame();
  }

  initializeGame() {
    this.updateStats();
    this.loadScenario(this.currentScenarioId);

    // Ajouter l'affichage de l'inventaire
    this.createInventoryDisplay();

    // Ajouter l'affichage de la progression
    this.createProgressionDisplay();
  }

  createInventoryDisplay() {
    // Créer le conteneur d'inventaire s'il n'existe pas déjà
    if (!document.querySelector(".inventory-container")) {
      const statsContainer = document.querySelector(".stats-container");

      const inventoryContainer = document.createElement("div");
      inventoryContainer.className = "inventory-container";

      const inventoryTitle = document.createElement("h3");
      inventoryTitle.textContent = "Inventaire";
      inventoryContainer.appendChild(inventoryTitle);

      const inventoryList = document.createElement("ul");
      inventoryList.id = "inventory-list";
      inventoryContainer.appendChild(inventoryList);

      // Insérer après les stats
      statsContainer.parentNode.insertBefore(inventoryContainer, statsContainer.nextSibling);
    }

    this.updateInventoryDisplay();
  }

  createProgressionDisplay() {
    // Créer le conteneur de progression s'il n'existe pas déjà
    if (!document.querySelector(".progression-container")) {
      const gameContainer = document.querySelector(".game-container");

      const progressionContainer = document.createElement("div");
      progressionContainer.className = "progression-container";

      const progressionTitle = document.createElement("h3");
      progressionTitle.textContent = "Progression";
      progressionContainer.appendChild(progressionTitle);

      const progressionBar = document.createElement("div");
      progressionBar.className = "progression-bar";

      const progressionFill = document.createElement("div");
      progressionFill.id = "progression-fill";
      progressionFill.className = "progression-fill";
      progressionBar.appendChild(progressionFill);

      const progressionValue = document.createElement("span");
      progressionValue.id = "progression-value";
      progressionValue.className = "progression-value";

      progressionContainer.appendChild(progressionBar);
      progressionContainer.appendChild(progressionValue);

      // Insérer au début du conteneur de jeu
      gameContainer.insertBefore(progressionContainer, gameContainer.firstChild);
    }

    this.updateProgressionDisplay();
  }

  updateInventoryDisplay() {
    const inventoryList = document.getElementById("inventory-list");
    if (inventoryList) {
      inventoryList.innerHTML = "";

      if (this.inventaire.length === 0) {
        const emptyItem = document.createElement("li");
        emptyItem.textContent = "Aucun objet";
        emptyItem.className = "empty-inventory";
        inventoryList.appendChild(emptyItem);
      } else {
        this.inventaire.forEach((item) => {
          const listItem = document.createElement("li");
          listItem.textContent = item;
          inventoryList.appendChild(listItem);
        });
      }
    }
  }

  updateProgressionDisplay() {
    const progressionFill = document.getElementById("progression-fill");
    const progressionValue = document.getElementById("progression-value");

    if (progressionFill && progressionValue) {
      progressionFill.style.width = `${this.progression}%`;
      progressionValue.textContent = `${this.progression}%`;
    }
  }

  updateStats() {
    Object.entries(this.stats).forEach(([stat, value]) => {
      const barElement = document.getElementById(`${stat}-bar`);
      const valueElement = document.getElementById(`${stat}-value`);
      const statContainer = document.querySelector(`.stat:has(#${stat}-bar)`);

      if (barElement && valueElement) {
        barElement.style.width = `${value}%`;
        valueElement.textContent = `${Math.round(value)}`;

        // Ajouter des classes pour indiquer visuellement l'état
        if (statContainer) {
          // Supprimer toutes les classes d'état existantes
          statContainer.classList.remove("danger", "warning", "good");

          // Ajouter la classe appropriée selon la valeur
          if (value <= 20) {
            statContainer.classList.add("danger");
            // Faire clignoter l'énergie si elle est critique (car c'est fatal)
            if (stat === "energie" && value <= 10) {
              statContainer.classList.add("blink");
            } else {
              statContainer.classList.remove("blink");
            }
          } else if (value <= 50) {
            statContainer.classList.add("warning");
            statContainer.classList.remove("blink");
          } else {
            statContainer.classList.add("good");
            statContainer.classList.remove("blink");
          }
        }
      }
    });

    // Mettre à jour l'inventaire et la progression
    this.updateInventoryDisplay();
    this.updateProgressionDisplay();
  }

  async loadScenario(scenarioId, keepStats = false) {
    try {
      const response = await fetch(`/api/scenario/${scenarioId}/`);
      const data = await response.json();

      // Mettre à jour le texte du scénario
      document.querySelector(".scenario-text").textContent = data.description;

      // Mettre à jour les stats si elles sont fournies et qu'on ne veut pas conserver les actuelles
      if (data.etat && !keepStats) {
        this.stats.faim = data.etat.faim;
        this.stats.energie = data.etat.energie;
        this.stats.moral = data.etat.moral;
        this.inventaire = data.etat.inventaire || [];
        this.progression = data.etat.progression || 0;
        this.updateStats();
      } else if (keepStats) {
        // Si on conserve les stats actuelles, mettre à jour uniquement l'inventaire et la progression
        if (data.etat) {
          this.inventaire = [...new Set([...this.inventaire, ...(data.etat.inventaire || [])])]; // Fusionner les inventaires
          // Afficher un message de progression au joueur tous les 20%
          const previousProgress = this.progression;
          this.progression = Math.max(this.progression, data.etat.progression || this.progression);

          // Si on atteint un seuil de progression (20%, 40%, 60%, 80%)
          if (Math.floor(previousProgress / 20) < Math.floor(this.progression / 20)) {
            this.showNotification(`Progression: ${Math.floor(this.progression / 20) * 20}% de l'aventure accomplie !`, "progression");
          }

          this.updateStats();
        }
      }

      // Afficher les choix disponibles
      const choicesContainer = document.querySelector(".choices-container");
      choicesContainer.innerHTML = "";

      // Vérifier si c'est un scénario de fin
      if (data.est_fin) {
        this.progression = 100; // Assurer que la progression est à 100%
        this.updateProgressionDisplay();
        this.showEndingScreen(true, "Félicitations ! Vous avez réussi à survivre et à vous échapper de l'île !");
        return;
      }

      // Ajouter les boutons de choix
      data.choix.forEach((choice) => {
        const button = document.createElement("button");
        button.className = "choice-button";
        button.textContent = choice.description;

        // Ajouter une indication si un objet est requis
        if (choice.requiert) {
          const requiredSpan = document.createElement("span");
          requiredSpan.className = "required-item";
          requiredSpan.textContent = ` (Nécessite: ${choice.requiert})`;
          button.appendChild(requiredSpan);

          // Désactiver le bouton si l'objet n'est pas dans l'inventaire
          if (!this.inventaire.includes(choice.requiert)) {
            button.disabled = true;
            button.classList.add("disabled");
          }
        }

        // Ajouter les effets sur les statistiques
        if (choice.effet_faim !== 0 || choice.effet_energie !== 0 || choice.effet_moral !== 0) {
          const effetsDiv = document.createElement("div");
          effetsDiv.className = "effets-stats";

          // Créer la liste des effets
          const effetsList = [];

          if (choice.effet_faim !== 0) {
            const faimSpan = document.createElement("span");
            faimSpan.className = choice.effet_faim > 0 ? "effet-positif" : "effet-negatif";
            faimSpan.innerHTML = `<i class="fas fa-utensils"></i> ${choice.effet_faim > 0 ? "+" : ""}${choice.effet_faim}`;
            effetsList.push(faimSpan);
          }

          if (choice.effet_energie !== 0) {
            const energieSpan = document.createElement("span");
            energieSpan.className = choice.effet_energie > 0 ? "effet-positif" : "effet-negatif";
            energieSpan.innerHTML = `<i class="fas fa-bolt"></i> ${choice.effet_energie > 0 ? "+" : ""}${choice.effet_energie}`;
            effetsList.push(energieSpan);
          }

          if (choice.effet_moral !== 0) {
            const moralSpan = document.createElement("span");
            moralSpan.className = choice.effet_moral > 0 ? "effet-positif" : "effet-negatif";
            moralSpan.innerHTML = `<i class="fas fa-smile"></i> ${choice.effet_moral > 0 ? "+" : ""}${choice.effet_moral}`;
            effetsList.push(moralSpan);
          }

          // Ajouter les effets à la div
          effetsList.forEach((effet, index) => {
            effetsDiv.appendChild(effet);
            if (index < effetsList.length - 1) {
              const separator = document.createTextNode("  ");
              effetsDiv.appendChild(separator);
            }
          });

          button.appendChild(document.createElement("br"));
          button.appendChild(effetsDiv);
        }

        // Ajouter un objet à obtenir, si disponible
        if (choice.ajoute_objet) {
          const objetDiv = document.createElement("div");
          objetDiv.className = "obtient-objet";
          objetDiv.innerHTML = `<i class="fas fa-plus-circle"></i> ${choice.ajoute_objet}`;
          button.appendChild(objetDiv);
        }

        button.onclick = () => this.makeChoice(choice.id);
        choicesContainer.appendChild(button);
      });
    } catch (error) {
      console.error("Erreur lors du chargement du scénario:", error);
    }
  }

  async makeChoice(choiceId) {
    try {
      const response = await fetch(`/api/choix/${choiceId}/`);
      const data = await response.json();

      // Appliquer d'abord les effets du choix (ils peuvent être positifs ou négatifs)
      this.stats.faim = Math.max(0, Math.min(100, this.stats.faim + data.effet_faim));
      this.stats.energie = Math.max(0, Math.min(100, this.stats.energie + data.effet_energie));
      this.stats.moral = Math.max(0, Math.min(100, this.stats.moral + data.effet_moral));

      // Appliquer un malus beaucoup plus léger pour représenter le temps qui passe
      // La faim diminue très légèrement (réduit de 1 à 0.3)
      this.stats.faim = Math.max(0, this.stats.faim - 0.3);

      // L'énergie ne diminue que pour certains choix et encore plus légèrement (réduit de 0.5 à 0.2)
      if (data.effet_energie <= 0) {
        this.stats.energie = Math.max(0, this.stats.energie - 0.2);
      }

      // Le moral ne diminue que si le joueur est déjà dans un état préoccupant
      // et avec une valeur plus faible (réduit de 0.5 à 0.2)
      if (this.stats.faim < 30 || this.stats.energie < 30) {
        this.stats.moral = Math.max(0, this.stats.moral - 0.2);
      }

      // Ajouter un objet à l'inventaire si nécessaire
      if (data.ajoute_objet && !this.inventaire.includes(data.ajoute_objet)) {
        this.inventaire.push(data.ajoute_objet);
        this.showNotification(`Vous avez obtenu: ${data.ajoute_objet}`, "item");
      }

      // Mettre à jour la progression (ajout d'un incrément plus significatif)
      if (data.prochain_scenario) {
        // On augmente la progression de 5% à chaque changement de scénario
        // pour créer une sensation de progression plus marquée
        this.progression = Math.min(100, this.progression + 5);
      }

      this.updateStats();

      // Afficher notification des changements de statistiques (uniquement ceux liés au choix)
      let statsMessage = "";
      if (data.effet_faim !== 0) {
        statsMessage += `Faim ${data.effet_faim > 0 ? "+" : ""}${data.effet_faim}  `;
      }
      if (data.effet_energie !== 0) {
        statsMessage += `Énergie ${data.effet_energie > 0 ? "+" : ""}${data.effet_energie}  `;
      }
      if (data.effet_moral !== 0) {
        statsMessage += `Moral ${data.effet_moral > 0 ? "+" : ""}${data.effet_moral}`;
      }

      if (statsMessage) {
        this.showNotification(statsMessage, "stats");
      }

      // Vérifier si le joueur a atteint la fin (progression à 100%)
      if (this.progression >= 100) {
        // Le joueur a atteint une fin victorieuse
        this.showEndingScreen(true, "Félicitations ! Après une longue aventure, vous avez réussi à survivre et à vous échapper de l'île !");
        return;
      }

      // Vérifier si le joueur a perdu (stats à 0)
      if (this.stats.energie <= 0) {
        // Si l'énergie tombe à zéro, c'est une défaite automatique
        this.showEndingScreen(false, "Vous n'avez plus d'énergie et vous vous êtes effondré d'épuisement...");
        return;
      } else if (this.stats.faim <= 0) {
        // Si la faim tombe à zéro
        this.showEndingScreen(false, "Vous êtes mort de faim sur cette île hostile...");
        return;
      } else if (this.stats.moral <= 0) {
        // Si le moral tombe à zéro
        this.showEndingScreen(false, "Votre moral s'est effondré et vous avez abandonné tout espoir de survie...");
        return;
      }

      // Chargement du prochain scénario
      if (data.prochain_scenario) {
        this.currentScenarioId = data.prochain_scenario;
        this.loadScenario(this.currentScenarioId, true);
      }
    } catch (error) {
      console.error("Erreur lors du choix:", error);
    }
  }

  showNotification(message, type = "default") {
    // Créer une notification temporaire
    const notification = document.createElement("div");
    notification.className = "game-notification";

    // Ajouter classe selon le type de notification
    if (type === "stats") {
      notification.classList.add("stats-notification");
    } else if (type === "item") {
      notification.classList.add("item-notification");
    } else if (type === "progression") {
      notification.classList.add("progression-notification");
    }

    notification.textContent = message;

    document.body.appendChild(notification);

    // Faire disparaître la notification après 3 secondes
    setTimeout(() => {
      notification.classList.add("fade-out");
      setTimeout(() => {
        notification.remove();
      }, 500);
    }, 3000);
  }

  showEndingScreen(isVictory, message) {
    // Créer l'écran de fin
    const endingScreen = document.createElement("div");
    endingScreen.className = "ending-screen";

    const endingTitle = document.createElement("h2");
    endingTitle.textContent = isVictory ? "VICTOIRE !" : "GAME OVER";
    endingTitle.className = isVictory ? "victory-title" : "defeat-title";

    const endingMessage = document.createElement("p");
    endingMessage.textContent = message;

    const restartButton = document.createElement("button");
    restartButton.textContent = "Recommencer";
    restartButton.onclick = () => {
      window.location.reload();
    };

    endingScreen.appendChild(endingTitle);
    endingScreen.appendChild(endingMessage);
    endingScreen.appendChild(restartButton);

    // Remplacer le contenu du jeu
    const gameContainer = document.querySelector(".game-container");
    gameContainer.innerHTML = "";
    gameContainer.appendChild(endingScreen);
  }
}

// Initialisation du jeu au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
  window.game = new Game();
});
