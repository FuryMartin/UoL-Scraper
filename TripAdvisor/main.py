import requests
import bs4
import json

class review:
    def __init__(self, data):
        self.data = data
        self.reviewer_name = self.data.find('div',attrs={'class':'info_text pointer_cursor'}).find('div').text
        self.reviewer_badge = self.data.find('span', attrs={'class':'badgeText'}).text
        self.grades = self.data.find('div',attrs={'class':'ui_column is-9'}).find_all('span')[0]['class'][1][-2] #取class倒数第二个字符
        self.title = self.data.find('span',attrs={'class':'noQuotes'}).text
        self.comment = self.data.find('p',attrs={'class':'partial_entry'}).text
        self.rating_date = self.data.find('span',attrs={'class':'ratingDate'})['title']
        self.visit_date = self.data.find('div',attrs={'class':'prw_rup prw_reviews_stay_date_hsx'}).text[15:] #取15位之后的字符
        self.likes = self.data.find('span',attrs={'class':'numHelp'}).text
        
        #点赞为空时置零
        if self.likes == "":
            self.likes = "0"

        #检查是否via_mobiles
        try:
            self.data.find('span',attrs={'class':'viaMobile'}).text
            self.via_mobiles = "True"
        except AttributeError:
            self.via_mobiles = "False"

        self.dict = {'ReviewerName': self.reviewer_name, 'ReviewerBadge': self.reviewer_badge, 'Grades': self.grades, 'RatingDate': self.rating_date,
                     'VisitDate': self.visit_date, 'Likes': self.likes, 'ViaMobiles': self.via_mobiles, 'Title': self.title, 'Comment': self.comment}
        
def fetch_urls(url):
    headers = {
        'authority': 'www.tripadvisor.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
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
    en_data_count = bsobj.find('div', attrs={'class':'item','data-value':'en'}).find('span', attrs={'class':'count'}).text
    en_data_count = int(en_data_count[1:-1].replace(',', ''))

    page_count = int(en_data_count / 15)
    page_list = []
    url_prefix = url[:url.find('Reviews')+8] + 'or'
    url_suffix = '-' + url[url.find('Reviews')+8:]
    page_list.append(url)
    for num in range(1, page_count + 1):
        sub_url = url_prefix + str(num*15) + url_suffix
        page_list.append(sub_url)
    return page_list

def fetch_review(url):
    headers = {
        'authority': 'www.tripadvisor.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Microsoft Edge";v="100"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
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
    reviews = bsobj.find_all('div', attrs={'class':'rev_wrap ui_columns is-multiline'})
    results = []
    for signle_review in reviews:
        results.append(review(signle_review).dict)
    return results

def scraper(url):
    results = []
    try:
        pages = fetch_urls(url)
    except requests.ConnectTimeout:
        pages = fetch_urls(url)
    failed_pages = []
    for page in pages:
        print(page)
        try:
            review_list = fetch_review(page)
            results.extend(review_list)
        except requests.ConnectTimeout:
            print("Timeout: " + page)
            failed_pages.append(page)
    if len(failed_pages) > 0:
        for page in failed_pages:
            print(page)
            try:
                review_list = fetch_review(page)
                results.extend(review_list)
            except requests.ConnectTimeout:
                print("Timeout: " + page)
    #results = fetch_review()
    restaurant_name = url[url[:url.rfind("-", 1)].rfind("-")+1: url.rfind("-", 1)]
    with open(restaurant_name + '.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(results, indent=4, ensure_ascii=False))
    print(len(results))


if __name__ == '__main__':
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d1421189-Reviews-London_Steakhouse_Co-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d14134252-Reviews-Scarlett_Green-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d21302648-Reviews-Hibox-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d13082910-Reviews-Devine_Restaurant_Coffee_Bar-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d19982460-Reviews-Nora_Cafe-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d10822007-Reviews-MBER-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d5122082-Reviews-Alexander_The_Great-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d783897-Reviews-Indian_Room-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d5856902-Reviews-Bayleaf_Restaurant-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d10440481-Reviews-Andy_s_Greek_Taverna-London_England.html'
    #url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d13544747-Reviews-Amrutha_Lounge-London_England.html'
    url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d813149-Reviews-Taste_Of_Nawab-London_England.html'
    scraper(url)
