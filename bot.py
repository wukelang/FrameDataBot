# import discord
from discord.ext import commands
from scraper import *
import config

# client = discord.Client()

# @client.event
# async def on_ready():
#     print(f'Logged in as {client.user}')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('$fd'):
#         await message.channel.send('Hello!')

# client.run(config.discord_bot_token)

SUPPORTED_GAMES = ["GGACPR"]

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command(name="fd", help="Get frame data of a characters move from dustloop. Input arguments as [game] [character] [input].")
async def get_frame_data(ctx, *args):
    
    args = [arg.lower() for arg in args]

    if args == []:
        await ctx.send(f"Supported games: {SUPPORTED_GAMES}")

    elif len(args) == 1:  # Only game name inputted. Show character names.
        # only supports ggacpr for now
        await ctx.send(ggacpr_chara_name_keys)

    elif len(args) >= 2:
        framedata, movelist = get_character_framedata(args[1])
        if not movelist:  # Character name doesn't exist
            await ctx.send("Invalid character name.")
            return
        else:
            await ctx.send(movelist)

        if len(args) >= 3:
            move_data = get_move_data(framedata, movelist, args[2])
            if not move_data:
                await ctx.send(f"Invalid move: '{args[2]}'")
                return
            await ctx.send(move_data)

    
bot.run(config.discord_bot_token)
