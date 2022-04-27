import bs4
import requests
import re

def fetch_all_restaurant(url):
    headers = {
        'authority': 'www.tripadvisor.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'referer': 'https://www.tripadvisor.com/Restaurant_Review-g186338-d1421189-Reviews-London_Steakhouse_Co-London_England.html',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Mobile Safari/537.36 Edg/100.0.1185.50',
    }
    r = requests.get(url, headers=headers, timeout=5)
    r.encoding = 'utf-8'
    html = r.text
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    page_num = bsobj.find('div',attrs={'class':'hLLNS Gh'}).find('span',attrs={'class':'bupEh'})
    #.find('span').text
    if page_num % 30 != 0:
        page_num = page_num - page_num%30 + 30
    for i in range(1,page_num+1,30):
        print(i)
    """
    restaurants = bsobj.find_all('div',attrs={'class':'OhCyu'})
    urls = []
    for res in restaurants:
        url = 'www.tripadvisor.com/' + res.find('span').find('a')['href']
        urls.append(url)
    return urls
    """

def fetch_every_page(url):
    headers = {
        'authority': 'www.tripadvisor.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'referer': 'https://www.tripadvisor.com/Restaurants-g186338-London_England.html',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50',
        'x-requested-with': 'XMLHttpRequest',
    }
    r = requests.get(url, headers=headers,timeout=5)
    r.encoding = 'utf-8'
    html = r.text
    with open('temp.html','w',encoding='utf-8') as f:
        f.write(html)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    page_num = re.search(r'"listResultCount":\d+,',html).group(0)
    #print(page_num)
    page_num = re.search(r'\d+', page_num).group(0)
    #print(page_num)
    page_num = int(page_num)
    if page_num % 30 != 0:
        page_num = page_num - page_num%30 + 30
    failed_pages = []
    urls = []
    for i in range(30,page_num+1,30):
        try:
            params = {
                'Action': 'PAGE',
                'ajax': '1',
                'availSearchEnabled': 'true',
                'sortOrder': 'popularity',
                'geo': '186338',
                'itags': '10591',
                'eaterydate': '2022_04_26',
                'date': '2022-04-27',
                'time': '20:00:00',
                'people': '2',
                'o': 'a' + str(i),
            }
            r = requests.get('https://www.tripadvisor.com/RestaurantSearch', headers=headers,timeout=5,params=params)
            restaurants = bsobj.find_all('div',attrs={'class':'OhCyu'})
            for res in restaurants:
                url = 'www.tripadvisor.com/' + res.find('span').find('a')['href']
                print(url)
                urls.append(url)
        except requests.ConnectTimeout:
            failed_pages.append(i)

    while(len(failed_pages) > 0):
        for i in failed_pages:
            try:                
                r = requests.get('https://www.tripadvisor.com/RestaurantSearch', headers=headers,timeout=5,params={'o':'a'+str(i)})
                restaurants = bsobj.find_all('div',attrs={'class':'OhCyu'})
                for res in restaurants:
                    url = 'www.tripadvisor.com/' + res.find('span').find('a')['href']
                    print(url)
                    urls.append(url)
                failed_pages.remove(i)
            except requests.ConnectTimeout:
                continue
    return urls

if __name__ == '__main__':
    #result = fetch_all_restaurant('https://www.tripadvisor.com/Restaurants-g186338-London_England.html')
    result = fetch_every_page('https://www.tripadvisor.com/Restaurants-g186338-London_England.html')
    #for index,res in enumerate(result[:1000]):
    #    print(str(index)+ ":" + res )
    with open('restaurant.txt','w') as f:
        f.writelines(result)