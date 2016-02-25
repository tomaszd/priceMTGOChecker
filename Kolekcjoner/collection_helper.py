import urllib
import openpyxl
import json
import datetime
##########
#This file is for methods / class for counting amount of monet for collection


#load collection xlsx
def convert_xlsx2dict(input_file):
  wb = openpyxl.load_workbook(input_file)
  sheet = wb.get_sheet_by_name('Sheet1')
  # transfom sheet ->dict
  cards_dict=[]
  for i in range(1,len(sheet.rows)):
    cards_dict.append(
                  {
                  'nazwa':sheet.rows[i][0].value,     
                  'ilosc':int(sheet.rows[i][1].value),   
                  'kolor':sheet.rows[i][2].value,    
                  'komentarz':sheet.rows[i][3].value
                   }      
                 )
    #if i ==2:
    #  break
    #  import pdb
    #  pdb.set_trace()
  return cards_dict

def getCFBPrice(cardName, cardSet=None):
  #tutaj czasem folie zabiera bo sa na gorze
  cfbURL = "http://store.channelfireball.com/products/search?q=" + urllib.quote(cardName)
  # tu sa filtered by price
  #cfbURL='http://store.channelfireball.com/products/search?query='+ urllib.quote(cardName)
  #if cardSet:
  #  cfbURL += " " + urllib.quote(cardSet)
  htmlFile = urllib.urlopen(cfbURL)
  rawHTML = htmlFile.read()
  tempIndex = rawHTML.find("grid-item-price")
  startPriceIndex = rawHTML.find("$", tempIndex)
  endPriceIndex = rawHTML.find("<", startPriceIndex)
  cfbPrice = rawHTML[startPriceIndex:endPriceIndex]
  print "{0}: {1}".format(cardName,cfbPrice)
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
  import pdb
  pdb.set_trace()
  
  return [lowPrice, midPrice, highPrice]



if __name__ == "__main__":
  print 'dupa'
  input_file='Luty2016.xlsx'
  moje_karty=convert_xlsx2dict(input_file)
  bledy=[]
  suma=0
  lazy_loading_dict={}
  for karta in moje_karty:
    try:
      if karta['nazwa'] in lazy_loading_dict.keys():
        price=lazy_loading_dict[karta['nazwa']]
        print "Already price was taken for {} it is {}".format(karta['nazwa'],price)
      else:  
        price=getCFBPrice(karta['nazwa'])
      karta['cena']=price
      lazy_loading_dict[karta['nazwa']]=price
      suma+=karta['ilosc']*float(price.replace('$',''))
    except:
      bledy.append(karta)
     #karta['cenaTCG']=getTCGPlayerPrices(karta['nazwa'])

  timestamp=datetime.datetime.now().strftime("%Y_%B_%d._%I:%M%p")
  with open('result'+timestamp+'.txt', 'w') as outfile:
    json.dump(moje_karty, outfile)  
  with open('bledy'+timestamp+'.txt', 'w') as outfile2:
    json.dump(bledy, outfile2) 
  with open('suma'+timestamp+'.txt', 'w') as outfile2:
    json.dump(suma, outfile2)   