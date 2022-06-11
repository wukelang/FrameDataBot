from shutil import move
import discord
from discord.ext import commands
from matplotlib import image


from scraper import *
import config


SUPPORTED_GAMES = ["GGACPR"]

bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Servers: ", bot.guilds)


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
            # await ctx.send(move_data)
            framedata_embed = create_embed_move_data(move_data)
            # print(move_data)
            await ctx.send(embed=framedata_embed)


def create_embed_move_data(move_data: dict) -> discord.Embed:
    embed_title = "{} {}".format(move_data["character"], move_data["input"])
    embed_description = ("Startup: {}, Active: {}, Recovery: {}"
                        .format(move_data["startup"], move_data["active"], move_data["recovery"]))
    # embed_image_url = "http://dustloop.com/" + (move_data["images"][0]).split()[0]
    embed_image_url = "http://dustloop.com/" + move_data["images"][0]
    print(embed_image_url)

    embed = discord.Embed(title=embed_title,
                        description=embed_description,
                        )
    embed.set_image(url=embed_image_url)
    return embed


bot.run(config.discord_bot_token)
