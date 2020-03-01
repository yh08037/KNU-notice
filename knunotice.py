import requests
import threading
import datetime
import time
from bs4 import BeautifulSoup


class WebhookNotice:

    def __init__(self, notice_url, event_name, user_key):

        self.event_name = event_name
        
        self.notice_url = notice_url
        self.user_url = 'https://maker.ifttt.com/trigger/' + event_name + '/with/key/' + user_key
        
        self.soup = BeautifulSoup(requests.get(self.notice_url).text, 'html.parser')
        self.tags_tr = self.soup.find('tbody').findAll('tr')

        self.today = self.get_today()
        self.latest = ''

        self.reset_latest()


    def reset_latest(self):
        
        for tr in self.tags_tr:
            num, title, _ = self.get_info(tr)
            
            if num == '공지':
                continue
            else:
                self.latest = title
                break


    def get_today(self):
        
        return datetime.datetime.now().strftime('%Y-%m-%d')
    
    
    def get_info(self, tr):
        
        # 글 번호, 제목, 작성부서, 작성일 등 포함
        strings = list(filter(('\n').__ne__, list(tr.strings)))
        
        num = strings[0]                    # '공지' 또는 글 번호
        title = strings[1].strip('\n\t\r')  # 제목
        # team = strings[2]                   # 작성 부서

        # URL, 제목 등 포함
        subject = tr.find(attrs={'class':'subject'})
        url = 'https://knu.ac.kr' + str(list(subject)[1]).split()[1][6:-1].replace('&amp;', '&')

        del strings, subject
        
        # return num, title, team, url
        return num, title, url
    

    def request_post(self, info):

        title, url = info
        data = {'value1': title, 'value2': url}

        requests.post(self.user_url, data=data)


    def update_tags(self):
        
        self.soup = BeautifulSoup(requests.get(self.notice_url).text, 'html.parser')
        self.tags_tr = self.soup.find('tbody').findAll('tr')


    def check_new(self):

        self.update_tags()
        
        new_info_list = []

        # 자정이 지나면 latest를 reset!
        if self.today != self.get_today():
            self.reset_latest()
            self.today = self.get_today()
            
        for tr in self.tags_tr:
            num, title, url = self.get_info(tr)
                        
            if num == '공지':
                continue
            elif title == self.latest:
                break
            else: # new things!
                new_info_list.insert(0, (title, url))

        self.reset_latest()

        return new_info_list


    def post_new(self):

        new_info_list = self.check_new()
        
        for info in new_info_list:
            print('new post! -', self.event_name, info[0])
            self.request_post(info)


    def run(self, interval):
        
        now = datetime.datetime.now()
        print(self.event_name, 'thread running', now.strftime('%Y-%m-%d %H:%M:%S'))

        self.post_new()

        threading.Timer(interval, self.run, args=[interval]).start()


    



# 직접 실행될 때
if __name__ == "__main__":
    
    notice_url = 'https://knu.ac.kr/wbbs/wbbs/bbs/btin/list.action?bbs_cde=1&menu_idx=67'
    corona_url = 'http://knu.ac.kr/wbbs/wbbs/bbs/btin/list.action?bbs_cde=34&menu_idx=224'

    notice_event_name = 'knunotice'
    corona_event_name = 'knucorona'

    user_key = 'YOUR_IFTTT_WEBHOOK_KEY'
    
    notice_wh = WebhookNotice(notice_url, notice_event_name, user_key)
    corona_wh = WebhookNotice(corona_url, corona_event_name, user_key)

    notice_wh.run(120)
    time.sleep(60)
    corona_wh.run(120)
    

# import되어 사용될 때
else:  
    pass
