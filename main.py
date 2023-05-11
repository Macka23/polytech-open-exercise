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


def open_normal_mode(count):
    divide = re.split('(\d+)', exercise[3])
    link = ""

    try:
        link = f"https://studentacademy.be/examen-entree/polytech/anciens-examens/#/ex-page/" \
               f"{divide[0]}/{divide[1]}"
        if open_window_mode % 2 != 0:
            webbrowser.open(link)
        count += 1
    except:
        print("Couldn't find that exercise.")

    blank = 40 - len(exercise[0])
    white = ""
    for space in range(blank):
        white += " "
    if len(link) > 84:
        print(f"{link}       {exercise[0]} {white} {exercise[2]}")
    else:
        print(f"{link}        {exercise[0]} {white} {exercise[2]}")

    return count


def date_input_entries():
    date = ""
    subject = []
    total_entry = input(
        "What subject are you searching and when was it? (Press Enter to exit. Change open mode; --change. '--help-commands'): ").split(" ")
    for entry in total_entry:
        if entry.isnumeric():
            date += entry

        else:
            subject.append(entry)

    return date, " ".join(subject)


def num_there(s):
    return any(i.isdigit() for i in s)


def change_date(list_completed) -> list:
    for exercise in list_completed:
        final_string = []
        correct_date = ""
        inter_string = ""

        if num_there(exercise[2]):
            for i in exercise[2]:
                if i.isnumeric():
                    inter_string += i

            count = 0
            for i in inter_string:
                correct_date += i
                count += 1
                if count % 4 == 0:
                    final_string.append(correct_date)
                    correct_date = ""
                    count = 0

            final_string = list(set(final_string))
            final_string = '-'.join(sorted(final_string, key=int))
            exercise[2] = str(final_string)

        else:
            exercise[2] = "xxxx"
            if exercise[0] != "Session" and exercise[0] != "NumÃ©ro":
                index = list_completed.index(exercise)
                prob_date = "xxxx"
                count = 0
                date_before = 0
                while "xxxx" in prob_date:
                    count += 1
                    if num_there(list_completed[index - count][2]) and list_completed[index - count][0] != "Session" and \
                            list_completed[index - count][0] != "NumÃ©ro":
                        date_before = int((list_completed[index - count][2])[:4])


                    elif num_there(list_completed[index + count][2]):
                        date_before = int((list_completed[index + count][2])[:4])

                    prob_date = f"{str(date_before)}-{date_before + 1}"
                exercise[2] = prob_date + "  Probably this date"

    return list_completed


all_data = []
parser = Parser()
parser.feed(open('all_html_content.html').read())

# Creating lists of every exercise, with all of html files data in all_data variable, a pattern is used to get a list of
# all exercises classified : ['subject', 'month', 'year', 'EXAL???'].
new_list = []
list_completed = []
months = ['No month', 'janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
          'novembre',
          'décembre']

all_data = all_data[7:]
all_data = all_data[::-1]

# Filling all missing data (often month and year which are replaced by 'janvier' for the month and '1900' for the year)
count = 1
i = 0
while i < len(all_data):
    if count == 2 and check_months(months, all_data[i]) is False:
        all_data.insert(i, 'No month')
    if count == 3 and all_data[i] != "No year" and all_data[i][:3].isnumeric() is False:
        all_data.insert(i, 'No year')
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

list_completed.pop(0)

# Help list created if user cannot find exercise
help_list = {'Aire et volume', 'Angles', 'Binôme de newton', 'Calcul numérique', 'Cylcométriques', 'Cône', 'Divers',
             'Domaine', 'Dérivée', 'Déterminant', 'Droites et plan', 'Equation', 'Etude de fonction',
             'Expression', 'Fonction inverse', 'Hexagone', 'Identité', 'Intégrale', 'Inéquation',
             'Lieu géométrique', 'Limites', 'Logarithmes et exponentielles', 'Matrices', 'Nombre complexe',
             'Optimisation', 'Polygone', 'Polynôme', 'Primitive', 'Problème', 'Relation', 'Second degré',
             'Session', 'Sphère', 'Suites', 'Surface et volume', 'Système paramétrique', 'Théorème', 'Trapèze',
             'Vrai/faux'}

list_completed = change_date(list_completed)
# Asking for subject wanted and opening each exercise
running = 1
open_window_mode = 1
subject = "NEVER_GOING_TO_BE_IN_A_STRING_GGWP"
date = "gurney"
while running:
    date, subject = date_input_entries()

    if subject == "--help-commands":
        print("Here are all the commands created:\n"
              "'--change' : Navigator tabs won't open when you input your subject\n"
              "When you input something, write your subject and eventually a year within them a space, it'll search for every "
              "exercises released on that specific date. (ex.: inté 2005). If you don't input any year, it'll search for every exercises named the same way as your subject.")


    if subject == "--help":
        print("Here are all subjects fetched from studentacademy.be :")
        for help in sorted(help_list):
            print(help)

        print("When you input something, write your subject and eventually a year within them a space, it'll search for every"
              "exercises released on that specific date. (ex.: inté 2005). If you don't input any year, it'll search for every exercises named the same way as your subject.")


    if subject == "--change":
        open_window_mode += 1
        if open_window_mode % 2 == 0:
            print("Open mode disabled.")
        else:
            print("Open mode enabled.")

    if subject == "":
        break

    count = 0
    for exercise in list_completed:
        if subject.lower() in exercise[0].lower() and date == "":
            count = open_normal_mode(count)

        if subject.lower() in exercise[0].lower() and date in exercise[2]:
            count = open_normal_mode(count)


    if subject != "--change" and subject != "--help" and subject != "--help-commands":
        print(f"Found {count} exercises.")

