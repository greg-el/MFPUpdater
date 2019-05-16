import requests
import bs4
import getpass
import datetime

MFP_LOGIN = "https://www.myfitnesspal.com/account/login"
MFP_GET_CALORIES = "https://www.myfitnesspal.com/food/diary/"
MFP_GET_WEIGHT = "https://www.myfitnesspal.com/measurements/edit?page=1"

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
        session.post(MFP_LOGIN, data=payload)
        r = session.get(MFP_GET_CALORIES)
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        total_row = soup.find("tr", class_="total")
        today_calories = total_row.contents[3]
        return today_calories.getText()

def getWeight():
    with requests.Session() as session:
        session.post(MFP_LOGIN, data=payload)
        pages = session.get(MFP_GET_WEIGHT.format(1))
        soup = bs4.BeautifulSoup(pages.text, "html.parser")
        last_group = soup.find_all("p", class_="cont-2")
        for last in last_group:
            try:
                test = last.find("input", class_="text very_short")["value"]
                return test
            except TypeError:
                continue


def getWeightFromDate(date=TODAY):
    with requests.Session() as session:
        session.post(MFP_LOGIN, data=payload)
        output = []
        pages = session.get(MFP_GET_WEIGHT.format(1))
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
            r = session.get(MFP_GET_WEIGHT.format(i))
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