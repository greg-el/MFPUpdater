from oauth2client.service_account import ServiceAccountCredentials
import pickle
import datetime
import gspread
import scraper

SCOPE = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
SPREADSHEET_ID = "1TkCv3vyPoUv3W3mxao-mwp1KIB4zbvdGY2WChF6THcY"
RANGE_NAME = "CALCULATIONS!B:K"

datetime_now = datetime.datetime.now()
WEEKDAY = datetime_now.strftime("%a.")
DATE_NUMBER = int(datetime_now.strftime("%d"))
DATE_REMAINDER = datetime_now.strftime("%b-%y")

week_begin = {
    "Tue." : 0,
    "Wed." : 1,
    "Thu." : 2,
    "Fri." : 3,
    "Sat." : 4,
    "Sun." : 5,
    "Mon." : 6
}


def main(): 
    credentials = ServiceAccountCredentials.from_json_keyfile_name('WillMFP-8f13a8c60090.json', SCOPE)
    gc = gspread.authorize(credentials)
    sh = gc.open_by_key(SPREADSHEET_ID)
    wks = sh.worksheet("CALCULATIONS")

    week_beginning_int = DATE_NUMBER - week_begin.get(WEEKDAY)
    week_beginning = str(week_beginning_int) + "-" + DATE_REMAINDER
    week_beginning_row = wks.find(week_beginning).row

    weekday_column = wks.find(WEEKDAY).col

    calories_row = week_beginning_row + 1

    wks.update_cell(week_beginning_row, weekday_column, "testweight")
    wks.update_cell(calories_row, weekday_column, calories)

if __name__ == '__main__':
    calories = scraper.get_Calories()
    main()