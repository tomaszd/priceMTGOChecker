import json

file_name = 'Results/Results_2018_July/result2018_July.txt'
with open(file_name) as json_file:
    json_data = json.load(json_file)
    # print(json_data)


def show_card(karta):
    if karta['komentarz'] is None:
        karta['komentarz'] = ''
    if 'cena' in karta:
        print "{0} {1} {2} {3}".format(karta['ilosc'],
                                       karta['nazwa'],
                                       karta['cena'],
                                       karta['komentarz'])
    else:
        print "{0} {1} {2} ".format(karta['ilosc'],
                                    karta['nazwa'],
                                    karta['komentarz'])


Total_Wartosc = 0
cards_with_problems = []
for karta in json_data:

    try:
        karta['cena'] = float(karta['cena'].replace('$', ''))
    except:
        cards_with_problems.append(karta)
        print karta

json_data_sorted_with_cena = [x for x in json_data if "cena" in x]

for karta in json_data_sorted_with_cena:
    karta["cena"] = float(karta["cena"].replace(",", "."))

for karta in json_data_sorted_with_cena:
    if karta["cena"] <= 0.5:
        karta["cena"] = 0.5
EURO = 4.30
for karta in json_data_sorted_with_cena:
    karta["cena"] = karta["cena"] * EURO
    Total_Wartosc += karta["cena"] * karta["ilosc"]

json_data_sorted = sorted(json_data_sorted_with_cena, key=lambda k: (-k['cena'], k['nazwa']))
print "GOTOWE DO WYSTAWIENIA"
for karta in json_data_sorted:
    show_card(karta)

print "Wartosc calkowita ", Total_Wartosc
# print "PROBLEMY!!!"
# for karta in cards_with_problems:
#    show_card(karta)
