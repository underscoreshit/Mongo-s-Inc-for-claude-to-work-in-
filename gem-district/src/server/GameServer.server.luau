-- Boucle de la Phase 1 : recevoir une pierre brute -> la tailler -> la vendre.
-- Toute l'économie est calculée ici, jamais côté client.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Shared")
local Config = require(Shared:WaitForChild("Config"))
local CutMath = require(Shared:WaitForChild("CutMath"))
local ShopBuilder = require(script.Parent:WaitForChild("ShopBuilder"))

-- RemoteEvents
local remotes = Instance.new("Folder")
remotes.Name = "Remotes"

local function makeRemote(name: string): RemoteEvent
	local remote = Instance.new("RemoteEvent")
	remote.Name = name
	remote.Parent = remotes
	return remote
end

local InventoryChanged = makeRemote("InventoryChanged") -- serveur -> client
local Notify = makeRemote("Notify") -- serveur -> client
local StartCut = makeRemote("StartCut") -- serveur -> client
local SubmitCut = makeRemote("SubmitCut") -- client -> serveur
local CutResult = makeRemote("CutResult") -- serveur -> client
remotes.Parent = ReplicatedStorage

type RawStone = { stone: string, quality: any }
type CutStone = { stone: string, quality: any, cut: any, value: number }
type Inventory = { raw: { RawStone }, cut: { CutStone } }
type ActiveCut = { startTime: number, zoneCenter: number, rawStone: RawStone }

local inventories: { [Player]: Inventory } = {}
local activeCuts: { [Player]: ActiveCut } = {}

local random = Random.new()

