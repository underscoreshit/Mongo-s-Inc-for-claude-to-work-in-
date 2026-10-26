-- Interface du joueur : inventaire, notifications et mini-jeu de taille.
-- Le client affiche seulement ; le résultat est calculé par le serveur.
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local ContextActionService = game:GetService("ContextActionService")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local Shared = ReplicatedStorage:WaitForChild("Shared")
local CutMath = require(Shared:WaitForChild("CutMath"))
local Remotes = ReplicatedStorage:WaitForChild("Remotes")

local FONT = Enum.Font.FredokaOne
local ZONE_COLORS = {
	Good = Color3.fromRGB(255, 200, 70),
	Perfect = Color3.fromRGB(90, 220, 120),
	Genius = Color3.fromRGB(120, 230, 255),
}
local RESULT_COLORS = {
	Genius = Color3.fromRGB(120, 230, 255),
	Perfect = Color3.fromRGB(90, 220, 120),
	Good = Color3.fromRGB(255, 220, 120),
	Failed = Color3.fromRGB(255, 100, 100),
}

local function make(className: string, props: { [string]: any }, children: { Instance }?): any
	local instance = Instance.new(className)
	for key, value in props do
		if key ~= "Parent" then
			(instance :: any)[key] = value
		end
	end
	for _, child in children or {} do
		child.Parent = instance
	end
	if props.Parent then
		instance.Parent = props.Parent
	end
	return instance
end

local function corner(radius: number)
	return make("UICorner", { CornerRadius = UDim.new(0, radius) })
end

local gui = make("ScreenGui", {
	Name = "GemHud",
	ResetOnSpawn = false,
	IgnoreGuiInset = false,
	Parent = player:WaitForChild("PlayerGui"),
})

-- Inventaire (haut gauche)
local inventoryLabel = make("TextLabel", {
	Size = UDim2.fromOffset(260, 0),
	AutomaticSize = Enum.AutomaticSize.Y,
	Position = UDim2.fromOffset(12, 12),
	BackgroundColor3 = Color3.fromRGB(30, 20, 45),
	BackgroundTransparency = 0.15,
	TextColor3 = Color3.new(1, 1, 1),
	Font = FONT,
	TextSize = 18,
	TextXAlignment = Enum.TextXAlignment.Left,
	TextYAlignment = Enum.TextYAlignment.Top,
	TextWrapped = true,
	RichText = true,
	Text = "Pierres brutes : 0\nPierres taillées : 0",
	Parent = gui,
}, { corner(10), make("UIPadding", {
	PaddingTop = UDim.new(0, 10),
	PaddingBottom = UDim.new(0, 10),
	PaddingLeft = UDim.new(0, 12),
	PaddingRight = UDim.new(0, 12),
}) })

