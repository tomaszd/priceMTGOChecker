'''
Created on 24 lut 2016

@author: opera
'''
from BeautifulSoup import BeautifulSoup
import requests


def get_singles_details_MCM(cardname=None):
    url = "http://www.magiccardmarket.eu/?mainPage=showSearchResult&searchFor="
    if not cardname:
        print "no card specified"
        return []

    full_url = url + cardname
    try:
        data = requests.get(full_url)
        soup = BeautifulSoup(data.text)
    except:
        print "problems for {}".format(full_url)
        return []
    list_of_cards = []
    # [1:-1] cause first element is column legend names
    # and the last is empty
    base_url = "https://www.magiccardmarket.eu"
    for row in range(len(soup.findAll('tr')))[1:-1]:
        card_details = {}
        # print "checking ",full_url
        try:
            thumb, expan, rarity, href, comment, singles, avail, price = soup.findAll(
                'tr')[row].findAll('td')
        except:
            print "just one occurence for {}".format(full_url)
            card_details = {

                "href": full_url,
                "comment": "1 occurence",
                "singles": False,
                "avail": False,
                "expansion_set": "strange",
                "price": "strange"}
            print "dupa2"
            return [card_details]
        if price.text == "N/A":
            print "Warning! N/A for price {} .{}".format(price, href)
            continue
        if "Playmat" in str(href):
            print "Warning! This is Playmat , Skipping...", href
            continue
        if "Promo" in str(href):
            print "Warning! This is PROMO price , Skipping...", href
            continue

        thumb = str(thumb).replace('<td>', '').replace('</td>', '')
        expan = str(expan).replace('<td>', '').replace('</td>', '')
        href = str(href).replace('<td>', '').replace('</td>', '')
        comment = str(comment).replace('<td>', '').replace('</td>', '')
        singles = str(singles).replace('<td>', '').replace('</td>', '')
        avail = str(avail).replace('<td>', '').replace('</td>', '')
        price = str(price).replace('<td>', '').replace(
            '</td>', '').replace('&#x20AC;', 'EURO')
        is_card_single = 'Products/Singles/' in href
        if is_card_single:
            expansion_set = href.split('Singles/')[1].split('/')[0]
        else:

            continue
        if expansion_set in ["Alpha", "Beta", "Unlimited"]:
            print "Expansion set is {} .skipping then ...for {}".format(expansion_set,
                                                                        cardname)
            continue
        if "WCD" in expansion_set:
            print "Expansion set is {} .skipping then ...HIS gold bordered {}".format(expansion_set,
                                                                                      cardname)
            continue
        # print "thumb", thumb
        # print "expan", expan
        # print "rarity", rarity
        if comment:
            print "comment", comment
            # print "singles", singles
            # print "avail", avail
        #    print "expansion_set", expansion_set
        #    print "price", price

        card_details = {
            # "thumb":thumb,
            # "expan": expan,
            # "rarity": rarity,
            "href": base_url + href.split("\"")[1],
            "comment": comment,
            "singles": singles,
            "avail": avail,
            "expansion_set": expansion_set,
            "price": price}

        list_of_cards.append(card_details)
    if list_of_cards == []:
        print "Nie ma!"
    return list_of_cards


def get_best_expansion(list_of_cards):
    """This is getting lowest price dict. the cheapest expansion set"""
    #   for single_detail in list_of_cards:
    #     print single_detail['expansion_set'] , " : ", single_detail['price']
    newlist_sorted_by_price = sorted(list_of_cards,
                                     key=lambda k: float(k['price'].
                                                         replace(",", ".").replace("EURO", "")))
    #    for single_detail in newlist_sorted_by_price:
    #      print single_detail['expansion_set'] , " : ", single_detail['price']
    lowest_price_single = newlist_sorted_by_price[0]
    return lowest_price_single


def get_price_trend(lowest_price_single):
    """get price tend form sites like :
     https://www.magiccardmarket.eu/Products/Singles/Future+Sight/Tarmogoyf"""
    # 'href': '<a href="/Products/Singles/Magic+2012/Manabarbs">Manabarbs</a>' -> /Products/Singles/Magic+2012/Manabarbs
    url_for_single = lowest_price_single["href"]
    final_single_url = url_for_single
    price_trend = 0
    try:
        data_for_single = requests.get(final_single_url)
        soup = BeautifulSoup(data_for_single.text)
        # get table with details
        availTable = soup.findAll("table", {"class": "availTable"})[0]
        for row in availTable.findAll("tr"):
            if "Price Trend" in row.text:
                # print "Znalalzlem",row.text
                price_trend = row.text.split("Price Trend:")[
                    1].replace('&#x20AC;', 'EURO')
                break
    except:
        print "problems for {}".format(final_single_url)
    lowest_price_single['price_trend'] = price_trend
    return lowest_price_single


def get_price_and_set_MagicCardMarket(cardname):
    """ function return dict with all details about card in form:

    {'comment': '',
     'singles': 'Singles',
     price_trend': u'113,50 EURO'
     'price': '0,02 EURO',
     'avail': '1379',
     'href': 'https://www.magiccardmarket.eu/Products/Singles/Magic+2012/Manabarbs',
     'expansion_set': 'Magic+2012'}
    """
    lowest_price_single = get_best_expansion(get_singles_details_MCM(cardname))
    lowest_price_single = get_price_trend(lowest_price_single)
    return lowest_price_single


if __name__ == "__main__": \
        # print get_price_and_set_MagicCardMarket("tarmogoyf")
    # print get_price_and_set_MagicCardMarket("doran, the siege tower")
    # print get_price_and_set_MagicCardMarket("flooded strand")
    print get_price_and_set_MagicCardMarket(" Fire-lit thicket")
