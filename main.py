import discord
from discord.ext import commands
from pypresence import Presence
from discord import app_commands
import time
import threading
import os
import groqclient


clarity_discord_key = os.getenv("CLARITY_DISCORD_TOKEN")
groq_api_key=os.getenv("GROQ_API_KEY")


intents = discord.Intents.default()
intents.guilds = True  
intents.dm_messages = True 
intents.message_content = True

tabIndex = 1
numfilesTabgraphics = 5


groq_client = groqclient.Client(api_key=groq_api_key)
bot = commands.Bot(command_prefix="/", intents=intents)

CLIENT_ID = '1296313809883107338'  
rpc = Presence(CLIENT_ID)

def start_rich_presence():
    rpc.connect()
    while True:
        rpc.update(
            state="Playing with my girl",          
            large_image="embedded_cover",    
            details="hewwo world, I'm Clarity-bot!"
        )
        time.sleep(15)


threading.Thread(target=start_rich_presence, daemon=True).start()


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="sayhello")
async def sayhello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, my name is Clarity! Nice to meet you!")

@bot.tree.command(name="whomadeyou")
async def whomadeyou(interaction: discord.Interaction):
    await interaction.response.send_message("I'm being developed by moc!")


@bot.tree.command(name="tabgraphics")
async def tabgraphics(interaction: discord.Interaction):
    global tabIndex
    tabIndex = ((tabIndex + 1) % numfilesTabgraphics) + 1
    await interaction.response.send_message(f"Tabgraphics No{tabIndex}", file=discord.File(f"./tabgraphics/tab{tabIndex}.jpg"))


@bot.tree.command(name="ask")
@app_commands.describe(question="The question to ask GROQ")
async def askgroq(interaction: discord.Interaction, question: str):
    response = groqclient.get_response(groq_client, question)
    await interaction.response.send_message(f"\n\n### Your Question:\n {question} \n\n### The reply from GROQ:\n {response}\n\n\nHope it helps, your Clarity :smiley_cat:")


bot.run(clarity_discord_key)


