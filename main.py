import discord
from discord.ext import commands
from pypresence import Presence
from discord import app_commands
from discord.ext import tasks, commands
import time
import threading
import os
import clarity_groq_tools as cgt
import clarity_open_weather
import groq
import clarity_tabgraphics
import clarity_email_tools
import clarity_filewalker
import clarity_youtube_tools as clarity_yt
import clarity_emotes
import clarity_google_search as c_google
import clarity_cbc_tools
import util_time_formatter


clarity_discord_key = os.getenv("CLARITY_DISCORD_TOKEN")
groq_api_key=os.getenv("GROQ_API_KEY")
groq_model = "llama3-8b-8192"
news_channel_IDs = [1321252031553474582,1321986669183766528]
test_channel_ID = 1289086658817556480

intents = discord.Intents.default()
intents.guilds = True  
intents.dm_messages = True 
intents.messages = True
intents.message_content = True

groq_client = groq.Client(api_key=groq_api_key)
bot = commands.Bot(command_prefix="!", intents=intents)

CLIENT_ID = '1296313809883107338'  
rpc = Presence(CLIENT_ID)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        check_for_news.start()
        print(f"News checking routine started")
    except Exception as e:
        print(f"Failed to sync commands: {e}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="yapping"))


def start_rich_presence():
    try:
        rpc.connect()

        while True:
            rpc.update(
                state=f"I'm Clarity, nice to meet you!",          
                large_image="embedded_cover",    
                details = "/ask /youtube /tabgraphics /sendtext /weather /googlesearch"
            )
            time.sleep(15)
    
    except Exception as e: 
        print(f"Rich Presence Attempt Failed: {e}")
        return False

rich_presence = start_rich_presence
if rich_presence:
    threading.Thread(target=start_rich_presence, daemon=True).start()


@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="sayhello")
async def sayhello(interaction: discord.Interaction):
    
    '''says hello'''
    
    await interaction.response.send_message("Hello, my name is Clarity! Nice to meet you!")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="whomadeyou")
async def whomadeyou(interaction: discord.Interaction):

    '''
    owner
    '''

    await interaction.response.send_message("I'm being developed by moc!")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="tabgraphics")
async def tabgraphics(interaction: discord.Interaction):

    '''
    randomly sends an image from a Tabgraphics volume
    '''

    await interaction.response.send_message(clarity_tabgraphics.get_yandere_url())

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="ask")
@app_commands.describe(question=f"The question to ask {groq_model}")
async def askgroq(interaction: discord.Interaction, question: str):
    
    '''
    communicates with an AI chatbot and returns you an answer
    '''
    
    result = cgt.get_response(groq_client, question, groq_model)
    if len(result) < 2:
        await interaction.response.send_message(f"\n\n### Your Question:\n {question} \n\n### The reply from {groq_model}:\n {result[0]}\n\n\nHope it helps, your Clarity :smiley_cat:")
    else:

        for i in range(len(result)):
            print(i, end=": ")
            print(len(result[i]))

        await interaction.response.send_message(f"\n\n### Your Question:\n {question} \n\n### The reply from {groq_model}:\n {result[0]}\n")
        for i in range(1, len(result)):
            await interaction.followup.send(f"{result[i]}")
        await interaction.followup.send(f"Hope it helps, your Clarity :smiley_cat:")


@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="currentweather")
@app_commands.describe(city="Enter a city for which you'd like to know the weather", state = "State / Province / Territory", country = "use 2-letter code e.g. CANADA = CA")
async def weather(interaction: discord.Interaction, city:str = "Montreal", state:str = None, country:str = None): # defaulted to MTL, will be an optional slash command arg
    
    '''
    gets current weather conditions
    '''
    
    response = clarity_open_weather.get_current_weather(clarity_open_weather.geocoder_to_coords(city, state, country))
    await interaction.response.send_message(response)

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="5dayweather")
@app_commands.describe(city="Enter a city for which you'd like to know the weather for the next 5 days", state = "State / Province / Territory", country = "use 2-letter code e.g. CANADA = CA")
async def fivedayweather(interaction: discord.Interaction, city:str = "Montreal", state:str = None, country:str = None): # defaulted to MTL, will be an optional slash command arg
    
    '''
    gets a detailed weather forecast for the next 5 days
    '''
    
    response = clarity_open_weather.get_5_day_forecast(clarity_open_weather.geocoder_to_coords(city, state, country))
    await interaction.response.send_message(response[0])
    for i in range(1, len(response)): 
        await interaction.followup.send(f"{response[i]}")


# @discord.app_commands.allowed_installs(guilds=True, users=True)
# @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
# @bot.tree.command(name="getemote")
# @app_commands.describe(name="name of the emote")
# async def getemote(interaction: discord.Interaction, name:str):

#     if name in clarity_emotes.global_emote_dict.keys():
#         if name.startswith('a:'):
#            await interaction.response.send_message(f"<{name}:{clarity_emotes.global_emote_dict[name]}>")
#         else:
#             await interaction.response.send_message(f"<:{name}:{clarity_emotes.global_emote_dict[name]}>")
#     else:
#         await interaction.response.send_message(f"No such emote sadly ... <:zerotsu_sadge:1312653671737327656>")

