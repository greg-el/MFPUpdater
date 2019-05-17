import requests
import bs4
import getpass
import datetime
import re

LOGIN = "https://www.myfitnesspal.com/account/login"
GET_CALORIES = "https://www.myfitnesspal.com/food/diary/"
GET_WEIGHT_DATE = "https://www.myfitnesspal.com/measurements/edit?page=1"
GET_WEIGHT = "https://www.myfitnesspal.com/measurements/check_in"

now = datetime.datetime.now()
TODAY = now.strftime("%m/%-d/%Y").lstrip("0").replace(" 0", " ")

username = input("Username: ")
password = getpass.getpass('Password:')
payload = {
    'username': username,
    'password': password
}

def getCalories():
    with requests.Session() as session:
        session.post(LOGIN, data=payload)
        r = session.get(GET_CALORIES)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        total_row = soup.find("tr", class_="total")
        today_calories = total_row.contents[3]
        return today_calories.getText()

def getWeight():
    with requests.Session() as session:
        session.post(LOGIN, data=payload)
        pages = session.get(GET_WEIGHT.format(1))
        soup = bs4.BeautifulSoup(pages.text, "html.parser")
        last_group = soup.find_all("p", class_="cont-2")
        for last in last_group:
            x = re.findall(("\\d\\d\\.\\d"), str(last))
            return x[0]


def getWeightFromDate(date=TODAY):
    with requests.Session() as session:
        session.post(LOGIN, data=payload)
        output = []
        pages = session.get(GET_WEIGHT_DATE.format(1))
        soup = bs4.BeautifulSoup(pages.text, "html.parser")
        paginator = soup.find_all("div", class_="pagination alt")
        pages = []
        temp_list = []
        for page in paginator:
            text = page.getText().split()
            for item in text:
                if item.isdigit():
                    pages.append(int(item))

        for i in range(1, max(pages)+1):
            r = session.get(GET_WEIGHT_DATE.format(i))
            soup = bs4.BeautifulSoup(r.text, "html.parser")
            table = soup.find_all("td", class_="col-num")
            for entry in table:
                text = entry.getText()
                if text == "Date" or text == "Amount" or text == "Delete?":
                    continue
                if len(temp_list) == 2:
                    output.append(temp_list.copy())
                    temp_list.clear()
                temp_list.append(text)
    for data in output:
        if data[0] == date:
            return data[1]