import string
from typing import Tuple
from bs4 import BeautifulSoup
import requests


SITE_URL = "https://dustloop.com"


def get_game_characters(game_title: string = "ggacpr") -> list:
    # Helper function that retrieves proper names of the characters for website URLs.
    # List should be sorted from the website.
    # url = f"http://dustloop.com/wiki/index.php?title={url}"
    url = "http://dustloop.com/wiki/index.php?title=Guilty_Gear_XX_Accent_Core_Plus_R"

    page = requests.get(url)
    if page.status_code != 200:
        print(f"{page.status_code} error occurred!")
    else:
        soup = BeautifulSoup(page.content, "html.parser")
        character_panel = soup.find("div", id="fpbottomsection")
        character_table = character_panel.find("div", class_="columns")
        character_names = character_table.find_all("b")

        return [name.text for name in character_names]

ggacpr_chara_name_keys = ["aba", "anji", "axl", "baiken", "bridget", "chipp", "dizzy", "eddie", "faust", "ino",
                                "jam", "johnny", "justice", "kliff", "ky", "may", "millia", "ordersol", "potemkin", "robo",
                                "slayer", "sol", "testament", "venom", "zappa"]

ggacpr_characters = dict(zip(ggacpr_chara_name_keys, get_game_characters()))


def get_character_framedata(chara_name: string) -> Tuple:
    # Primary function that webscrapes dustloop frame data tables.
    # Returns tuple with two lists containing data for each move and move inputs for indexing.
    moves = []  # Contains dicts that represents a move column.
    move_inputs = []

    if chara_name in ggacpr_chara_name_keys:  # Check if name is a proper abbreviation
        chara_name = ggacpr_characters[chara_name]

    url = "http://dustloop.com/wiki/index.php?title=GGACR/{}/Frame_Data".format(chara_name)
    page = requests.get(url)
    if page.status_code != 200:
        print(f"{page.status_code} error occurred!")

    else:
        soup = BeautifulSoup(page.content, "html.parser")
        fd_tables = soup.find_all("table", class_="display")

        for table in fd_tables:
            # Get header values for dict keys.
            table_header = table.find("tr")
            header_data = [col.text for col in table_header.find_all("th")]

            # Create dict for each move.
            table_body = table.find("tbody").find_all("tr")
            for move_row in table_body:
                move_details = [col.text for col in move_row.find_all("td")]
                move_data = dict(zip(header_data, move_details))

                bonus_details = move_row["data-details"]  # Get HTML shown from control button (images, notes)
                details_html = BeautifulSoup(bonus_details, "html.parser")
                move_images = details_html.find_all("img")
                # image_urls = [SITE_URL + image["src"] for image in move_images]
                try:
                    image_urls = [SITE_URL + image["srcset"].split()[0] for image in move_images]
                except KeyError:  # If srcset attribute isn't used.
                    image_urls = [SITE_URL + image["src"] for image in move_images]

                move_data["images"] = image_urls
                move_data["character"] = chara_name

                moves.append(move_data)
                move_inputs.append(move_details[1].lower())

    return (moves, move_inputs)


def get_move_data(moves: list, move_inputs: list, move_input: string) -> dict:
    # Could be a better way to write this; use a dict with input as key and list as value
    move = {}
    if move_input in move_inputs:
        move = moves[move_inputs.index(move_input)]
    return move


def get_move_hitbox_image_url(move_images: list) -> string:
    # Returns the first hitbox image if it exists, otherwise return first normal image.
    for url in move_images:
        if "Hitbox" in url:
            return url
    return move_images[0]
