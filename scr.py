import discord
from discord.ext import commands
from lib import MTA
import json
from flask import Flask, request,jsonify
import threading
import configparser

# Set up intents and initialize the bot
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
bot = commands.Bot(command_prefix='!', intents=intents)

config = configparser.ConfigParser()
config.read('config.ini')

    # Read values from config file
usernameconfig = config['MTA']['username']
passwrodconfig = config['MTA']['password']
hostconfig = config['MTA']['host']
portconfig = int(config['MTA']['port'])
hostconfig = config['MTA']['host']
resourceconfig = config['MTA']['resource']
tokenconfig = config['MTA']['bottoken']




# Initialize your MTA object with your server credentials
mta = MTA(username=usernameconfig, password=passwrodconfig, host=hostconfig, port=portconfig)
if mta: 
    print("✅ Connected to MTA server.")
else:
    print("❌ Failed to connect to MTA server.")

# =======================================================================
# Command: !players
@bot.command(name='players')
@commands.has_role('Admin')
async def get_players(ctx):
    response = mta.callFunction(resourceconfig, 'getPlayerList')
    if response:
        # Flatten the nested list and join into a string
        flat_list = [item for sublist in response for item in sublist]
        players = ', '.join(flat_list)
        await ctx.send(f"اللاعبون المتصلون: {players}")
    else:
        await ctx.send("⚠️ لا يوجد لاعبين متصلين أو فشل الاتصال.")

# =======================================================================
# Command: !kick <player_name> <reason>
@bot.command(name='kick')
@commands.has_role('Admin')
async def kick(ctx, player_name: str = None, reason: str = None):
    if player_name is None or reason is None:
        await ctx.send("⚠️ Please provide both the player name and a reason. Usage: !kick <player_name> <reason>")
        return

    response = mta.callFunction(resourceconfig, 'kickPlayerByName', player_name, reason)
    if isinstance(response, list):
        response = ' '.join(response)
    await ctx.send(response)

# =======================================================================
# Command: !ban <player_name> <reason>
@bot.command(name='ban')
@commands.has_role('Admin')
async def ban(ctx, player_name: str = None, reason: str = None):
    if player_name is None or reason is None:
        await ctx.send("⚠️ Please provide both the player name and a reason. Usage: !ban <player_name> <reason>")
        return

    response = mta.callFunction(resourceconfig, 'banPlayerByName', player_name, reason)
    if isinstance(response, list):
        response = ' '.join(response)
    await ctx.send(response)

# =======================================================================
# Command: !playersmoney
@bot.command(name='playersmoney')
@commands.has_role('Admin')
async def get_players_money(ctx):
    response = mta.callFunction(resourceconfig, 'getPlayersMoney')
    # If the response is a list with one element that is a dict, extract the dict
    if isinstance(response, list) and len(response) == 1 and isinstance(response[0], dict):
        response = response[0]

    if response and isinstance(response, dict):
        players_money = [f"{player}: {money}" for player, money in response.items()]
        players_money_str = ', '.join(players_money)
        await ctx.send(f"اللاعبون وأموالهم: {players_money_str}")
    else:
        await ctx.send("⚠️ لا يوجد لاعبين متصلين أو فشل الاتصال.")

# =======================================================================
# Command: !givemoney <player_name> <money>
@bot.command(name='givemoney')
@commands.has_role('Admin')
async def give_money(ctx, player_name: str = None, money: int = None):
    if player_name is None or money is None:
        await ctx.send("⚠️ Please provide both the player's name and money amount. Usage: !givemoney <player_name> <money>")
        return

    response = mta.callFunction(resourceconfig, 'setPlayerMoneyByName', player_name, money)
    if isinstance(response, list):
        response_text = response[0]
    else:
        response_text = response
    await ctx.send(response_text)

# =======================================================================
# Command: !setpos <player_name> <x> <y> <z>
@bot.command(name='setpos')
@commands.has_role('Admin')
async def set_player_pos(ctx, player_name: str, x: float, y: float, z: float):
    if player_name is None or x is None or y is None or z is None:
        await ctx.send("⚠️ Please provide the player's name and coordinates. Usage: !setpos <player_name> <x> <y> <z>")
        return

    response = mta.callFunction(resourceconfig, 'setPlayerPos', player_name, x, y, z)
    if response:
        await ctx.send(f"Player {player_name} has been moved to position ({x}, {y}, {z}).")
    else:
        await ctx.send(f"⚠️ Failed to move player {player_name}.")

