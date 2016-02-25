'''
Created on 24 lut 2016

@author: opera
'''
import requests
from BeautifulSoup import BeautifulSoup


def get_singles_details_from_magic_card_market(cardname=None):
  url = "http://www.magiccardmarket.eu/?mainPage=showSearchResult&searchFor="
  if not cardname:
    print "no card specified"
    return []
  
  full_url = url + cardname
  data = requests.get(full_url)
  soup = BeautifulSoup(data.text)
  list_of_cards=[]
  #[1:-1] cause first element is column legend names
  # and the last is empty
  for row in range(len(soup.findAll('tr')))[1:-1]:
    card_details = {}
  
    thumb, expan, rarity, href, comment, singles, avail, price = soup.findAll('tr')[row].findAll('td')
    #full_list=[thumb, expan, rarity, href, comment, singles, avail, price]
    #full_list=[str(var).replace('<td>','').replace('</td>','') for var in full_list]
    thumb=str(thumb).replace('<td>','').replace('</td>','')
    expan=str(expan).replace('<td>','').replace('</td>','')
    href=str(href).replace('<td>','').replace('</td>','')
    comment=str(comment).replace('<td>','').replace('</td>','')
    singles=str(singles).replace('<td>','').replace('</td>','')
    avail=str(avail).replace('<td>','').replace('</td>','')
    price=str(price).replace('<td>','').replace('</td>','').replace('&#x20AC;','EURO')
    is_card_single='Products/Singles/' in href
    if is_card_single:
    
      expansion_set=href.split('Singles/')[1].split('/')[0]
    else:
      print "This is not a single card skipping"
      continue
    
    print "thumb", thumb
    print "expan", expan
    print "rarity", rarity
    print "href", href
    print "comment", comment
    print "singles", singles
    print "avail", avail
    print "expansion_set",expansion_set
    print "price", price
  
    card_details={"thumb":thumb,
                  "expan": expan,
                  "rarity": rarity,
                  "href": href,
                  "comment": comment,
                  "singles": singles,
                  "avail": avail,
                  "expansion_set":expansion_set,
                  "price": price}
  
    list_of_cards.append(card_details)
    return list_of_cards
  
if __name__=="__main__":
  get_singles_details_from_magic_card_market("Tarmogoyf")
  
