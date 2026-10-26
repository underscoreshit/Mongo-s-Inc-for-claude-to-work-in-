-- Calcul partagé client/serveur : position du curseur sur la barre de taille.
local CutMath = {}

-- Aller-retour 0 -> 1 -> 0 en `period` secondes.
function CutMath.barPosition(elapsed: number, period: number): number
	local t = (elapsed % period) / period
	if t < 0.5 then
		return t * 2
	end
	return 2 - t * 2
end

return CutMath
