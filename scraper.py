import string
from typing import Tuple
from bs4 import BeautifulSoup
import requests


def get_character_framedata(chara_name: string) -> Tuple:
    # Primary function that webscrapes dustloop frame data tables.
    # Returns tuple with two lists containing data for each move and move inputs for indexing.
    moves = []  # Contains dicts that represents a move column.
    move_inputs = []

    URL = "http://dustloop.com/wiki/index.php?title=GGACR/{}/Frame_Data".format(chara_name)
    page = requests.get(URL)
    if page.status_code == 404:
        print("Error: 404 character page not found!")

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
                image_urls = [image["src"] for image in move_images]
                move_data["images"] = image_urls

                moves.append(move_data)
                move_inputs.append(move_details[1].upper())

    return (moves, move_inputs)


def get_move_data(moves: list, move_inputs: list, move_input: string) -> dict:
    move = {}
    if move_input in move_inputs:
        move = moves[move_inputs.index(move_input)]
    else:
        print("Error: Move not found!")

    return move


#testing

# name = input("what character (exact wording): ")
# moves, move_inputs = get_character_framedata(name)
# print(move_inputs)

# if moves != []:
#     input = input("what move: ").upper()
#     move = get_move_data(moves, move_inputs, input)
#     print("Input: {}, Startup: {}, Active: {}, Recovery: {}".
#     format(move["input"], move["startup"], move["active"], move["recovery"]))
#     print(move["images"])
