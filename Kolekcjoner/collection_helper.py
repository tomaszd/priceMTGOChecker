import datetime
import json
import openpyxl
import os
import urllib
import magic_card_market

##########
# This file is for methods / class for counting amount of monet for collection
# load collection xlsx
def convert_xlsx2dict(input_file):
  wb = openpyxl.load_workbook(input_file)
  sheet = wb.get_sheet_by_name('Sheet1')
  # transfom sheet ->dict
  cards_dict = []
  for i in range(1, len(sheet.rows)):
    cards_dict.append(
                  {
                  'nazwa':sheet.rows[i][0].value,
                  'ilosc':int(sheet.rows[i][1].value),
                  'kolor':sheet.rows[i][2].value,
                  'komentarz':sheet.rows[i][3].value
                   }
                 )

  return cards_dict

def getCFBPrice(cardName, cardSet=None):
  # tutaj czasem folie zabiera bo sa na gorze
  cfbURL = "http://store.channelfireball.com/products/search?q=" + urllib.quote(cardName)
  # tu sa filtered by price
  # cfbURL='http://store.channelfireball.com/products/search?query='+ urllib.quote(cardName)
  # if cardSet:
  #  cfbURL += " " + urllib.quote(cardSet)
  htmlFile = urllib.urlopen(cfbURL)
  rawHTML = htmlFile.read()
  tempIndex = rawHTML.find("grid-item-price")
  startPriceIndex = rawHTML.find("$", tempIndex)
  endPriceIndex = rawHTML.find("<", startPriceIndex)
  cfbPrice = rawHTML[startPriceIndex:endPriceIndex]
  print "{0}: {1}".format(cardName, cfbPrice)
  return cfbPrice

def getTCGPlayerPrices(cardName, cardSet=None):
  # Open the TCGPlayer URL
  tcgPlayerURL = "http://magic.tcgplayer.com/db/magic_single_card.asp?cn=" + urllib.quote(cardName)
  if cardSet:
    tcgPlayerURL += "&sn=" + urllib.quote(cardSet)
  htmlFile = urllib.urlopen(tcgPlayerURL)
  rawHTML = htmlFile.read()
  # Scrape for the low price
  tempIndex = rawHTML.find('>Low:')
  startLowIndex = rawHTML.find("$", tempIndex)
  endLowIndex = rawHTML.find("<", startLowIndex)
  lowPrice = rawHTML[startLowIndex:endLowIndex]
  # Scrape for the mid price
  tempIndex = rawHTML.find('>Median:')
  startMidIndex = rawHTML.find("$", tempIndex)
  endMidIndex = rawHTML.find("<", startMidIndex)
  midPrice = rawHTML[startMidIndex:endMidIndex]
  # Scrape for the high price
  tempIndex = rawHTML.find('>High:')
  startHighIndex = rawHTML.find("$", tempIndex)
  endHighIndex = rawHTML.find("<", startHighIndex)
  highPrice = rawHTML[startHighIndex:endHighIndex]
  print [lowPrice, midPrice, highPrice]
  # import pdb
  # pdb.set_trace()

  return [lowPrice, midPrice, highPrice]



if __name__ == "__main__":
  print 'dupa'
  # input_file = 'Luty2016.xlsx'
  input_file = 'Test2016.xlsx'
  my_cards = convert_xlsx2dict(input_file)
  bledy = []
  suma = 0
  lazy_loading_dict = {}
  for karta in my_cards:
    if karta['nazwa'] in lazy_loading_dict.keys():
      price = lazy_loading_dict[karta['nazwa']]
      print "Already price was taken for {} it is {}".format(karta['nazwa'], price)
    else:
      try:
        card_details = magic_card_market.get_price_and_set_MagicCardMarket(karta['nazwa'])
        price_trend = card_details["price_trend"].split(" ")[0]
        expansion_set = card_details['expansion_set']
        # .split( " " )[0] to remove " EURO"
        price = card_details['price'].split(" ")[0]
        karta['expansion_set'] = expansion_set
        karta['href'] = card_details["href"]
        # #Na razie price liczone z prcie trendu
        price = price_trend
        # price = getCFBPrice( karta['nazwa'] )
        """
        {'comment': '',
        'singles': 'Singles',
        price_trend': u'113,50 EURO'
        'price': '0,02 EURO',
        'avail': '1379',
        'href': 'https://www.magiccardmarket.eu/Products/Singles/Magic+2012/Manabarbs',
        'expansion_set': 'Magic+2012'}
        """
      except:
        print "issues for {}".format(karta)
        bledy.append(karta)


    karta['cena'] = price
    lazy_loading_dict[karta['nazwa']] = price
    suma += karta['ilosc'] * float(price.replace('$', '').replace(",", "."))
    print " after adding {} {} - worth total in EURO :  {} -> added {}".format(karta['ilosc'],
                                                                 price,
                                                                 suma,
                                                                 karta['nazwa'])
    """
    except:
      print "issues for {}".format(karta)
      bledy.append(karta)
      # karta['cenaTCG']=getTCGPlayerPrices(karta['nazwa'])
    """

  timestamp = datetime.datetime.now().strftime("%Y_%B")
  dir_with_result_path = "Results_" + str(timestamp)
  os.mkdir(dir_with_result_path)

  with open(os.path.join(dir_with_result_path,
                         'result' + timestamp + '.txt'), 'w') as outfile:
    json.dump(my_cards, outfile)
  with open(os.path.join(dir_with_result_path,
                         'bledy' + timestamp + '.txt'), 'w') as outfile2:
    json.dump(bledy, outfile2)
  with open(os.path.join(dir_with_result_path,
                         'suma' + timestamp + '.txt'), 'w') as outfile3:
    json.dump(suma, outfile3)
  print "Finito!!!!!"