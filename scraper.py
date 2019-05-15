import requests
import bs4
import getpass

MFP_LOGIN = "https://www.myfitnesspal.com/account/login"
MFP_GET = "https://www.myfitnesspal.com/food/diary/"

def get_Calories():
    username = input("Username: ")
    password = getpass.getpass('Password:')
    payload = {
        'username': username,
        'password': password
    }

    with requests.Session() as session:
        session.post(MFP_LOGIN, data=payload)
        r = session.get(MFP_GET)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        total_row = soup.find("tr", class_="total")
        today_calories = total_row.contents[3]
        return today_calories.getText()


