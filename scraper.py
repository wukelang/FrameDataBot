from bs4 import BeautifulSoup
import requests


URL = "http://dustloop.com/wiki/index.php?title=GGACR/Ky_Kiske/Frame_Data"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
fd_tables = soup.find_all("table", class_="display")




moves = []  # all the moves for that character
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



for move in moves:
    print(move["input"], move["startup"])
