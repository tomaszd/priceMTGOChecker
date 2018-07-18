import json

file_name = 'Results/Results_2018_July/result2018_July.txt'
with open(file_name) as json_file:
    json_data = json.load(json_file)
    # print(json_data)


def show_card(karta):
    if karta['komentarz'] is None:
        karta['komentarz'] = ''
    print "{0} {1} {2} {3}".format(karta['ilosc'],
                                   karta['nazwa'],
                                   karta['cena'],
                                   karta['komentarz'])


cards_with_problems = []
for karta in json_data:

    try:
        karta['cena'] = float(karta['cena'].replace('$', ''))
    except:
        cards_with_problems.append(karta)
        print karta

json_data_sorted = sorted(json_data, key=lambda k: k['cena'])
for karta in json_data_sorted:
    show_card(karta)