local function rollQuality()
	local total = 0
	for _, quality in Config.HiddenQualities do
		total += quality.weight
	end
	local roll = random:NextNumber(0, total)
	for _, quality in Config.HiddenQualities do
		roll -= quality.weight
		if roll <= 0 then
			return quality
		end
	end
	return Config.HiddenQualities[#Config.HiddenQualities]
end

local function cutResultFor(distance: number)
	for _, result in Config.CutResults do
		if distance <= result.maxDistance then
			return result
		end
	end
	return Config.CutResults[#Config.CutResults]
end

local function sendInventory(player: Player)
	local inventory = inventories[player]
	if not inventory then
		return
	end
	local cutList = {}
	for _, stone in inventory.cut do
		table.insert(cutList, {
			name = Config.Stones[stone.stone].displayName,
			quality = stone.quality.label,
			cut = stone.cut.label,
			value = stone.value,
		})
	end
	InventoryChanged:FireClient(player, {
		rawCount = #inventory.raw,
		maxRaw = Config.MaxRawStones,
		cut = cutList,
	})
end

local function getMoney(player: Player): IntValue?
	local leaderstats = player:FindFirstChild("leaderstats")
	return leaderstats and leaderstats:FindFirstChild("Argent") :: IntValue?
end

local function onPlayerAdded(player: Player)
	local leaderstats = Instance.new("Folder")
	leaderstats.Name = "leaderstats"
	local money = Instance.new("IntValue")
	money.Name = "Argent"
	money.Value = 0
	money.Parent = leaderstats
	leaderstats.Parent = player

	inventories[player] = { raw = {}, cut = {} }
	sendInventory(player)
end

Players.PlayerAdded:Connect(onPlayerAdded)
for _, player in Players:GetPlayers() do
	onPlayerAdded(player)
end

Players.PlayerRemoving:Connect(function(player)
	inventories[player] = nil
	activeCuts[player] = nil
end)

local shop = ShopBuilder.build()

-- 1. Recevoir une pierre brute
shop.cratePrompt.Triggered:Connect(function(player)
	local inventory = inventories[player]
	if not inventory then
		return
	end
	if #inventory.raw >= Config.MaxRawStones then
		Notify:FireClient(player, "Tes mains sont pleines : va tailler tes pierres.")
		return
	end
	local stone = Config.StarterStone
	table.insert(inventory.raw, { stone = stone, quality = rollQuality() })
	Notify:FireClient(player, Config.Stones[stone].displayName .. " brut reçu. Qualité inconnue...")
	sendInventory(player)
end)

-- 2. Tailler : le serveur lance le mini-jeu et garde la position de la zone
shop.benchPrompt.Triggered:Connect(function(player)
	local inventory = inventories[player]
	if not inventory or activeCuts[player] then
		return
	end
	if #inventory.raw == 0 then
		Notify:FireClient(player, "Aucune pierre brute. Passe à la livraison.")
		return
	end

	local rawStone = table.remove(inventory.raw, 1) :: RawStone
	local cut: ActiveCut = {
		startTime = os.clock(),
		zoneCenter = random:NextNumber(0.2, 0.8),
		rawStone = rawStone,
	}
	activeCuts[player] = cut
	sendInventory(player)

	local zones = {}
	for _, result in Config.CutResults do
		if result.maxDistance ~= math.huge then
			table.insert(zones, { id = result.id, halfWidth = result.maxDistance })
		end
	end
	StartCut:FireClient(player, {
		stoneName = Config.Stones[rawStone.stone].displayName,
		zoneCenter = cut.zoneCenter,
		zones = zones,
		period = Config.Cutting.barPeriod,
	})

	-- Si le joueur ne coupe pas, on lui rend sa pierre
	task.delay(Config.Cutting.timeout, function()
		if activeCuts[player] == cut then
			activeCuts[player] = nil
			local inv = inventories[player]
			if inv then
				table.insert(inv.raw, 1, rawStone)
				sendInventory(player)
			end
			CutResult:FireClient(player, nil)
			Notify:FireClient(player, "Taille annulée, la pierre est remise dans ta poche.")
		end
	end)
end)

SubmitCut.OnServerEvent:Connect(function(player, clientElapsed)
	local cut = activeCuts[player]
	local inventory = inventories[player]
	if not cut or not inventory then
		return
	end
	if typeof(clientElapsed) ~= "number" or clientElapsed ~= clientElapsed then
		return
	end
	activeCuts[player] = nil

	-- Le client mesure son propre temps (il démarre plus tard à cause du réseau).
	-- On n'accepte qu'une valeur cohérente avec l'horloge du serveur.
	local serverElapsed = os.clock() - cut.startTime
	local elapsed = math.clamp(clientElapsed, math.max(0, serverElapsed - Config.Cutting.maxLatency), serverElapsed)

	local position = CutMath.barPosition(elapsed, Config.Cutting.barPeriod)
	local result = cutResultFor(math.abs(position - cut.zoneCenter))
	local stoneConfig = Config.Stones[cut.rawStone.stone]
	local value = math.max(1, math.floor(stoneConfig.baseValue * cut.rawStone.quality.multiplier * result.multiplier + 0.5))

	table.insert(inventory.cut, {
		stone = cut.rawStone.stone,
		quality = cut.rawStone.quality,
		cut = result,
		value = value,
	})

	CutResult:FireClient(player, {
		position = position,
		cutId = result.id,
		cutLabel = result.label,
		qualityId = cut.rawStone.quality.id,
		qualityLabel = cut.rawStone.quality.label,
		value = value,
	})
	sendInventory(player)
end)

-- 3. Vendre toutes les pierres taillées
shop.counterPrompt.Triggered:Connect(function(player)
	local inventory = inventories[player]
	local money = getMoney(player)
	if not inventory or not money then
		return
	end
	if #inventory.cut == 0 then
		Notify:FireClient(player, "Rien à vendre. Taille d'abord une pierre.")
		return
	end
	local total = 0
	for _, stone in inventory.cut do
		total += stone.value
	end
	local count = #inventory.cut
	inventory.cut = {}
	money.Value += total
	Notify:FireClient(player, string.format("%d pierre(s) vendue(s) pour %d $", count, total))
	sendInventory(player)
end)
