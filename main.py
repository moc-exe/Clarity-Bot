import discord
from discord.ext import commands
from pypresence import Presence
from discord import app_commands
import time
import threading
import os
import clarity_groq_tools as cgt
import clarity_open_weather
import groq
import clarity_tabgraphics
import clarity_email_tools


clarity_discord_key = os.getenv("CLARITY_DISCORD_TOKEN")
groq_api_key=os.getenv("GROQ_API_KEY")
groq_model = "llama3-8b-8192"


intents = discord.Intents.default()
intents.guilds = True  
intents.dm_messages = True 
intents.message_content = True



groq_client = groq.Client(api_key=groq_api_key)
bot = commands.Bot(command_prefix="/", intents=intents)

CLIENT_ID = '1296313809883107338'  
rpc = Presence(CLIENT_ID)

def start_rich_presence():
    rpc.connect()
    while True:
        rpc.update(
            state="listening to /ask /tabgraphics /weather",          
            large_image="embedded_cover",    
            details="I'm Clarity, nice to meet you!"
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
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="yapping"))

@bot.tree.command(name="sayhello")
async def sayhello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, my name is Clarity! Nice to meet you!")

@bot.tree.command(name="whomadeyou")
async def whomadeyou(interaction: discord.Interaction):
    await interaction.response.send_message("I'm being developed by moc!")


@bot.tree.command(name="tabgraphics")
async def tabgraphics(interaction: discord.Interaction):
    await interaction.response.send_message(file=discord.File(clarity_tabgraphics.get_random_tabgraphic_path()))


@bot.tree.command(name="ask")
@app_commands.describe(question=f"The question to ask {groq_model}")
async def askgroq(interaction: discord.Interaction, question: str):
    response = cgt.get_response(groq_client, question, groq_model)
    await interaction.response.send_message(f"\n\n### Your Question:\n {question} \n\n### The reply from {groq_model}:\n {response}\n\n\nHope it helps, your Clarity :smiley_cat:")

@bot.tree.command(name="weather")
@app_commands.describe(city="Enter a city for which you'd like to know the weather")
async def weather(interaction: discord.Interaction, city:str = "Montreal"): # defaulted to MTL, will be an optional slash command arg
    response = clarity_open_weather.get_weather(city)
    await interaction.response.send_message(response)

@bot.tree.command(name="textme")
@app_commands.describe(body="body of your message", subject="subject (optional)")
async def textme(interaction: discord.Interaction, body:str, subject:str="No subject"):
    
    username = interaction.user.name
    guildname = interaction.guild.name if interaction.guild else "direct message"
    status = clarity_email_tools.send_text_to_self(subject, body, username, guildname)
    if status == True: 
        await interaction.response.send_message("Your message was successfully delivered, thank you! :white_check_mark: ")
    else:
        await interaction.response.send_message("Sorry, your message couldn't be delivered at this time... :cross_mark: ")


bot.run(clarity_discord_key)


