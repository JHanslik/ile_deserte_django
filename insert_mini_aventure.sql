-- Mini-aventure améliorée : scénarios et choix pour L'Île Perdue

-- 1. Plage (départ)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (1, 'Vous vous réveillez sur une plage déserte, le soleil brûlant sur votre peau. Votre tête bourdonne et vos vêtements sont trempés. Les vagues viennent doucement lécher le sable à vos pieds. Autour de vous, vous ne voyez que du sable blanc, des palmiers et l''océan à perte de vue. Votre estomac crie famine et vous vous sentez faible. Que faites-vous ?', 1, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 2. Jungle
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (2, 'Vous vous enfoncez dans la jungle. L''air est moite, la végétation dense. Vous entendez des bruits d''animaux et apercevez des fruits dans les arbres. Vous trouvez aussi du bois sec au sol.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 3. Nourriture sur la plage
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (3, 'Vous cherchez de la nourriture sur la plage. Après quelques minutes, vous apercevez des traces dans le sable.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 4. Abri
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (4, 'Vous tentez de construire un abri avec ce que vous trouvez sur la plage. Cela vous protège du soleil et du vent.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 5. Fruits (bonus)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (5, 'Vous trouvez des fruits comestibles et reprenez des forces. Vous pouvez retourner à la plage.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 6. Grotte (danger)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (6, 'Vous découvrez une grotte sombre. L''entrée est étroite et l''intérieur semble dangereux. Vous trouvez une pierre à feu près de l''entrée.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 7. Crabe (bonus)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (7, 'Vous attrapez un crabe et le cuisinez. Cela vous redonne de l''énergie.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 8. Rien trouvé (malus)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (8, 'Vous ne trouvez rien à manger. La faim se fait sentir.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 9. Repos (bonus moral/énergie)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (9, 'Vous vous reposez dans votre abri. Vous vous sentez mieux et prêt à explorer.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 10. Colline (fin possible)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (10, 'Du sommet de la colline, vous voyez toute l''île. C''est l''endroit idéal pour allumer un feu de signal.', 0, 0, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 11. Grotte dangereuse (défaite)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (11, 'Vous vous perdez dans la grotte et ne retrouvez jamais la sortie... Votre aventure s''arrête ici.', 0, 1, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 12. Feu de signal (victoire)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (12, 'Grâce au bois sec et à la pierre à feu que vous avez collectés, vous parvenez à allumer un feu visible de loin. Un navire aperçoit la fumée et vient vous secourir. Vous êtes sauvé ! Votre ingéniosité et votre persévérance ont payé.', 0, 1, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- 13. Feu impossible (échec)
INSERT OR REPLACE INTO survie_scenario (id, texte, est_debut, est_fin, requiert_objet, created_at, updated_at)
VALUES (13, 'Vous essayez d''allumer un feu, mais sans bois sec ni pierre à feu, vos efforts sont vains. Vous perdez espoir et restez bloqué sur l''île...', 0, 1, NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 1 (Plage)
DELETE FROM survie_choix WHERE scenario_id=1;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (1, 'Explorer la jungle', -5, -10, 5, NULL, NULL, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (1, 'Chercher de la nourriture sur la plage', -5, -5, 0, NULL, NULL, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (1, 'Construire un abri de fortune', -10, -15, 10, 'Abri', NULL, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 2 (Jungle)
DELETE FROM survie_choix WHERE scenario_id=2;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (2, 'Cueillir des fruits', 20, 0, 5, 'Fruits', NULL, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'Ramasser du bois sec', 0, 0, 0, 'Bois sec', NULL, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'S''enfoncer plus loin dans la jungle', -10, -15, -5, NULL, NULL, 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (2, 'Retourner à la plage', 0, -5, 0, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 3 (Nourriture sur la plage)
DELETE FROM survie_choix WHERE scenario_id=3;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (3, 'Attraper un crabe', 15, 5, 5, 'Crabe', NULL, 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 'Rien trouvé', -10, -5, -5, NULL, NULL, 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (3, 'Retourner à la plage', 0, -5, 0, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 4 (Abri)
DELETE FROM survie_choix WHERE scenario_id=4;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (4, 'Se reposer dans l''abri', 0, 20, 10, NULL, 'Abri', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 'Explorer la colline', -5, -10, 5, NULL, NULL, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (4, 'Retourner à la plage', 0, -5, 0, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 5 (Fruits)
DELETE FROM survie_choix WHERE scenario_id=5;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (5, 'Retourner à la plage', 0, -5, 0, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 6 (Grotte)
DELETE FROM survie_choix WHERE scenario_id=6;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (6, 'Ramasser la pierre à feu', 0, 0, 0, 'Pierre à feu', NULL, 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 'Explorer la grotte', -20, -30, -20, NULL, NULL, 11, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (6, 'Revenir sur ses pas', 0, -5, 0, NULL, NULL, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 7 (Crabe)
DELETE FROM survie_choix WHERE scenario_id=7;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (7, 'Retourner à la plage', 0, -5, 0, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 8 (Rien trouvé)
DELETE FROM survie_choix WHERE scenario_id=8;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (8, 'Retourner à la plage', 0, -5, 0, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 9 (Repos)
DELETE FROM survie_choix WHERE scenario_id=9;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (9, 'Explorer la colline', -5, -10, 5, NULL, NULL, 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (9, 'Retourner à la plage', 0, -5, 0, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 10 (Colline)
DELETE FROM survie_choix WHERE scenario_id=10;
INSERT INTO survie_choix (scenario_id, texte, delta_faim, delta_energie, delta_moral, ajoute_objet, requiert_objet, scenario_suivant_id, created_at, updated_at)
VALUES
  (10, 'Allumer un feu de signal', 0, 0, 50, NULL, 'Bois sec,Pierre à feu', 12, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (10, 'Allumer un feu de signal (sans les bons objets)', 0, 0, -20, NULL, NULL, 13, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
  (10, 'Redescendre vers la plage', 0, -5, 0, NULL, NULL, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Choix pour le scénario 11 (Grotte dangereuse - défaite)
-- Pas de choix, fin du jeu

-- Choix pour le scénario 12 (Feu de signal - victoire)
-- Pas de choix, fin du jeu

-- Choix pour le scénario 13 (Feu impossible - échec)
-- Pas de choix, fin du jeu 