import asyncio
import json
import os
import discord
import requests
import youtube_dl

from discord.ext import commands
from youtube_search import YoutubeSearch

from features import *
from settings import *

client = discord.Client()
bot = commands.Bot(command_prefix=config.COMMANDPREFIX,
                   case_insensitive=True)  # Makes !help == !HELP == !HeLp
bot.remove_command('help')


@bot.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(bot.user.name))
    print('Client ID: ' + str(bot.user.id))
    print('Invite URL: ' + 'https://discordapp.com/oauth2/authorize?&client_id='
          + str(bot.user.id) + '&scope=bot&permissions=0')
    await bot.change_presence(activity=discord.Game(name="ONLINE"))


# Shuts the bot down - only usable by the bot owner specified in config
@bot.command(name='shutdown')
async def shutdown(ctx):
    try:
        if str(ctx.author.id) == config.OWNERID:
            print('ok')
            await ctx.channel.send('Shutting down. Bye!')
            await client.close()
            await bot.close()
        else:
            await ctx.channel.send('Only owner of the bot can use this command!')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Allows owner to reset the game status of the bot
@bot.command(name='reset_status')
async def reset_status(ctx):
    try:
        if str(ctx.author.id) == config.OWNERID:
            await bot.change_presence(activity=discord.Game(name="ONLINE"))
        else:
            await ctx.channel.send('Only owner of the bot can use this command!')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Allows owner to set the game status of the bot
@bot.command(name='set_status')
async def set_status(ctx):
    try:
        if str(ctx.author.id) == config.OWNERID:
            status = ctx.message.content.split()
            if 12 > len(status) > 1:
                await bot.change_presence(activity=discord.Game(name=' '.join(status[1:])))
            else:
                await ctx.channel.send('Status mast be from one to ten words len!')
        else:
            await ctx.channel.send('Only owner of the bot can use this command!')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Help Message, sends a personal message with a list of all the commands
# and how to use them correctly
@bot.command(name='help')
async def help(ctx):
    if ' '.join(str(ctx.channel).split()[3:]) != str(ctx.author):
        await ctx.channel.send('Sending you a PM!')
    await ctx.author.send(helpMessage.helpMessage)


# Sends a personal message with the invite link of the bot
@bot.command(name='invite_link')
async def invite_link(ctx):
    try:
        if ' '.join(str(ctx.channel).split()[3:]) != str(ctx.author):
            await ctx.channel.send('Sending you a PM!')
        await ctx.author.send('Invite URL: ' + 'https://discordapp.com/oauth2/authorize?&client_id='
                              + str(bot.user.id) + '&scope=bot&permissions=0')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Sends a conted number from line like <<a + b / c>>
@bot.command(name='count')
async def count(ctx):
    try:
        await ctx.channel.send("Counted!")
        await ctx.channel.send(eval(' '.join(ctx.message.content.split()[1:])))
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Searches the second word following python_help in python docs
@bot.command(name='python_help')
async def python_help(ctx):
    try:
        messagetext = ctx.message.content
        split = messagetext.split(' ')
        if len(split) == 2:
            messagetext = split[1]
            if ' '.join(str(ctx.channel).split()[3:]) != str(ctx.author):
                await ctx.channel.send('Sending you a PM!')
            await ctx.author.send('https://docs.python.org/3/search.html?q=' + messagetext)
        else:
            await ctx.channel.send('Name of library mast be one word')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Messages a random chuck norris joke - do not use, they're bloody terrible
@bot.command(name='joke')
async def joke(ctx):
    try:
        random_joke = requests.get('http://api.icndb.com/jokes/random?')
        if random_joke.status_code == 200:
            out = random_joke.json()['value']['joke']
            await ctx.channel.send(out)
        else:
            await ctx.channel.send('Error 404. Website may be down.')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Random coin flip
@bot.command(name='coinflip')
async def coinflip(ctx):
    try:
        await ctx.channel.send(rng.get_coin_face())
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


@bot.command(name='dice')
async def dice(ctx):
    try:
        await ctx.channel.send(rng.rollDice(ctx.message.content))
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Slots machine in emoji format for discord
@bot.command(name='slots')
async def slots(ctx):
    try:
        await ctx.channel.send(rng.get_slots_screen())
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Random cat gif
@bot.command(name='catgif')
async def catgif(ctx):
    try:
        await ctx.channel.send(cats.get_cat_gif())
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Random cat picture
@bot.command(name='cat')
async def cat(ctx):
    try:
        await ctx.channel.send(cats.get_cat_picture())
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# **************** TRANSLATE COMMANDS **************** #
tr_url = "https://translated-mymemory---translation-memory.p.rapidapi.com/api/get"
lang_pair = "ru|en"

headers = {
    'x-rapidapi-key': "7e5cc6f72fmshd5472477a995ccep10b72cjsnaed447d4c2e9",
    'x-rapidapi-host': "translated-mymemory---translation-memory.p.rapidapi.com"
}

languages = {
        "английский": 'en',
        "немецкий": 'de',
        "испанский": "es",
        "украинский": 'uk',
        "польский": "pl",
        "французский": "fr",
        'русский': 'ru'
    }


