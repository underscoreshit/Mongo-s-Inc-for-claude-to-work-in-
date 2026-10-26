-- Tous les chiffres d'équilibrage du jeu. On ajoute les pierres ici en Phase 2.
local Config = {}

Config.Stones = {
	Quartz = {
		displayName = "Quartz",
		baseValue = 20,
		color = Color3.fromRGB(235, 225, 255),
	},
}

Config.StarterStone = "Quartz"
Config.MaxRawStones = 3

-- Qualité cachée : tirée à la réception, révélée seulement après la taille.
-- C'est le pari : une pierre peut cacher un défaut ou une valeur énorme.
Config.HiddenQualities = {
	{ id = "Flawed", label = "Défaut caché", multiplier = 0.3, weight = 20 },
	{ id = "Standard", label = "Standard", multiplier = 1, weight = 60 },
	{ id = "Fine", label = "Belle eau", multiplier = 1.8, weight = 17 },
	{ id = "Exceptional", label = "Exceptionnelle !", multiplier = 5, weight = 3 },
}

-- Résultats de taille, du plus précis au moins précis.
-- maxDistance : écart max entre le curseur et le centre de la zone (barre de 0 à 1).
Config.CutResults = {
	{ id = "Genius", label = "Coup de génie !", maxDistance = 0.015, multiplier = 3 },
	{ id = "Perfect", label = "Taille parfaite", maxDistance = 0.05, multiplier = 1.5 },
	{ id = "Good", label = "Taille correcte", maxDistance = 0.12, multiplier = 1 },
	{ id = "Failed", label = "Taille ratée", maxDistance = math.huge, multiplier = 0.2 },
}

Config.Cutting = {
	barPeriod = 1.4, -- secondes pour un aller-retour du curseur
	maxLatency = 0.5, -- retard réseau toléré entre client et serveur
	timeout = 12, -- si le joueur ne coupe pas, la pierre lui est rendue
}

return Config
