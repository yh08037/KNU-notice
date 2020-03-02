import requests
import threading
import datetime
import time
from bs4 import BeautifulSoup


class WebhookNotice:

    def __init__(self, notice_url, event_name, user_keys):

        self.event_name = event_name
        
        self.notice_url = notice_url
        self.user_urls = [self.get_user_url(user_key) for user_key in user_keys]
        
        self.soup = BeautifulSoup(requests.get(self.notice_url).text, 'html.parser')
        self.tags_tr = self.soup.find('tbody').findAll('tr')

        self.today = self.get_today()
        self.latest = ''

        self.update_latest()


    def get_user_url(self, user_key):

        # 용도: 여러명의 사용자의 키가 들어있는 리스트를 사용자 URL 리스트로 변환하기 위함
        # 입력: 한 사용자의 webhook KEY
        # 출력: 한 사용자의 해당 이벤트에 대한 webhook trigger URL

        return 'https://maker.ifttt.com/trigger/' + self.event_name + '/with/key/' + user_key


    def get_today(self):

        # 용도: 매일 자정 일어나는 게시 중단으로 인한 오작동을 방지하기위함
        # 입력: -
        # 출력: 오늘의 날짜 (형식 - "2020-03-03")

        return datetime.datetime.now().strftime('%Y-%m-%d')

    
    def update_tags(self):

        # 용도: 공지사항 게시판의 html을 새로 불러와서 파싱함
        # 입력: -
        # 출력: -
        
        self.soup = BeautifulSoup(requests.get(self.notice_url).text, 'html.parser')
        self.tags_tr = self.soup.find('tbody').findAll('tr')
    
    
    def update_latest(self):

        # 용도: 새로운 글이 올라와 POST를 한 이후 self.latest 값을 업데이트하기 위함
        # 입력: -
        # 출력: -
        
        for tr in self.tags_tr:
            num, title, _ = self.get_info(tr)
            
            if num == '공지':
                continue
            else:
                self.latest = title
                break


    def get_info(self, tr):

        # 용도: tr개체를 파싱하여 한 게시물에 대한 정보를 반환함
        # 입력: html로부터 파싱한 tr개체
        # 출력: 한 게시물의 글번호, 제목, 링크URL
        
        # 글 번호, 제목, 작성부서, 작성일 등 포함
        strings = list(filter(('\n').__ne__, list(tr.strings)))
        
        num = strings[0]                    # '공지' 또는 글 번호
        title = strings[1].strip('\n\t\r')  # 제목
        # team = strings[2]                   # 작성자

        # URL, 제목 등 포함
        subject = tr.find(attrs={'class':'subject'})
        url = 'https://knu.ac.kr' + str(list(subject)[1]).split()[1][6:-1].replace('&amp;', '&')

        del strings, subject
        
        return num, title, url
    

    def check_new(self):

        # 용도: 게시판 첫페이지에 어떤 새로운 게시글이 올라왔는지 체크함
        # 입력: -
        # 출력: 알림을 띄워야할 게시글들의 정보(제목, URL)의 리스트
        
        self.update_tags()
        
        new_info_list = []

        # 자정이 지나면 latest를 reset!
        if self.today != self.get_today():
            self.update_latest()
            self.today = self.get_today()
            
        for tr in self.tags_tr:
            num, title, url = self.get_info(tr)
                        
            if num == '공지':
                continue
            elif title == self.latest:
                break
            else: # new things!
                new_info_list.insert(0, (title, url))

        self.update_latest()

        return new_info_list
    

    def request_post(self, info):

        # 용도: 게시글의 정보를 형식에 맞추어 사용자들의 webhook trigger에 POST함
        # 입력: 게시글의 정보(글제목, URL)
        # 출력: -

        title, url = info
        data = {'value1': title, 'value2': url}

        for user_url in self.user_urls:
            requests.post(user_url, data=data)


    def post_new(self):

        # 용도: 새로운 게시글이 있으면 사용자들의 webhook trigger에 POST함
        # 입력: -
        # 출력: -

        new_info_list = self.check_new()
        
        for info in new_info_list:
            print('new post! -', self.event_name, info[0])
            self.request_post(info)


    def run(self, interval):

        # 용도: 일정한 주기로 호출되어 새로운 게시글을 확인해 POST하기 위함
        # 입력: 초(s) 단위의 호출 주기
        # 출력: -
        
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
    
    # all users
    key_dict = {'user1' : 'USER_1_IFTTT_WEBHOOK_KEY',   # need to be fixed to use these!
                'user2' : 'USER_2_IFTTT_WEBHOOK_KEY',
                'user3' : 'USER_3_IFTTT_WEBHOOK_KEY'}
    
    # current activated users
    user_name_list = ['user2', 'user3']

    user_keys = [key_dict[name] for name in user_name_list]
   
    notice_wh = WebhookNotice(notice_url, notice_event_name, user_keys)
    corona_wh = WebhookNotice(corona_url, corona_event_name, user_keys)

    notice_wh.run(120)
    time.sleep(60)
    corona_wh.run(120)


# import되어 사용될 때
else:  
    pass
