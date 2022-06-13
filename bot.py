import discord
from discord.ext import commands
from scraper import *
import config


bot = commands.Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Servers: ", bot.guilds)


@bot.command(name="fd", help="Get frame data of a characters move from dustloop. Input arguments as [game] [character] [input].\n"
                             'Note: for inputs using spaces, input with quotes (e.g "236D > 4D" or "Ky Kiske")')
async def get_frame_data(ctx, *args):
    
    if len(args) >= 1:  # Only game name inputted. Show character names.
        game = args[0].upper()
        # if game not in SUPPORTED_GAMES:
        if not get_game_characters(game_title=game):
            await ctx.send(f"Invalid game. Use **$fd** to check supported games.")
            return 

        if len(args) >= 2:  # Character name inputted. Show moves of character.
            character = args[1]
            framedata, movelist = get_character_framedata(character, game_title=game)
            if not movelist:  # Character name doesn't exist
                await ctx.send("Invalid character name. Use **$fd [game]** to check character names.")
                return

            if len(args) >= 3:  # Move input entered. Show frame data of character move.
                move = args[2].upper()
                move_data = get_move_data(framedata, movelist, move)
                if not move_data:
                    await ctx.send(f"Invalid move '{args[2]}'. Use **$fd [game] [character]** to check moves inputs.")
                    return

                framedata_embed = create_embed_move_data(move_data)
                # print(move_data)
                await ctx.send(embed=framedata_embed)
                return 1  # Success

            await ctx.send(movelist)
            return 1

        await ctx.send(get_game_characters(game_title=game))
        return 1

    await ctx.send(f"Supported games: {SUPPORTED_GAMES}")  # Nothing input after $fd

def create_embed_move_data(move_data: dict) -> discord.Embed:
    embed_title = "{} {}".format(move_data["character"], move_data["input"])
    if "name" in move_data.keys():
        embed_title += " ({})".format(move_data["name"])

    embed_description = ("Startup: {}, Active: {}, Recovery: {}, On-Block: {}\n"
                        "Damage: {}, Guard: {} \nInvuln: {}"
                        .format(move_data["startup"], move_data["active"], move_data["recovery"], move_data["onBlock"],
                        move_data["damage"], move_data["guard"], move_data["invuln"]))

    embed_image_url = get_move_hitbox_image_url(move_data["images"])
    # print(embed_image_url)

    # add a link to the embed that goes to wiki page

    embed = discord.Embed(title=embed_title,
                        description=embed_description,
                        )
    embed.set_thumbnail(url=embed_image_url)
    return embed


bot.run(config.discord_bot_token)