# @discord.app_commands.allowed_installs(guilds=True, users=True)
# @discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
# @bot.tree.command(name="getemotenames")
# async def getemotenames(interaction: discord.Interaction):
#     await interaction.response.send_message(f"{clarity_emotes.get_emote_keys()}")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="textme")
@app_commands.describe(body="body of your message", subject="subject (optional)")
async def textme(interaction: discord.Interaction, body:str, subject:str="No subject"):
    '''
    sends a text message to the bot owner
    '''
    username = interaction.user.name
    guildname = interaction.guild.name if interaction.guild else "direct message"
    status = clarity_email_tools.send_text_to_self(subject, body, username, guildname)
    if status == True: 
        await interaction.response.send_message("Your message was successfully delivered, thank you! :white_check_mark: ")
    else:
        await interaction.response.send_message("Sorry, your message couldn't be delivered at this time... :cross_mark: ")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="youtube")
@app_commands.describe(query="your query to retrieve a video")
async def youtube(interaction: discord.Interaction, query:str):
    '''
    searches youtube for your query and retrieves the first result
    '''
    res = clarity_yt.public_yt_query(query)
    await interaction.response.send_message(res)
   
@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="googlesearch")
@app_commands.describe(query="your query to search the web", limit = "max number of results to retrieve (1-10 only)", desc = "descriptions for your search results")
async def googlesearch(interaction: discord.Interaction, query:str, limit:int = 10, desc:bool = False):
    '''
    browses the web for your query and returns the result
    '''
    res = c_google.web_search(query, limit, desc)
    formatted_res = c_google.format_web_search(res)
    await interaction.response.send_message(f"\n\n### Your search query : {query}\n {formatted_res[0]}\n")
    for i in range(1, len(formatted_res)):
        await interaction.followup.send(f"{formatted_res[i]}")
    await interaction.followup.send(f"Hope it helps, your Clarity :smiley_cat:")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="googleimage")
@app_commands.describe(prompt="your prompt to find a picture", 
                       limit = "max number of results to retrieve (1-10 only)", 
                       color = "dominant color in the picture", 
                       size = 'huge / icon / large / medium / small / xlarge / xxlarge', 
                       image_type = "clipart/face/lineart/stock/photo/animated", 
                       custom_link = "custom website url to search")
async def googleimage(interaction: discord.Interaction, 
                      prompt:str, limit:int=5,
                      color:str=None,
                      size:str=None,
                      image_type:str=None,
                      custom_link:str=None):
    '''
    finds a picture online based on your description
    '''
    # def image_search(prompt:str, color:str=None, limit:int=10, size:str=None, image_type:str=None, custom_link:str=None) -> list[str]:
    res = c_google.image_search(prompt, color, limit, size, image_type, custom_link)
    formatted_res = c_google.format_web_search(res)
    await interaction.response.send_message(f"## Your search query : {prompt}\n {formatted_res[0]}\n")
    for i in range(1, len(formatted_res)):
        await interaction.followup.send(f"{formatted_res[i]}")


@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.command(name='ntabgraphics')
async def numoftabs(ctx):
    '''Displays number of currently scraped pictures from yandere website with tags = tabgraphics'''
    if await bot.is_owner(ctx.author):
        await ctx.send(f'Currently scraped : {len(clarity_tabgraphics.yandere_large_pics)} pics from yandere')
    else:
        await ctx.send(f"Sorry, {ctx.author.mention}, you are not authorized to use this command. :eyes: ")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.command(name='getmusicvault')
async def getmusicvault(ctx: commands.Context) -> None:
    '''Displays currently stored music collection as a filetree'''
    if await bot.is_owner(ctx.author):
        message = clarity_filewalker.print_tree(clarity_filewalker.build_filetree(clarity_filewalker.curr_root_dir))
        message_list = clarity_filewalker.split_text_by_newlines(message)
        await ctx.send("## Currently stored\n")

        for m in message_list:
            await ctx.send(f"```{m}```")
    else:
        await ctx.send(f"Sorry, {ctx.author.mention}, you are not authorized to use this command. :eyes: ")

@discord.app_commands.allowed_installs(guilds=True, users=True)
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.command(name='getf')

async def getf(ctx: commands.Context, filepath: str = None) -> None:
    '''Retrieves and uploads a file provided the path is valid and the size is valid to be uploaded'''
    if await bot.is_owner(ctx.author):
        
        checkup = clarity_filewalker.check_is_file_and_size(filepath)
        '''meow meow'''
        if checkup[0]:
            await ctx.send(file=discord.File(checkup[1]))
        else:
            await ctx.send(checkup[1])

    else:
        await ctx.send(f"Sorry, {ctx.author.mention}, you are not authorized to use this command. :eyes: ")


news_counter = 0
@tasks.loop(minutes = 30)
async def check_for_news():
    global news_counter
    news_counter+=1
    print(f"### [!] {util_time_formatter.get_curr_timestamp()} I'm checking for news")
    channels = [bot.get_channel(channel) for channel in news_channel_IDs]
    # await channel.send(f"### [!] {util_time_formatter.get_curr_timestamp()} I'm checking for news")
    if not channels:
        print(f"[!] {util_time_formatter.get_curr_timestamp()} Clarity couldnt connect to the news channel...")
        return

    articles = await clarity_cbc_tools.fetch_news()
    
    if news_counter <= 1:
        for channel in channels:
            await channel.send("Back online, I'm checking for news.")
    else:
        for channel in channels: 
            for article in articles:
                await channel.send(article)


bot.run(clarity_discord_key)
