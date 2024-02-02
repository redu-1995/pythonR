import requests
from bs4 import BeautifulSoup
from types import NoneType
from telegram.constants import ParseMode
from urllib.parse import urljoin


zurl = 'https://www.bbc.com/amharic'
request_data = requests.get(zurl) 
our_content = request_data.content
soup = BeautifulSoup(our_content, 'html.parser')
print(request_data)

def scrap():
    json = []
    
    ulist = soup.find_all('li', {'class' : 'e13i2e3d1'})
    for inside_list in ulist:
        try:
            news_data = {}
            image = inside_list.find('img' , {'class' : 'bbc-1uwua2r'}).get('src')
            link = inside_list.find("a" , {"class":"bbc-1mirykb"}).get('href')
            title = inside_list.find('span').get_text()
            description = inside_list.find('p' , {'class' : 'ea6by781'}).get_text()
            #print(title) 
            
            if not (image is None) or not (description is None) or not (link is None) or not (title is None):
                news_data['image'] = image
                news_data['title'] = title
                news_data['description'] = description
                news_data['link'] = link
                json.append(news_data)        
        except Exception as e:
                print(e)
    #print(json)
    return(json)


def send_to_telegram():
    message = scrap()
    apiToken = '6053654763%3AAAHcF54O8dRyYBt2wYY6DAS_6xlm1Cfy2V4'
    chatID = '-1001687385030'
    url = f"https://api.telegram.org/bot{apiToken}/sendPhoto?chat_id={chatID}"

    for i in range(len(message)):
        msg = f"""<b><i>Title : </i> {message[i]['title']} \n</b><i>{message[i]['description']}</i> \n 📄<i>BBC Amharic</i> 📄 \n 🎤  """ 

        img_link = urljoin('https://www.bbc.com/', message[i]['link']) 
        
        payload = {
            "photo": message[i]['image'],
            "caption": msg + f"<a href=\"{img_link}\">view here</a>",
            "disable_notification": False,
            "reply_to_message_id": None,
            "parse_mode" : ParseMode.HTML
        }
        headers = {
            "accept": "application/json",
            "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        # print(response.text)
    

send_to_telegram()