# =======================================================================
# Command: !getpos <player_name>
@bot.command(name='getpos')
@commands.has_role('Admin')
async def get_player_pos(ctx, player_name: str):
    if player_name is None:
        await ctx.send("⚠️ Please provide the player's name. Usage: !getpos <player_name>")
        return

    response = mta.callFunction(resourceconfig, 'getPlayerPos', player_name)
    if response:
        await ctx.send(response[0])
    else:
        await ctx.send(f"⚠️ Failed to retrieve position for player {player_name}.")

# =======================================================================
# Command: !getskin <player_name>
@bot.command(name='getskin')
@commands.has_role('Admin')
async def get_player_skin(ctx, player_name: str):
    if player_name is None:
        await ctx.send("⚠️ Please provide the player's name. Usage: !getskin <player_name>")
        return

    response = mta.callFunction(resourceconfig, 'getPlayerSkins', player_name)
    if response:
        await ctx.send(response[0])
    else:
        await ctx.send(f"⚠️ Failed to retrieve skin for player {player_name}.")

# =======================================================================
# Command: !setskin <player_name> <skin_id>
@bot.command(name='setskin')
@commands.has_role('Admin')
async def set_player_skin(ctx, player_name: str, skin_id: int):
    if player_name is None or skin_id is None:
        await ctx.send("⚠️ Please provide both the player's name and the skin ID. Usage: !setskin <player_name> <skin_id>")
        return

    response = mta.callFunction(resourceconfig, 'setSkinPlayer', player_name, skin_id)
    if response:
        await ctx.send(response[0])
    else:
        await ctx.send(f"⚠️ Failed to set skin for player {player_name}.")

# The give_player_car function for the Discord bot
@bot.command(name='givecar')
@commands.has_role('Admin')  # Only users with the "Admin" role can use this command
async def give_car(ctx, player_name: str, car_id: int):
    # Check if both player name and car ID are provided
    if player_name is None or car_id is None:
        await ctx.send("⚠️ Please provide both the player's name and car ID. Usage: !givecar <player_name> <car_id>")
        return
    
    # Call MTA function (this should be your actual MTA function to create the car)
    response = mta.callFunction(resourceconfig, 'givePlayerCar', player_name, car_id)

    # If response is a list, remove the square brackets by accessing the first element
    if isinstance(response, list):
        response = response[0]  # Get the first item in the list
    
    # Send the response back to the Discord channel without brackets
    await ctx.send(response)
# Ensure only users with the "Admin" role can use the command
@bot.command(name='getcar')
@commands.has_role('Admin')  # Only users with the "Admin" role can use this command
async def get_car(ctx, player_name: str):
    # Check if player name is provided
    if not player_name:
        await ctx.send("⚠️ Please provide the player's name. Usage: !getcar <player_name>")
        return
    
    # Call MTA function to get the player's vehicle
    response = mta.callFunction(resourceconfig, 'getPlayerVehicle', player_name)

    # If response is a list, access the first element
    if isinstance(response, list):
        response = response[0]  # Get the first item in the list

    # Send the response back to the Discord channel
    await ctx.send(response)

@bot.command(name='warpto')
@commands.has_role('Admin')  # Only users with the "Admin" role can use this command
async def warp_to(ctx, target_player_name: str, player_name: str):
    # Check if both player names are provided
    if not target_player_name or not player_name:
        await ctx.send("⚠️ Please provide both the target player's name and the player name. Usage: !warpto <target_player_name> <player_name>")
        return
    
    # Call MTA function to warp the player to the target's position
    response = mta.callFunction(resourceconfig, 'setPlayerWarpToPlayer', player_name, target_player_name)

    # If response is a list, access the first element
    if isinstance(response, list):
        response = response[0]  # Get the first item in the list

    # Send the response back to the Discord channel
    await ctx.send(response)

@bot.command(name='getweapon')
@commands.has_role('Admin')  # Only users with the "Admin" role can use this command
async def get_weapon(ctx, player_name: str):
    # Check if player name is provided
    if not player_name:
        await ctx.send("⚠️ Please provide the player's name. Usage: !getweapon <player_name>")
        return
    
    try:
        # Call MTA function to get the player's weapon ID
        response = mta.callFunction(resourceconfig, 'getPlayerWeapons', player_name)


        # Check if the response is empty
        if not response or response == "Player not found":
            await ctx.send(f"⚠️ No weapon found for player {player_name}.")
            return

        # If response is a list, access the first element
        if isinstance(response, list):
            response = response[0]  # Get the first item in the list

        # Send the response back to the Discord channel
        await ctx.send(f"Player {player_name} has weapon ID {response}")
    
    except Exception as e:
        # Handle any exception that might occur during the function call
        await ctx.send(f"⚠️ An error occurred while retrieving the weapon: {str(e)}")


