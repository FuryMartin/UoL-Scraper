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
    r.encoding = 'utf-8'
    html = r.text
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    reviews = bsobj.find_all('div', attrs={'class':'rev_wrap ui_columns is-multiline'})
    results = []
    for signle_review in reviews:
        results.append(review(signle_review).dict)
    return results

if __name__ == '__main__':
    results = []
    
    url = 'https://www.tripadvisor.com/Restaurant_Review-g186338-d1421189-Reviews-London_Steakhouse_Co-London_England.html'
    pages = fetch_urls(url)

    for page in pages[:100]:
        print(page)
        review_list = fetch_review(page)
        results.extend(review_list)
    #results = fetch_review()
    with open('output.json','w',encoding='utf-8') as f:
        f.write(json.dumps(results,indent=4,ensure_ascii=False))

    print(len(results))