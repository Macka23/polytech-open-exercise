import webbrowser
from html.parser import HTMLParser
import re


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
parser.feed(open('all_html_content.html').read())

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

# Adjusting list
all_subject = []
for i in list_completed:
    i[0] = i[0].replace('Ã©', 'é')
    i[0] = i[0].replace('Ã¨', 'è')
    i[0] = i[0].replace('Ã´', 'ô')
    if "primi" in i[0]:
        i[0] = "Intégrale"
    if "septembre" in i[0]:
        i[0] = "limites"
    if i[0] in "Année" or i[0] in "Sujet":
        list_completed.pop(list_completed.index(i))

# Help list created if user cannot find exercise
help_list = {'Aire et volume', 'Angles', 'Binôme de newton', 'Calcul numérique', 'Cylcométriques', 'Cône', 'Divers',
             'Domaine', 'Dérivée', 'Déterminant', 'Equation', 'Etude de fonction',
             'Expression', 'Fonction inverse', 'Hexagone', 'Identité', 'Intégrale', 'Inéquation',
             'Lieu géométrique', 'Limites', 'Logarithmes et exponentielles', 'Matrices', 'Nombre complexe',
             'Optimisation', 'Polygone', 'Polynôme', 'Primitive', 'Problème', 'Relation', 'Second degré',
             'Session', 'Sphère', 'Suites', 'Surface et volume', 'Système paramétrique', 'Théorème', 'Trapèze',
             'Vrai/faux'}

# Asking for subject wanted and opening each exercise
running = 1
subject = "NEVER_GOING_TO_BE_IN_A_STRING_GGWP"
while running:
    if running == 1:
        subject = input(
            "What subject are you searching for? (For help: write '--help'. Press enter if you want to exit the "
            "script) : ")
    if running > 1:
        subject = input("Something else? (For help; write '--help'. Press enter if you want to exit the script) : ")
    if subject == "":
        break
    if subject == "--help":
        print("Here are all subjects fetched from studentacademy.be")
        for help in sorted(help_list):
            print(help)
    for exercise in list_completed:
        if subject.lower() in exercise[0].lower():
            divide = re.split('(\d+)', exercise[3])
            link = ""
            try:
                link = f"https://studentacademy.be/examen-entree/polytech/anciens-examens/#/ex-page/" \
                       f"{divide[0]}/{divide[1]}"
                webbrowser.open(link)
            except:
                print("Couldn't find any exercise.")
                break
            if len(link) > 84:
                print(f"{link}       {exercise[0]}")
            else:
                print(f"{link}        {exercise[0]}")
    running += 1
