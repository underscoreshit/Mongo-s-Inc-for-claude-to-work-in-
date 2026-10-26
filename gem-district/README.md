# Gem District (jeu Roblox)

Tycoon de bijouterie. Ambiance quartier des diamantaires, gros coups, prise de risque. Univers original (aucun nom ni élément du film).

## Choix par défaut (à changer si tu veux)
- **Style** : cartoon et coloré, adapté au public Roblox.
- **Joueurs** : multijoueur sur le même serveur, mais chacun a son inventaire et son argent. Échanges et boutiques entre joueurs plus tard.
- **Niveau** : je te guide pas à pas.

## Phase 1 : prototype (ce dossier)
Boucle jouable : **livraison → établi de taille → comptoir de vente**.

1. **Caisse « Livraison »** : `E` pour prendre un quartz brut (3 max en poche). Sa qualité est **cachée** : défaut (×0,3), standard, belle eau (×1,8) ou exceptionnelle (×5, 3 % de chance).
2. **Établi de taille** : `E` ouvre le mini-jeu. Un curseur fait des allers-retours, tu appuies sur **Espace** (ou le bouton COUPER sur mobile) :
   - zone bleue fine = **coup de génie** ×3
   - zone verte = **parfaite** ×1,5
   - zone jaune = **correcte** ×1
   - à côté = **ratée** ×0,2

   Après la coupe, la qualité cachée est révélée. C'est le pari.
3. **Comptoir de vente** : `E` vend toutes tes pierres taillées. L'argent s'affiche dans le classement (Argent).

La boutique est construite par le code au lancement : rien à poser à la main. Si tu crées toi-même un modèle `GemShop` dans Workspace (avec des parts `Crate`, `Workbench`, `Counter` contenant chacune un ProximityPrompt), le jeu utilise le tien.

## Lancer le jeu dans Roblox Studio (avec Rojo)
Rojo synchronise les fichiers de ce dossier vers Studio.

1. Installe **Roblox Studio**.
2. Installe Rojo :
   - le plus simple : l'extension **Rojo** dans VS Code (elle installe tout), ou
   - en ligne de commande : installe [Rokit](https://github.com/rojo-rbx/rokit), puis `rokit install` dans ce dossier.
3. Dans Studio : onglet **Plugins** → installe le plugin **Rojo** (proposé par l'extension VS Code, ou `rojo plugin install`).
4. Ouvre un nouveau jeu **Baseplate** dans Studio.
5. Dans ce dossier : `rojo serve` (ou « Rojo: Open menu » → Start dans VS Code).
6. Dans Studio : plugin Rojo → **Connect**. Les scripts apparaissent dans l'Explorer.
7. Appuie sur **Play**. La boutique est derrière le point d'apparition.

## Sans Rojo (copier-coller)
Dans l'Explorer de Studio :

| Fichier | À créer dans Studio |
|---|---|
| `src/shared/Config.luau` | ReplicatedStorage → Folder `Shared` → ModuleScript `Config` |
| `src/shared/CutMath.luau` | ReplicatedStorage → `Shared` → ModuleScript `CutMath` |
| `src/server/ShopBuilder.luau` | ServerScriptService → Folder `Server` → ModuleScript `ShopBuilder` |
| `src/server/GameServer.server.luau` | ServerScriptService → `Server` → Script `GameServer` |
| `src/client/Hud.client.luau` | StarterPlayer → StarterPlayerScripts → LocalScript `Hud` |

Colle le contenu de chaque fichier, puis Play.

## Structure
```
src/
  shared/   Config (tous les chiffres d'équilibrage), CutMath (position du curseur)
  server/   GameServer (économie, inventaire, résultat de la taille), ShopBuilder (la boutique)
  client/   Hud (inventaire, notifications, mini-jeu)
```
L'argent et les résultats de taille sont calculés **côté serveur** uniquement. Le client affiche et envoie seulement « j'ai coupé à tel moment ».

## À tester (checklist Phase 1)
- [ ] Prendre 3 pierres, la 4e est refusée
- [ ] Tailler sans pierre : message d'erreur
- [ ] Les 4 résultats de taille sortent (viser à côté exprès)
- [ ] Ne pas couper pendant 12 s : la pierre est rendue
- [ ] Vendre : l'argent monte du bon montant
- [ ] Sur mobile (émulateur Studio) : bouton COUPER utilisable

## Limites connues (à traiter en Phase 2)
- Pas de sauvegarde : l'argent repart à 0 à chaque partie (DataStore en Phase 2).
- Anti-triche de la taille : le serveur accepte un timing dans une fenêtre de 0,5 s pour compenser le réseau. Un tricheur pourrait choisir son moment dans cette fenêtre. À durcir si le jeu marche.
- Une seule pierre (quartz). Les autres s'ajoutent dans `Config.Stones`.

## Suite
- **Phase 2** : améthyste → pierre légendaire, bijoux (pierre + métal), XP et niveaux, sauvegarde.
- **Phase 3** : clients PNJ, commandes, améliorations de la boutique.
- **Phase 4** : pierres mystérieuses, enchères, marché noir, vols, sons et effets.
- **Phase 5** : tutoriel, équilibrage, icône, publication.
