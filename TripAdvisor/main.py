import requests
import bs4
import time

def fetch_info():
    T0 = time.time()
    url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d1421189-Reviews-London_Steakhouse_Co-London_England.html'

    headers = {
        'authority': 'www.tripadvisor.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Microsoft Edge";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    r = requests.get(url, headers=headers)
    T1 = time.time()
    #r.raise_for_status()
    r.encoding = 'utf-8'
    html = r.text
    T2 = time.time()
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    #data_count = bsobj.find('div',attrs={'class':'title_text'})
    en_data_count = bsobj.find('div', attrs={'class':'item','data-value':'en'}).find('span', attrs={'class':'count'})
    print(en_data_count.text)
    T3 = time.time()

    print()
    print(T1-T0)
    print(T2-T0)
    print(T3-T0)


if __name__ == '__main__':
    fetch_info()