Remotes:WaitForChild("InventoryChanged").OnClientEvent:Connect(function(data)
	local lines = {
		string.format("<b>Pierres brutes</b> : %d / %d", data.rawCount, data.maxRaw),
		string.format("<b>Pierres taillées</b> : %d", #data.cut),
	}
	local total = 0
	for _, stone in data.cut do
		total += stone.value
		table.insert(lines, string.format("• %s, %s : %d $", stone.name, stone.quality, stone.value))
	end
	if #data.cut > 0 then
		table.insert(lines, string.format("<b>À vendre : %d $</b>", total))
	end
	inventoryLabel.Text = table.concat(lines, "\n")
end)

-- Notifications (bas centre)
local toast = make("TextLabel", {
	AnchorPoint = Vector2.new(0.5, 1),
	Position = UDim2.new(0.5, 0, 1, -110),
	Size = UDim2.fromOffset(0, 44),
	AutomaticSize = Enum.AutomaticSize.X,
	BackgroundColor3 = Color3.fromRGB(30, 20, 45),
	TextColor3 = Color3.new(1, 1, 1),
	Font = FONT,
	TextSize = 20,
	Visible = false,
	Parent = gui,
}, { corner(10), make("UIPadding", { PaddingLeft = UDim.new(0, 16), PaddingRight = UDim.new(0, 16) }) })

local toastToken = 0
local function showToast(message: string)
	toastToken += 1
	local token = toastToken
	toast.Text = message
	toast.Visible = true
	task.delay(3, function()
		if toastToken == token then
			toast.Visible = false
		end
	end)
end
Remotes:WaitForChild("Notify").OnClientEvent:Connect(showToast)

-- Mini-jeu de taille (centre)
local panel = make("Frame", {
	AnchorPoint = Vector2.new(0.5, 0.5),
	Position = UDim2.fromScale(0.5, 0.5),
	Size = UDim2.new(0.9, 0, 0, 230),
	BackgroundColor3 = Color3.fromRGB(30, 20, 45),
	Visible = false,
	Parent = gui,
}, { corner(16), make("UISizeConstraint", { MaxSize = Vector2.new(560, 230) }) })

local title = make("TextLabel", {
	Position = UDim2.fromOffset(0, 12),
	Size = UDim2.new(1, 0, 0, 30),
	BackgroundTransparency = 1,
	TextColor3 = Color3.new(1, 1, 1),
	Font = FONT,
	TextSize = 24,
	Text = "",
	Parent = panel,
})

local bar = make("Frame", {
	AnchorPoint = Vector2.new(0.5, 0),
	Position = UDim2.new(0.5, 0, 0, 60),
	Size = UDim2.new(1, -40, 0, 36),
	BackgroundColor3 = Color3.fromRGB(70, 55, 90),
	ClipsDescendants = true,
	Parent = panel,
}, { corner(8) })

local cursor = make("Frame", {
	AnchorPoint = Vector2.new(0.5, 0.5),
	Position = UDim2.fromScale(0, 0.5),
	Size = UDim2.new(0, 4, 1, 0),
	BackgroundColor3 = Color3.new(1, 1, 1),
	ZIndex = 5,
	Parent = bar,
})

local resultLabel = make("TextLabel", {
	Position = UDim2.fromOffset(0, 104),
	Size = UDim2.new(1, 0, 0, 50),
	BackgroundTransparency = 1,
	TextColor3 = Color3.new(1, 1, 1),
	Font = FONT,
	TextSize = 22,
	TextWrapped = true,
	Text = "",
	Parent = panel,
})

local cutButton = make("TextButton", {
	AnchorPoint = Vector2.new(0.5, 1),
	Position = UDim2.new(0.5, 0, 1, -14),
	Size = UDim2.fromOffset(220, 52),
	BackgroundColor3 = Color3.fromRGB(120, 230, 255),
	TextColor3 = Color3.fromRGB(30, 20, 45),
	Font = FONT,
	TextSize = 24,
	Text = "COUPER (Espace)",
	Parent = panel,
}, { corner(12) })

local zoneFrames: { Frame } = {}
local cutting = false
local cutStart = 0
local period = 1

local renderConnection: RBXScriptConnection?

local function stopRender()
	if renderConnection then
		renderConnection:Disconnect()
		renderConnection = nil
	end
	ContextActionService:UnbindAction("GemCut")
end

local function submit()
	if not cutting then
		return
	end
	cutting = false
	stopRender()
	cutButton.Visible = false
	Remotes.SubmitCut:FireServer(os.clock() - cutStart)
end

Remotes:WaitForChild("StartCut").OnClientEvent:Connect(function(data)
	for _, frame in zoneFrames do
		frame:Destroy()
	end
	table.clear(zoneFrames)

	-- Zones de la plus fine à la plus large : la plus fine passe au-dessus
	for i, zone in data.zones do
		local width = zone.halfWidth * 2
		table.insert(zoneFrames, make("Frame", {
			AnchorPoint = Vector2.new(0.5, 0),
			Position = UDim2.fromScale(data.zoneCenter, 0),
			Size = UDim2.fromScale(width, 1),
			BackgroundColor3 = ZONE_COLORS[zone.id] or Color3.new(1, 1, 1),
			BorderSizePixel = 0,
			ZIndex = #data.zones - i + 2,
			Parent = bar,
		}))
	end

	title.Text = "Taille : " .. data.stoneName
	resultLabel.Text = "Arrête le curseur dans la zone bleue."
	resultLabel.TextColor3 = Color3.new(1, 1, 1)
	cutButton.Visible = true
	panel.Visible = true

	period = data.period
	cutStart = os.clock()
	cutting = true

	stopRender()
	renderConnection = RunService.RenderStepped:Connect(function()
		cursor.Position = UDim2.fromScale(CutMath.barPosition(os.clock() - cutStart, period), 0.5)
	end)
	ContextActionService:BindActionAtPriority("GemCut", function(_, state)
		if state == Enum.UserInputState.Begin then
			submit()
		end
		return Enum.ContextActionResult.Sink
	end, false, Enum.ContextActionPriority.High.Value, Enum.KeyCode.Space, Enum.KeyCode.ButtonA)
end)

cutButton.Activated:Connect(submit)

Remotes:WaitForChild("CutResult").OnClientEvent:Connect(function(data)
	cutting = false
	stopRender()
	if not data then
		panel.Visible = false
		return
	end

	-- Le curseur se place là où le serveur a compté la coupe
	cursor.Position = UDim2.fromScale(data.position, 0.5)
	resultLabel.TextColor3 = RESULT_COLORS[data.cutId] or Color3.new(1, 1, 1)
	resultLabel.Text = string.format("%s\nQualité révélée : %s  →  %d $", data.cutLabel, data.qualityLabel, data.value)

	if data.cutId == "Genius" or data.qualityId == "Exceptional" then
		local pop = TweenService:Create(resultLabel, TweenInfo.new(0.15, Enum.EasingStyle.Back, Enum.EasingDirection.Out, 0, true), { TextSize = 30 })
		pop:Play()
	end

	task.delay(2.5, function()
		if not cutting then
			panel.Visible = false
		end
	end)
end)
