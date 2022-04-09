#WW websites
import requests
from bs4 import BeautifulSoup
import concurrent.futures
from random import choice

user_agentz = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Avast/70.0.917.102', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/538 (KHTML, like Gecko) Chrome/36 Safari/538', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2599.0 Safari/537.36']


def Check_link(ml, coin):
    link = ml + coin
    html = requests.get(link, headers={'user-agent': choice(user_agentz)})
    if html.status_code != 200:
        return 0
    return 1


def Check_lofcoin(arr):
    link = 'https://coinmarketcap.com/ru/currencies/'
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            res = [executor.submit(Check_link, link, cc) for cc in arr]
            for z in concurrent.futures.as_completed(res):
                if z.result() == 0:
                    return -1
        return 1
    except Exception as ex: print(repr(ex))
    
    
def get_stats(link, coin):
    try:
        coin_l = link + coin
        html = requests.get(coin_l, headers={'user-agent': choice(user_agentz)})
        soup = BeautifulSoup(html.text, 'html.parser')
        stats = soup.find(class_='sc-1q9q90x-0').text + '\n'
        price = soup.find(class_='priceValue').text
        diff = soup.find(class_='sc-15yy2pl-0')
        stats += '\n' + price
        if len(diff.find_all(class_='icon-Caret-up')) != 0:
            stats += '   +' + diff.text
        else:
            stats += '   -' + diff.text
        return stats
    except: return 0
    
    
def get_arr_stat(arr):
    link = 'https://coinmarketcap.com/currencies/'
    ans = "Stats of your coin list:   &#128185\n"
    try:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            res = [executor.submit(get_stats, link, cc) for cc in arr]
            for z in concurrent.futures.as_completed(res):
                if z.result() != 0:
                    ans += '\n---------------------------------\n' + z.result()
                else: return -1
        return ans
    except Exception as ex: print(repr(ex))
