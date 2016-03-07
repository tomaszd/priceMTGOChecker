'''
Created on 24 lut 2016

@author: opera
'''
from BeautifulSoup import BeautifulSoup
import requests


def get_singles_details_from_magic_card_market( cardname=None ):
  url = "http://www.magiccardmarket.eu/?mainPage=showSearchResult&searchFor="
  if not cardname:
    print "no card specified"
    return []

  full_url = url + cardname
  data = requests.get( full_url )
  soup = BeautifulSoup( data.text )
  list_of_cards = []
  # [1:-1] cause first element is column legend names
  # and the last is empty
  base_url = "https://www.magiccardmarket.eu"
  for row in range( len( soup.findAll( 'tr' ) ) )[1:-1]:
    card_details = {}

    thumb, expan, rarity, href, comment, singles, avail, price = soup.findAll( 'tr' )[row].findAll( 'td' )
    thumb = str( thumb ).replace( '<td>', '' ).replace( '</td>', '' )
    expan = str( expan ).replace( '<td>', '' ).replace( '</td>', '' )
    href = str( href ).replace( '<td>', '' ).replace( '</td>', '' )
    comment = str( comment ).replace( '<td>', '' ).replace( '</td>', '' )
    singles = str( singles ).replace( '<td>', '' ).replace( '</td>', '' )
    avail = str( avail ).replace( '<td>', '' ).replace( '</td>', '' )
    price = str( price ).replace( '<td>', '' ).replace( '</td>', '' ).replace( '&#x20AC;', 'EURO' )
    is_card_single = 'Products/Singles/' in href
    if is_card_single:
      expansion_set = href.split( 'Singles/' )[1].split( '/' )[0]
    else:
      print "This is not a single card skipping"
      continue
    if expansion_set in ["Alpha", "Beta", "Unlimited"]:
      print "Expansion set is {} .skipping then ...for {}".format( expansion_set,
                                                                  cardname )
      continue
    # print "thumb", thumb
    # print "expan", expan
    # print "rarity", rarity
    print "href", href
    if comment:
      print "comment", comment
    # print "singles", singles
    # print "avail", avail
    print "expansion_set", expansion_set
    print "price", price

    card_details = {
                  # "thumb":thumb,
                  # "expan": expan,
                  # "rarity": rarity,
                  "href":   base_url + href.split( "\"" )[1],
                  "comment": comment,
                  "singles": singles,
                  "avail": avail,
                  "expansion_set":expansion_set,
                  "price": price}

    list_of_cards.append( card_details )
  return list_of_cards

def get_best_expansion_set_to_get_price_from( list_of_cards ):
    """This is getting dict from"""
    for single_detail in list_of_cards:
      print single_detail['expansion_set'] , " : ", single_detail['price']
    newlist_sorted_by_price = sorted( list_of_cards, key=lambda k: k['price'] )
    print "Sorted:"
    for single_detail in newlist_sorted_by_price:
      print single_detail['expansion_set'] , " : ", single_detail['price']
    lowest_price_single = newlist_sorted_by_price[0]
    print "Lowest price :"
    print   lowest_price_single
    return lowest_price_single

def get_price_trend_for_single_card( lowest_price_single ):
  """get price tend form sites like : 
   https://www.magiccardmarket.eu/Products/Singles/Future+Sight/Tarmogoyf"""
  base_url = "https://www.magiccardmarket.eu"
  # 'href': '<a href="/Products/Singles/Magic+2012/Manabarbs">Manabarbs</a>' -> /Products/Singles/Magic+2012/Manabarbs
  url_for_single = lowest_price_single["href"]
  final_single_url = base_url + url_for_single
  print "final_single_url", final_single_url
  data_for_single = requests.get( final_single_url )
  soup = BeautifulSoup( data_for_single.text )

  # get table with details
  availTable = soup.findAll( "table", {"class":"availTable"} )[0]
  price_trend = None
  for row in availTable.findAll( "tr" ):
    if "Price Trend" in row.text:

      # print "Znalalzlem",row.text
      price_trend = row.text.split( "Price Trend:" )[1].replace( '&#x20AC;', 'EURO' )
      break
  lowest_price_single['price_trend'] = price_trend
  return  lowest_price_single

def _get_price_and_exp_from_magic_card_Market( cardname ):
  lowest_price_single = get_best_expansion_set_to_get_price_from( get_singles_details_from_magic_card_market( cardname ) )
  lowest_price_single = get_price_trend_for_single_card( lowest_price_single )
  return lowest_price_single




if __name__ == "__main__":\
  print _get_price_and_exp_from_magic_card_Market( "manabarbs" )


