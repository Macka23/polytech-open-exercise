import webbrowser
from html.parser import HTMLParser
import re
from os import listdir
from os.path import isfile, join


# Getting data from html file
class Parser(HTMLParser):
    def handle_data(self, data: str) -> None:
        all_data.append(data)


def check_months(one12, item):
    for month in one12:
        if month[:2].lower() in item.lower():
            return True
    return False


all_data = []
parser = Parser()

html_files = [f for f in listdir('html_files') if isfile(join('html_files', f))]
for file in html_files:
   parser.feed(open('html_files/' + file).read())

# Creating lists of every exercise, with all of html files data in all_data variable, a pattern is used to get a list of
# all exercises classified : ['subject', 'month', 'year', 'EXAL???'].
new_list = []
list_completed = []
months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre',
          'décembre']

all_data = all_data[7:]
all_data = all_data[::-1]

# Filling all missing data (often month and year which are replaced by 'janvier' for the month and '1900' for the year)
count = 1
i = 0
while i < len(all_data):
    if count == 2 and check_months(months, all_data[i]) is False:
        all_data.insert(i, 'janvier')
    if count == 3 and all_data[i][:3].isnumeric() is False:
        all_data.insert(i, '1900')
    if count == 4:
        count = 0
    count += 1
    i += 1

# Creating this pattern I talked above (['subject', 'month', 'year', 'EXAL???'], [...], [...])
count = 0
for data in all_data:
    if count < 4:
        new_list.append(data)
        count += 1
    if count == 4:
        list_completed.append(new_list)
        new_list = []
        count = 0

# Asking for subject wanted and opening each exercise
running = 1
subject = "NEVER_GOING_TO_BE_IN_A_STRING_GGWP"
while running:
    if running == 1:
        subject = input("What subject are you searching for? (Press enter if you want to exit the script) : ")
    if running > 1:
        subject = input("Something else? (Press enter if you want to exit the script) : ")
    if subject == "":
        break
    for exercise in list_completed:
        if subject.lower() in exercise[0].lower():
            divide = re.split('(\d+)', exercise[3])
            webbrowser.open(
                f"https://studentacademy.be/examen-entree/polytech/anciens-examens/#/ex-page/{divide[0]}/{divide[1]}")
            print(f"https://studentacademy.be/examen-entree/polytech/anciens-examens/#/ex-page/{divide[0]}/{divide[1]}")
    running += 1