@bot.command(name='gethealth')
@commands.has_role('Admin')  # Only users with the "Admin" role can use this command
async def get_health(ctx, player_name: str):
    # Check if player name is provided
    if not player_name:
        await ctx.send("⚠️ Please provide the player's name. Usage: !gethealth <player_name>")
        return
    
    try:
        # Call MTA function to get the player's health
        response = mta.callFunction(resourceconfig, 'getPlayerHealth', player_name)


        # Check if the response is empty or indicates the player was not found
        if not response or response == "Player not found.":
            await ctx.send(f"⚠️ Player {player_name} not found or no health data available.")
            return

        # If response is a list, access the first element
        if isinstance(response, list):
            response = response[0]  # Get the first item in the list

        # Send the response back to the Discord channel
        await ctx.send(f"Player {player_name} has {response} health.")
    
    except Exception as e:
        # Handle any exceptions that might occur during the function call
        await ctx.send(f"⚠️ An error occurred while retrieving the health: {str(e)}")

# Helper function to check if the user has the "Admin" role
def is_admin():
    async def predicate(ctx):
        return any(role.name == "Admin" for role in ctx.author.roles)
    return commands.check(predicate)

# 1️⃣ **Set Admin**
@bot.command(name='setadmin')
@is_admin()
async def set_admin(ctx, player_name: str, acl_name: str = "Admin"):  # Default "Admin" if not provided
    response = mta.callFunction(resourceconfig, 'setAdmin', player_name, acl_name)
    await ctx.send(response[0] if isinstance(response, list) and response else f"⚠️ Failed to set admin for {player_name}.")

# 2️⃣ **Remove Admin**
@bot.command(name='removeadmin')
@is_admin()
async def remove_admin(ctx, player_name: str, acl_name: str = "Admin"):  # Default "Admin" if not provided
    response = mta.callFunction(resourceconfig, 'RemoveAdmin', player_name, acl_name)
    await ctx.send(response[0] if isinstance(response, list) and response else f"⚠️ Failed to remove admin from {player_name}.")


@bot.command(name='getip')
@commands.has_role('Admin')
async def get_player_ip(ctx, player_name: str):
    if not player_name:
        await ctx.send("⚠️ Please provide the player's name. Usage: !getip <player_name>")
        return
    
    response = mta.callFunction(resourceconfig, 'getPlayerIPs', player_name)

    # Debugging: Print raw response
    print(f"DEBUG: getPlayerIPs({player_name}) returned: {response}")

    if response and isinstance(response, list) and response[0]:
        await ctx.send(f"🖥️ IP of {player_name}: {response[0]}")
    else:
        await ctx.send(f"⚠️ Failed to retrieve IP for player {player_name}.")

@bot.command(name='getserial')
@commands.has_role('Admin')
async def get_player_serial(ctx, player_name: str = None):
    if not player_name:
        await ctx.send("⚠️ Please provide the player's name. Usage: !getserial <player_name>")
        return

    response = mta.callFunction(resourceconfig, 'getPlayerSerials', player_name)


    if response and response[0]:  # Ensure response is valid
        await ctx.send(f"🔑 Serial of {player_name}: {response[0]}")
    else:
        await ctx.send(f"⚠️ Failed to retrieve serial for player {player_name}. Maybe they are not online?")

@bot.command(name='getaccount')
@commands.has_role('Admin')
async def get_player_account(ctx, player_name: str):
    if  player_name is None:
        await ctx.send("⚠️ Please provide the player's name. Usage: !getaccount <player_name>")
        return
    
    response = mta.callFunction(resourceconfig, 'getPlayerAccountName', player_name)
    if response:
        await ctx.send(f"👤 Account of {player_name}: {response[0]}")
    else:
        await ctx.send(f"⚠️ Failed to retrieve account name for player {player_name}.")


@bot.command(name='startresource')
@commands.has_role('Admin')
async def start_resource(ctx, resource_name: str):
    if not resource_name:
        await ctx.send("⚠️ Please provide the resource name. Usage: !startresource <resource_name>")
        return

    try:
        # Call the MTA function to start the resource
        response = mta.callFunction(resourceconfig, 'startResources', resource_name)

        # If response is an empty string or None, treat it as failure
        if not response:
            await ctx.send(f"⚠️ Failed to start resource '{resource_name}'. No valid response received.")
        else:
            await ctx.send(f"✅ Resource '{resource_name}' started successfully!")
    except Exception as e:
        # If something goes wrong in the process, send an error message
        await ctx.send(f"An unexpected error occurred: {str(e)}")
