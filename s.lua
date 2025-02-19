function getPlayerList()
    local players = {}
    for _, player in ipairs(getElementsByType("player")) do
        table.insert(players, getPlayerName(player))
    end
    return players
end
function kickPlayerByName(playerName, reason)
    -- Try to get the player element using the player name
    local player = getPlayerFromName(playerName)

    if player then
        -- If the player exists, kick them with the reason
        kickPlayer(player, reason)
        return "Player " .. playerName .. " has been kicked."
    else
        -- If the player doesn't exist, return an error message
        return "Player not found or is not online."
    end
end


function banPlayerByName(playerName, reason)
    local player = getPlayerFromName(playerName)
    if not player then
        return "Player not found."
    end

    banPlayer(player, reason)  -- Ban the player with the given reason
    return "Player " .. playerName .. " has been banned for: " .. reason
end
function getPlayersMoney()
    local playersMoney = {}
    for _, player in ipairs(getElementsByType("player")) do
        local playerName = getPlayerName(player)
        local money = getPlayerMoney(player)
        playersMoney[playerName] = money
    end
    return playersMoney
end

function setPlayerMoneyByName(playerName, money)
    local player = getPlayerFromName(playerName)
    if not player then
        return "Player not found."
    end
    setPlayerMoney(player,money)
    return "Player " .. playerName .. " now has $" .. money
end

function setPlayerPos(playerName, x, y, z)
    local player = getPlayerFromName(playerName)
    if player then
        -- Set the player's position to the specified coordinates
        setElementPosition(player, x, y, z)
        return "Player " .. playerName .. " moved to (" .. x .. ", " .. y .. ", " .. z .. ")"
    else
        return "Player not found."
    end
end

