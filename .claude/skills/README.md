# Skills : quoi, quand, pourquoi

Collection installée le 16 octobre 2026 à partir des repos de la vidéo d'Enzo (tous MIT, licence copiée dans chaque dossier). Règle : **un skill par étape, pas tous à la fois.** Trop de skills contradictoires donnent une page molle. L'ordre ci-dessous est celui d'une démo Kade (2 h) ou d'un site client (48 h).

## Le parcours d'un site, skill par skill
| Étape | Skill | Ce qu'on lui demande | Pas plus de |
|---|---|---|---|
| 0. Lire le brief | `web-design-engineer` (garden-skills) | Le « Design Read » : 5 curseurs (variance, motion, densité, dépendance aux photos, fidélité à la marque) et les 4 questions (rôle, distance de lecture, température, capacité). On le remplit dans le README de la démo, on ne code pas avant. | 10 lignes |
| 1. Structure et texte | `landing-page-design` (elaya) | Une offre, un public, une action. Hero (titre = résultat + public, sous-titre, un CTA, une preuve), bénéfices, comment ça marche en 3 étapes, preuve, FAQ, CTA final. Les formules de titre. **On ignore sa partie B** (Geist, Tailwind, gradients de texte) : Kade a ses polices et ses règles dans `CLAUDE.md`. | 1 CTA au-dessus du pli |
| 2. Direction visuelle | `mengto-build-awwwards-quality-sites` + `taste-skill` | Écrire la direction avant de coder : thèse visuelle, image focale du hero, hiérarchie typo, couleurs, séquence des sections, récit du mouvement. Une police display qui porte la page. Pas de SVG dessiné pour remplacer une photo : placeholder honnête (règle Kade : rayé + nom du fichier). | 1 idée par page |
| 3. Typographie | `better-typography` (Krehel) | Échelle avec noms, line-height sans unité (display 1.1, titres 1.2, texte 1.5), tracking en em, mesure 60-75 caractères, `text-wrap: balance` sur les titres, 16 px dans les champs sur mobile, `tabular-nums` sur les chiffres. | 2 polices |
| 4. Mouvement | `emil-animate` → `gsap-scrolltrigger` (skill claude.ai), `mengto-staggered-word-reveal`, `mengto-masked-reveal` | D'abord la question d'Emil : faut-il animer ? Une seule « signature » par page (le hero), un seul trigger par section, transform et opacity uniquement, sortie par le même chemin, `prefers-reduced-motion` = état final tout de suite. GSAP depuis cdnjs, la page doit être complète sans JS. | 1 moment signature |
| 5. Relecture | `better-interface` (orchestre `better-accessibility`, `better-layout`, `better-writing`, `better-colors`, `better-ui`) puis `critique-visual-hierarchy`, `critique-composition` | Revue avec preuves (fichier:ligne), sévérité par impact, fix le moins cher d'abord. Les « escalation triggers » (focus invisible, contraste, 320 px cassé, motion sans reduced-motion) sont bloquants. | 15 findings |
| 6. Avant d'envoyer | `emil-review-animations`, `emil-animation-performance`, `playwright-cli` | Motion relue, perf (pas de blur lourd, pas d'animation hors écran), captures 390 px et 1440 px, thème sombre, pas de scroll horizontal. Checklist Kade : `delivery/quality-checklist.md`. | |

## Ce qu'on garde de chaque auteur
- **Emil Kowalski** : la porte d'entrée « animer ou pas », transform/opacity seulement, ease-out en entrée, < 300 ms pour l'UI, reduced-motion = plus doux, pas absent.
- **Elaya (landing-page-design)** : la structure en 12 blocs, les formules de titre, « proof next to the claim », la section tagline en gros caractères qui s'allume mot par mot au scroll, pas de Lorem, pas de chiffres ronds inventés.
- **Meng To** : direction écrite avant le code, hero = moment le plus fort, une seule bibliothèque de scroll (ou aucune), GSAP pour l'orchestration, placeholders honnêtes, jamais « award-winning » dans le texte.
- **garden-skills (web-design-engineer)** : les 5 curseurs, la liste anti-cliché (dégradés violet-rose, cartes à bord coloré, emoji-icônes, Inter partout, stats inventées), placeholder plutôt que faux dessin.
- **Jakub Krehel (better-*)** : la revue par preuves, la sévérité par impact utilisateur, le fix le moins cher, les triggers bloquants.
- **Owl-Listener (critique-*)** : vocabulaire de critique visuelle pour le dernier regard avant d'envoyer à Enzo.
- **tastemaker (codeswithroh)** : non installé. Il demande un profil de goût persistant et des scripts ; le `taste-skill` déjà présent couvre le besoin. À revoir si on veut un profil « Kade » formalisé.

## Ce qu'on n'applique pas (conflit avec les règles Kade)
- Polices Geist/Manrope via Google Fonts (elaya) : Kade = polices locales, Archivo + Big Shoulders ou Bricolage.
- Tailwind obligatoire (elaya) : les sites Kade sont du HTML/CSS statique.
- Dégradé sur le titre du hero (elaya B5) : seulement si la marque du client s'y prête.
- Lenis / smooth scroll (Meng To) : pas sur un site d'artisan, la vitesse perçue compte plus.
- Checkpoints « attendre la confirmation » (garden) : la session construit la démo entière, Enzo valide sur son gsm.

## Retirés le 20 octobre 2026 (doublons ou inutilisables ici)
| Skill | Pourquoi | Remplacé par |
|---|---|---|
| `image-to-code` | Écrit pour Codex, exige de générer des images de maquette : impossible dans nos sessions. | `taste-skill`, `web-design-engineer` |
| `mengto-landing-page` | Même structure que `landing-page-design`, en moins complet. | `landing-page-design` |
| `mengto-gsap` | Doublon du skill claude.ai `gsap-scrolltrigger`. | `gsap-scrolltrigger` |
| `mengto-animation-on-scroll` | Basé sur Tailwind (pas utilisé chez Kade), même effet que le reveal mot par mot. | `mengto-staggered-word-reveal` |
| `critique-brand-consistency` | Exige des fichiers `mood.md`, `voice.md`, `tokens.md` qu'on n'a pas. | `critique-visual-hierarchy` |
| `critique-color` | Doublon de `better-colors` (contraste, palette). | `better-colors` |
| `critique-typography` | Doublon de `better-typography`. | `better-typography` |
| `web-design-guidelines` | Va chercher ses règles sur le web à chaque fois ; `better-interface` couvre la même revue. | `better-interface` |

Pour en remettre un : il est dans l'historique git (commit du tri) ou dans son repo source ci-dessous.

## Mise à jour
Les sources sont dans les repos GitHub `emilkowalski/skills`, `elayadesign/ai-design-skills`, `MengTo/Skills`, `ConardLi/garden-skills`, `jakubkrehel/skills`, `Owl-Listener/designer-skills`. Pour remettre à jour : recloner, recopier le dossier du skill, garder ce README.