# Command: !stopresource <resource_name>
@bot.command(name='stopresource')
@commands.has_role('Admin')
async def stop_resource(ctx, resource_name: str):
    if not resource_name:
        await ctx.send("⚠️ Please provide the resource name. Usage: !stopresource <resource_name>")
        return
    
    try:
        # Call the MTA function to stop the resource
        response = mta.callFunction(resourceconfig, 'stopResources', resource_name)

        # If the response is None or empty, treat it as failure
        if not response:
            await ctx.send(f"⚠️ Failed to stop resource '{resource_name}'. No valid response received.")
        else:
            await ctx.send(f"✅ Resource '{resource_name}' stopped successfully!")
    except Exception as e:
        # If something goes wrong in the process, send an error message
        await ctx.send(f"An unexpected error occurred: {str(e)}")

@bot.command(name='getresourceState')
@commands.has_role('Admin')
async def get_resource_state(ctx, resource_name: str):
    if not resource_name:
        await ctx.send("⚠️ Please provide the resource name. Usage: !getresourceState <resource_name>")
        return
    
    try:
        # Call the MTA function to get the resource state
        response = mta.callFunction(resourceconfig, 'getResourceStated', resource_name)
        
        # Check if the response is a valid state and it's a list with at least one item
        if response and isinstance(response, list) and len(response) > 0:
            # Get the state as a string (remove the list brackets)
            state = response[0]
            await ctx.send(f"✅ The state of resource '{resource_name}' is: {state}")
        else:
            await ctx.send(f"⚠️ Failed to get the state of resource '{resource_name}'. Error: {response}")
    
    except Exception as e:
        # Handle unexpected errors
        await ctx.send(f"An unexpected error occurred: {str(e)}")
@bot.command(name='startresource')
@commands.has_role('Admin')
async def start_resource(ctx, resource_name: str):
    if not resource_name:
        await ctx.send("⚠️ Please provide the resource name. Usage: !startresource <resource_name>")
        return

    try:
        # Call the MTA function to start the resource
        response = mta.callFunction(resourceconfig, 'startResources', resource_name)

        # If response is an empty string or None, treat it as failure
        if not response:
            await ctx.send(f"⚠️ Failed to start resource '{resource_name}'. No valid response received.")
        else:
            await ctx.send(f"✅ Resource '{resource_name}' started successfully!")
    except Exception as e:
        # If something goes wrong in the process, send an error message
        await ctx.send(f"An unexpected error occurred: {str(e)}")
# Command: !stopresource <resource_name>
@bot.command(name='stopresource')
@commands.has_role('Admin')
async def stop_resource(ctx, resource_name: str):
    if not resource_name:
        await ctx.send("⚠️ Please provide the resource name. Usage: !stopresource <resource_name>")
        return
    
    try:
        # Call the MTA function to stop the resource
        response = mta.callFunction(resourceconfig, 'stopResources', resource_name)

        # If the response is None or empty, treat it as failure
        if not response:
            await ctx.send(f"⚠️ Failed to stop resource '{resource_name}'. No valid response received.")
        else:
            await ctx.send(f"✅ Resource '{resource_name}' stopped successfully!")
    except Exception as e:
        # If something goes wrong in the process, send an error message
        await ctx.send(f"An unexpected error occurred: {str(e)}")


CHANNEL_ID = 1098574958021595216  # ID القناة في Discord
# إنشاء سيرفر Flask للاستماع إلى رسائل MTA
app = Flask(__name__)


async def send_to_discord(sender, message):
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(f"📝 {sender}: {message}")
    else:
        print("⚠️ Error: Could not find the Discord channel!")


@app.route('/chat', methods=['POST'])
def receive_chat():
    try:
        # إجبار Flask على تحليل JSON حتى لو كان غير مثالي
        data = request.get_json(force=True)
        
        # إذا كانت البيانات عبارة عن قائمة، نستخرج العنصر الأول
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        
        # التحقق من وجود المفاتيح المطلوبة
        if not data or "message" not in data or "sender" not in data:
            print(f"⚠️ Invalid data received: {data}")
            return jsonify({"error": "Invalid data format"}), 400

        sender = data["sender"]
        message = data["message"]
        print(f"📩 Received message from MTA: {sender}: {message}")

        # إنشاء مهمة لإرسال الرسالة إلى Discord
        bot.loop.create_task(send_to_discord(sender, message))
        return jsonify({"status": "Message sent"}), 200

    except Exception as e:
        print(f"❌ Error in Flask: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

##############################################
@bot.event
async def on_ready():
    print(f'✅ Bot connected as {bot.user}')

threading.Thread(target=lambda: app.run(host="0.0.0.0", port=5000)).start()

import requests
data = {"sender": "Ahmed_Ly", "message": "Hello everyone!"}
response = requests.post("http://127.0.0.1:5000/chat", json=data)
print(response.text)


# =======================================================================

bot.run(tokenconfig)