function getPlayerPos(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        -- Get the player's position
        local x, y, z = getElementPosition(player)
        return "Player " .. playerName .. " is at (" .. x .. ", " .. y .. ", " .. z .. ")"
    else
        return "Player not found."
    end
end

function getPlayerSkins(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        -- Get the player's skin ID
        local skin = getElementModel(player)
        return "Player " .. playerName .. " has skin ID " .. skin
    else
        return "Player not found."
    end
end
function setSkinPlayer(playerName, skinID)
    local player = getPlayerFromName(playerName)
    if player then
        -- Set the player's skin to the specified skin ID
        setElementModel(player, skinID)
        return "Player " .. playerName .. " now has skin ID " .. skinID
    else
        return "Player not found."
    end
end
function givePlayerCar(playerName, carID)
    local player = getPlayerFromName(playerName)
    if player then
        -- Create a vehicle for the player
        local x, y, z = getElementPosition(player)
        local vehicle = createVehicle(carID, x, y, z)
        -- Set the vehicle's owner to the player
        setElementData(vehicle, "owner", playerName)
        -- Warp the player into the vehicle
        warpPedIntoVehicle(player, vehicle)
        return "Player " .. playerName .. " has received a vehicle with ID " .. carID
    else
        return "Player not found."
    end
end

function getPlayerVehicle(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        -- Get the player's vehicle
        local vehicle = getPedOccupiedVehicle(player)
        if vehicle then
            -- Get the vehicle's ID
            local vehicleID = getElementModel(vehicle)
            return "Player " .. playerName .. " is in a vehicle with ID " .. vehicleID
        else
            return "Player " .. playerName .. " is not in a vehicle"
        end
    else
        return "Player not found."
    end
end
    
function setPlayerWarpToPlayer(playerName, targetPlayerName)
    local player = getPlayerFromName(playerName)
    local targetPlayer = getPlayerFromName(targetPlayerName)
    if player and targetPlayer then
        -- Get the target player's position
        local x, y, z = getElementPosition(targetPlayer)
        -- Set the player's position to the target player's position
        setElementPosition(player, x, y, z)
        return "Player " .. playerName .. " has been warped to " .. targetPlayerName
    else
        return "Player not found."
    end
end
function getPlayerWeapons(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        -- Get the player's current weapon
        local weapon = getPedWeapon(player)
        return tostring(weapon)  -- Ensure the weapon is returned as a string
    else
        return "Player not found"
    end
end
function getPlayerHealth(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        -- Get the player's health
        local health = getElementHealth(player)
        return "Player " .. playerName .. " has " .. health .. " health"
    else
        return "Player not found."
    end
end

function setAdmin(playerName,aclname)
    local player = getPlayerFromName(playerName)
    if player then
        aclGroupAddObject(aclGetGroup(aclname), "user." .. getAccountName(getPlayerAccount(player)))
        return "Player " .. playerName .. " is now an admin"
    else
        return "Player not found."
    end
end

function RemoveAdmin(playerName,aclname)
    local player = getPlayerFromName(playerName)
    if player then
        aclGroupRemoveObject(aclGetGroup(aclname), "user." .. getAccountName(getPlayerAccount(player)))
        return "Player " .. playerName .. " is no longer an admin"
    else
        return "Player not found."
    end
end

function getPlayerIPs(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        local ip = getPlayerIP(player)
        if ip then
            return ip
        else
            return "Error: Unable to retrieve IP"
        end
    else
        return "Error: Player not found"
    end
end


function getPlayerSerials(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        return getPlayerSerial(player)
    else
        return nil
    end
end

function getPlayerAccountName(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        local account = getPlayerAccount(player)
        if account and not isGuestAccount(account) then
            return getAccountName(account)
        end
    end
    return nil
end



function getPlayerPower(playerName)
    local player = getPlayerFromName(playerName)
    if player then
        local account = getPlayerAccount(player)
        if account and not isGuestAccount(account) then
            local accountName = getAccountName(account)
            local group = aclGetGroup("Admin")
            if aclGroupIsObjectInGroup(group, "user." .. accountName) then
                return "Admin"
            end
            group = aclGetGroup("Moderator")
            if aclGroupIsObjectInGroup(group, "user." .. accountName) then
                return "Moderator"
            end
            group = aclGetGroup("Supporter")
            if aclGroupIsObjectInGroup(group, "user." .. accountName) then
                return "Supporter"
            end
            return "Player"
        end
    end
    return nil
end

local botURL = "http://127.0.0.1:5000/chat"

function sendToDiscordChannel(message, player)
    local playerName = getPlayerName(player)
    local data = { sender = playerName, message = message }
    local postData = toJSON(data)  -- تحويل الجدول إلى JSON

    fetchRemote(
        botURL,
        function(responseData, errorCode)
            if errorCode ~= 0 then
                outputDebugString("⚠️ Error sending message to bot: " .. tostring(errorCode))
            else
                outputDebugString("✅ Message sent successfully to bot!")
            end
        end,
        postData,
        true,  -- تمرير true لاستخدام POST
        { ["Content-Type"] = "application/json" }
    )
end

addEventHandler("onPlayerChat", root, function(message)
    sendToDiscordChannel(message, source)
end)

addEventHandler("onPlayerJoin", root, function()
    sendToDiscordChannel("joined the server", source)
end)

addEventHandler("onPlayerQuit", root, function(quitType)
    sendToDiscordChannel("left the server (" .. quitType .. ")", source)
end)

addEventHandler("onPlayerChangeNick", root, function(oldNick, newNick)
    sendToDiscordChannel("changed their nickname from " .. oldNick .. " to " .. newNick, source)
end)

addEventHandler("onPlayerLogin", root, function(_, account)
    local playerName = getPlayerName(source)
    local accountName = getAccountName(account)
    sendToDiscordChannel("logged in as " .. accountName, source)
end)

addEventHandler("onPlayerLogout", root, function()
    sendToDiscordChannel("logged out", source)
end)

addEventHandler("onPlayerCommand", root, function(command)
    sendToDiscordChannel("executed command: " .. command, source)
end)

addEventHandler("onPlayerScreenShot", root, function()
    sendToDiscordChannel("took a screenshot", source)
end)

addEventHandler("onPlayerBan", root, function()
    sendToDiscordChannel("has been banned", source)
end)

addEventHandler("onPlayerUnban", root, function()
    sendToDiscordChannel("has been unbanned", source)
end)

addEventHandler("onPlayerMute", root, function()
    sendToDiscordChannel("has been muted", source)
end)

addEventHandler("onPlayerUnmute", root, function()
    sendToDiscordChannel("has been unmuted", source)
end)


addEventHandler("onPlayerWasted", root, function()
    sendToDiscordChannel("died", source)
end)

addEventHandler("onPlayerDamage", root, function()
    sendToDiscordChannel("has been damaged", source)
end)
addEventHandler("onPlayerPickupHit", root, function()
    sendToDiscordChannel("has been hit by a pickup", source)
end)

addEventHandler("onPlayerPickupUse", root, function()
    sendToDiscordChannel("has used a pickup", source)
end)

addEventHandler("onPlayerPickupLeave", root, function()
    sendToDiscordChannel("has left a pickup", source)
end)

addEventHandler("onPlayerPickupRespawn", root, function()
    sendToDiscordChannel("has respawned a pickup", source)
end)

addEventHandler("onPlayerVehicleEnter", root, function()
    sendToDiscordChannel("entered a vehicle", source)
end)

addEventHandler("onPlayerVehicleExit", root, function()
    sendToDiscordChannel("exited a vehicle", source)
end)

addEventHandler("onPlayerMarkerHit", root, function()
    sendToDiscordChannel("hit a marker", source)
end)

addEventHandler("onPlayerMarkerLeave", root, function()
    sendToDiscordChannel("left a marker", source)
end)

function startResources(resourceName)
    local resource = getResourceFromName(resourceName)
    if resource then
        startResource(resource)
        return "Resource " .. resourceName .. " has been started."
    else
        return "Resource not found."
    end
end

function stopResources(resourceName)
    if type(resourceName) ~= "string" then
        return "Error: resourceName should be a string."
    end
    local resource = getResourceFromName(resourceName)
    if resource then
        stopResource(resource)
        return "Resource " .. resourceName .. " has been stopped."
    else
        return "Resource not found."
    end
end

function getPlayerInServer()
    local players = getElementsByType("player")
    local playerCount = #players
    outputDebugString("DEBUG: عدد اللاعبين في السيرفر: " .. playerCount)
    return playerCount
end

