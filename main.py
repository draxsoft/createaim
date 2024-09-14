-- Ensure you have Rayfield UI and its dependencies loaded in your environment.

-- Dependencies
local Rayfield = require(game:GetService("ReplicatedStorage"):WaitForChild("Rayfield"))

-- Create a Rayfield UI instance
local window = Rayfield:CreateWindow({
    Name = "Custom GUI",
    Size = Vector2.new(400, 300),
    Theme = Rayfield.Themes.Dark
})

-- Create tabs for different functionalities
local flyTab = window:CreateTab("Fly")
local ballTab = window:CreateTab("Ball")
local animationsTab = window:CreateTab("Animations")

-- Fly functionality
local function toggleFly()
    local player = game.Players.LocalPlayer
    local character = player.Character or player.CharacterAdded:Wait()
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    
    if humanoid then
        local bodyVelocity = Instance.new("BodyVelocity")
        bodyVelocity.Velocity = Vector3.new(0, 50, 0) -- Change this value for different flying speeds
        bodyVelocity.Parent = character.PrimaryPart
        game:GetService("RunService").Heartbeat:Connect(function()
            bodyVelocity.Velocity = Vector3.new(0, 50, 0)
        end)
    end
end

flyTab:AddButton({
    Name = "Toggle Fly",
    Callback = toggleFly
})

-- Ball functionality with physics
local function transformToBall()
    local player = game.Players.LocalPlayer
    local character = player.Character or player.CharacterAdded:Wait()
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    
    if humanoid then
        -- Ensure the character's PrimaryPart is set
        if not character.PrimaryPart then
            character:SetPrimaryPartCFrame(character:FindFirstChild("HumanoidRootPart").CFrame)
        end

        -- Create the ball part
        local ball = Instance.new("Part")
        ball.Size = Vector3.new(5, 5, 5)
        ball.Shape = Enum.PartType.Ball
        ball.Position = character.PrimaryPart.Position
        ball.Anchored = false
        ball.CanCollide = true
        ball.Parent = workspace

        -- Create a BodyGyro to maintain ball-like rotation
        local bodyGyro = Instance.new("BodyGyro")
        bodyGyro.P = 10000
        bodyGyro.D = 1000
        bodyGyro.MaxTorque = Vector3.new(4000, 4000, 4000)
        bodyGyro.CFrame = character.PrimaryPart.CFrame
        bodyGyro.Parent = ball

        -- Create a BodyVelocity to move the ball
        local bodyVelocity = Instance.new("BodyVelocity")
        bodyVelocity.Velocity = Vector3.new(0, 0, 0)
        bodyVelocity.MaxForce = Vector3.new(4000, 4000, 4000)
        bodyVelocity.Parent = ball

        -- Position ball where character is
        ball.CFrame = character.PrimaryPart.CFrame

        -- Optional: Remove character to keep only the ball
        character:Destroy()

        -- Update the ball position and rotation
        game:GetService("RunService").Stepped:Connect(function()
            ball.CFrame = character.PrimaryPart.CFrame
        end)
    end
end

ballTab:AddButton({
    Name = "Transform to Ball",
    Callback = transformToBall
})

-- Animation player functionality
local function playAnimation(animationId)
    local player = game.Players.LocalPlayer
    local character = player.Character or player.CharacterAdded:Wait()
    local humanoid = character:FindFirstChildOfClass("Humanoid")
    
    if humanoid then
        local animation = Instance.new("Animation")
        animation.AnimationId = "rbxassetid://" .. animationId
        
        local animTrack = humanoid:LoadAnimation(animation)
        animTrack:Play()
    end
end

animationsTab:AddInput({
    Name = "Animation ID",
    PlaceholderText = "Enter Animation ID",
    Callback = function(input)
        playAnimation(input)
    end
})

-- Display the UI
window:Show()
