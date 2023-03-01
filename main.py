import webbrowser
from html.parser import HTMLParser
import re
from os import listdir
from os.path import isfile, join

# Getting data from html file
class Parser(HTMLParser):
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        pass

    def handle_data(self, data: str) -> None:
        all_data.append(data)

def check_months(months, item):
    for month in months:
        if month[:2].lower() in item.lower():
            return True
    return False

all_data = []
parser = Parser()

html_files = [f for f in listdir('html_files') if isfile(join('html_files', f))]
for file in html_files:
    parser.feed(open('html_files/' + file).read())


# Creating lists of every exercise
new_list = []
list_completed = []
months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre',
         'décembre']


all_data = all_data[7:]
all_data = all_data[::-1]

count = 1
i = 0
while i < len(all_data):
    if count == 2 and check_months(months, all_data[i]) is False:
        all_data.insert(i, 'janvier')
    if count == 3 and all_data[i].split(' ')[0].isnumeric() is False:
        all_data.insert(i, '1900')
    if count == 4:
        count = 0
    count += 1
    i += 1

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
subject = input("What subject are you searching for? : ")
for exercise in list_completed:
    if subject.lower() in exercise[0].lower():
        divide = re.split('(\d+)', exercise[3])
        webbrowser.open(
            f"https://studentacademy.be/examen-entree/polytech/anciens-examens/#/ex-page/{divide[0]}/{divide[1]}")