# Return translation of user message {base from ru to en}
@bot.command(name='translate')
async def translate(ctx):
    try:
        to_tranclate = ' '.join(ctx.message.content.split()[1:])
        try:
            global lang_pair
            querystring = {"q": to_tranclate, "langpair": lang_pair, "de": "a@b.c", "onlyprivate": "0", "mt": "1"}
            response = requests.request("GET", tr_url, headers=headers, params=querystring)
            translation = response.json()['matches'][0]['translation']
            await ctx.channel.send(translation)
        except:
            await ctx.channel.send("Wrong text to translate or wrong language chosen")
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Allow user to set language to translate from - to
@bot.command(name="set_lang")
async def set_lang(ctx):
    try:
        global languages

        try:
            lan1 = languages[ctx.message.content.split()[1].lower()]
            lan2 = languages[ctx.message.content.split()[2].lower()]

            global lang_pair
            lang_pair = f'{lan1}|{lan2}'
            await ctx.channel.send("Done!")

        except:
            await ctx.channel.send("Wrong or unsupported language!"
                                   "(you can see list of the supported languages with command list_lang)")
            await ctx.channel.send("You may ask set_language [language from] [language to]")
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


@bot.command(name="list_lang")
async def list_lang(ctx):
    try:
        if ' '.join(str(ctx.channel).split()[3:]) != str(ctx.author):
            await ctx.channel.send('Sending you a PM!')
        global languages
        await ctx.author.send('Supported languages for this moment:')
        await ctx.author.send('\n'.join(languages.keys()))
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# **************** VOICE COMMANDS **************** #
# Will join the voice channel of the message author if they're in a channel
# and the bot is not currently connected to a voice channel
currentChannel = None


@bot.command(name='join')
async def join(ctx):
    try:
        if ctx.author.voice and ctx.author.voice.channel:
            global currentChannel
            currentChannel = ctx.author.voice.channel
            if ctx.voice_client is not None:
                return await ctx.voice_client.connect()

            await currentChannel.connect()
        else:
            await ctx.send('You are not in a voice channel.')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Will leave the current voice channel
@bot.command(name='leave')
async def leave(ctx):
    try:
        global currentChannel
        if currentChannel is not None:
            if ctx.author.voice and ctx.author.voice.channel:
                if ctx.author.voice.channel == currentChannel:
                    await ctx.voice_client.disconnect()
                else:
                    await ctx.send('You mast be in my voice chat to do this!')
            else:
                await ctx.send('You are not in voice chat!')
        else:
            await ctx.send('I am not in voice chat!')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        try:
            loop = loop or asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=True))
            if 'entries' in data:
                # take first item from a playlist
                data = data['entries'][0]
            global filename
            filename = ytdl.prepare_filename(data)
            print(filename)
            # For playing music at this bot you need to download ffmpeg.exe player and add it directory to Path
            # After you did it you need to put way to ffmpeg.exe to key executable=
            return cls(discord.FFmpegPCMAudio(source=filename, **ffmpeg_options,
                                              executable='C:/PATH_Programms/ffmpeg.exe'), data=data)
        except:
            pass


# Plays from a url (almost anything youtube_dl supports)
@bot.command(name='play')
async def play(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        try:
            async with ctx.typing():
                global player
                request = ' '.join(ctx.message.content.split()[1:])
                results = YoutubeSearch(request, max_results=1).to_json()
                results_dict = json.loads(results)
                url = 'https://www.youtube.com' + results_dict['videos'][0]['url_suffix']
                player = await YTDLSource.from_url(url, loop=bot.loop)
                ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
                ctx.voice_client.is_playing()

                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                    name=player.title))
                await ctx.send(f'Now playing: {player.title}, \n {url}')
        except discord.errors.ClientException as er:
            print(er)
            await ctx.send('Some troubles with player!')
    else:
        await ctx.send('You are not in voice chat!')


# Changes the player's volume
@bot.command(name='set_volume')
async def set_volume(ctx, volume: int):
    try:
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"Changed volume to {volume}%")
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Will pause the audio player
@bot.command(name='pause')
async def pause(ctx):
    try:
        if ctx.voice_client.is_playing():
            try:
                ctx.voice_client.pause()
                await bot.change_presence(activity=discord.Game(name="ONLINE"))

            except NameError:
                await ctx.channel.send('Not currently playing audio.')
        else:
            await ctx.channel.send('Not currently playing audio.')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Will resume the audio player
@bot.command(name='resume')
async def resume(ctx):
    try:
        if ctx.voice_client.is_playing:
            try:
                ctx.voice_client.resume()
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=player.title))
            except NameError:
                await ctx.channel.send('Not currently playing audio.')
        else:
            await ctx.channel.send('Not currently playing audio.')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


# Will stop the audio player
@bot.command(name='stop')
async def stop(ctx):
    try:
        try:
            ctx.voice_client.stop()
            await bot.change_presence(activity=discord.Game(name="ONLINE"))
            await asyncio.sleep(5)
            path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)
            os.remove(path)
        except NameError:
            await ctx.channel.send('Not currently playing audio.')
    except:
        await ctx.send('Sorry some troubles i cant do it now(')


@client.event
async def on_message(message):
    print(message)
    # If the message author isn't the bot and the message starts with the
    if message.author.name != bot.user.name and not message.content.startswith(config.COMMANDPREFIX):
        text = message.content.lower()
        await message.channel.send(text)
    else:
        pass


if __name__ == '__main__':
    bot.run(config.TOKEN)
    client.run(config.TOKEN)
