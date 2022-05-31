import string
from typing import Tuple
from bs4 import BeautifulSoup
import requests


# move_search = input("what move: ").upper()
# if move_search in move_inputs:
#     print(moves[move_inputs.index(move_search)])
# else:
#     print("no move found!")


def get_character_framedata(chara_name: string) -> Tuple:
    # Returns tuple with two lists containing data for each move and move inputs for indexing.

    URL = "http://dustloop.com/wiki/index.php?title=GGACR/{}/Frame_Data".format(chara_name)
    page = requests.get(URL)
    if page.status_code == 404:
        print("404 character page not found")
        return (None, None)

    else:
        soup = BeautifulSoup(page.content, "html.parser")
        fd_tables = soup.find_all("table", class_="display")
        moves = []  # all the moves for that character
        move_inputs = []  # name index will match the dict index
        for table in fd_tables:
            # Get header values for dict keys.
            table_header = table.find("tr")
            header_data = [col.text for col in table_header.find_all("th")]
            
            # Create dict for each move
            table_body = table.find("tbody").find_all("tr")
            for move_row in table_body:
                move_details = [col.text for col in move_row.find_all("td")]
                move_data = dict(zip(header_data, move_details))
                moves.append(move_data)
                move_inputs.append(move_details[1])
        return (moves, move_inputs)


name = input("what character (exact wording): ")
moves, move_inputs = get_character_framedata(name)
print(move_inputs)
