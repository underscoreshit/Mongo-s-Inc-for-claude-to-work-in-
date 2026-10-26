-- Construit la boutique du prototype en code, pour pouvoir jouer sans rien poser à la main.
-- Si un modèle "GemShop" existe déjà dans Workspace (fait dans Studio), on le garde.
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Config = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("Config"))

local ShopBuilder = {}

local function makePart(parent: Instance, props: { [string]: any }): Part
	local part = Instance.new("Part")
	part.Anchored = true
	part.TopSurface = Enum.SurfaceType.Smooth
	part.BottomSurface = Enum.SurfaceType.Smooth
	for key, value in props do
		(part :: any)[key] = value
	end
	part.Parent = parent
	return part
end

local function addLabel(part: BasePart, text: string, color: Color3)
	local gui = Instance.new("BillboardGui")
	gui.Size = UDim2.fromOffset(220, 50)
	gui.StudsOffset = Vector3.new(0, part.Size.Y / 2 + 2.5, 0)
	gui.AlwaysOnTop = true
	gui.MaxDistance = 60

	local label = Instance.new("TextLabel")
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.FredokaOne
	label.TextScaled = true
	label.TextColor3 = color
	label.TextStrokeTransparency = 0.2
	label.Text = text
	label.Parent = gui

	gui.Parent = part
end

local function addPrompt(part: BasePart, action: string, object: string): ProximityPrompt
	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = action
	prompt.ObjectText = object
	prompt.HoldDuration = 0
	prompt.MaxActivationDistance = 10
	prompt.RequiresLineOfSight = false
	prompt.Parent = part
	return prompt
end

export type Shop = {
	cratePrompt: ProximityPrompt,
	benchPrompt: ProximityPrompt,
	counterPrompt: ProximityPrompt,
}

function ShopBuilder.build(): Shop
	local existing = workspace:FindFirstChild("GemShop")
	if existing then
		return {
			cratePrompt = existing:FindFirstChild("Crate"):FindFirstChildOfClass("ProximityPrompt"),
			benchPrompt = existing:FindFirstChild("Workbench"):FindFirstChildOfClass("ProximityPrompt"),
			counterPrompt = existing:FindFirstChild("Counter"):FindFirstChildOfClass("ProximityPrompt"),
		}
	end

	local shop = Instance.new("Model")
	shop.Name = "GemShop"

	local origin = Vector3.new(0, 0, -30)

	makePart(shop, {
		Name = "Floor",
		Size = Vector3.new(44, 1, 32),
		Position = origin + Vector3.new(0, 0.5, 0),
		Color = Color3.fromRGB(70, 45, 90),
		Material = Enum.Material.SmoothPlastic,
	})

	makePart(shop, {
		Name = "BackWall",
		Size = Vector3.new(44, 14, 1),
		Position = origin + Vector3.new(0, 7.5, -16),
		Color = Color3.fromRGB(255, 205, 90),
		Material = Enum.Material.SmoothPlastic,
	})

	local sign = makePart(shop, {
		Name = "Sign",
		Size = Vector3.new(18, 3, 0.5),
		Position = origin + Vector3.new(0, 12, -15.3),
		Color = Color3.fromRGB(40, 20, 60),
	})
	local signGui = Instance.new("SurfaceGui")
	signGui.Face = Enum.NormalId.Front
	local signText = Instance.new("TextLabel")
	signText.Size = UDim2.fromScale(1, 1)
	signText.BackgroundTransparency = 1
	signText.Font = Enum.Font.FredokaOne
	signText.TextScaled = true
	signText.TextColor3 = Color3.fromRGB(120, 230, 255)
	signText.Text = "GEM DISTRICT"
	signText.Parent = signGui
	signGui.Parent = sign

	local crate = makePart(shop, {
		Name = "Crate",
		Size = Vector3.new(5, 4, 5),
		Position = origin + Vector3.new(-14, 3, -9),
		Color = Color3.fromRGB(150, 100, 55),
		Material = Enum.Material.WoodPlanks,
	})
	addLabel(crate, "Livraison", Color3.fromRGB(255, 230, 160))

	local bench = makePart(shop, {
		Name = "Workbench",
		Size = Vector3.new(8, 3.5, 4),
		Position = origin + Vector3.new(0, 2.75, -10),
		Color = Color3.fromRGB(110, 115, 130),
		Material = Enum.Material.DiamondPlate,
	})
	addLabel(bench, "Établi de taille", Color3.fromRGB(200, 240, 255))

	-- Une pierre décorative sur l'établi
	makePart(shop, {
		Name = "BenchGem",
		Shape = Enum.PartType.Ball,
		Size = Vector3.new(1.2, 1.2, 1.2),
		Position = bench.Position + Vector3.new(0, 2.4, 0),
		Color = Config.Stones[Config.StarterStone].color,
		Material = Enum.Material.Neon,
	})

	local counter = makePart(shop, {
		Name = "Counter",
		Size = Vector3.new(8, 3.5, 3),
		Position = origin + Vector3.new(14, 2.75, -9),
		Color = Color3.fromRGB(60, 190, 140),
		Material = Enum.Material.SmoothPlastic,
	})
	addLabel(counter, "Comptoir de vente", Color3.fromRGB(180, 255, 200))

	local shopData: Shop = {
		cratePrompt = addPrompt(crate, "Prendre", "Pierre brute"),
		benchPrompt = addPrompt(bench, "Tailler", "Établi"),
		counterPrompt = addPrompt(counter, "Vendre", "Comptoir"),
	}

	shop.Parent = workspace
	return shopData
end

return ShopBuilder
