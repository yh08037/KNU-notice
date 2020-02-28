import requests
import threading
from bs4 import BeautifulSoup



class WebhookNotice:

    def __init__(self):

        self.notice_url = 'https://knu.ac.kr/wbbs/wbbs/bbs/btin/list.action?bbs_cde=1&menu_idx=67'
        self.user_url = 'https://maker.ifttt.com/trigger/knunotice/with/key/YOUR_IFTTT_WEBHOOK_KEY' # need to be fixed to use this!
        
        self.soup = BeautifulSoup(requests.get(self.notice_url).text, 'html.parser')
        self.tags_tr = self.soup.find('tbody').findAll('tr')

        self.latest = 0

        

        for tr in self.tags_tr:
            num = self.get_num(tr)
            if num == '공지':
                continue
            else:
                self.latest = num
                break


    def get_num(self, tr):

        return list(tr.strings)[1]
    
    
    def get_info(self, tr):
        
        # 글 번호, 제목, 작성부서, 작성일 등 포함
        strings = list(filter(('\n').__ne__, list(tr.strings)))
        
        num = strings[0]            # '공지' 또는 글 번호
        title = strings[1][24:-7]   # 제목
        team = strings[2]           # 작성 부서


        # URL, 제목 등 포함
        subject = tr.find(attrs={'class':'subject'})
        url = 'https://knu.ac.kr' + str(list(subject)[1]).split()[1][6:-1].replace('&amp;', '&')

        del strings, subject
        
        # return num, title, team, url
        return title, url
    

    def request_post(self, tr):

        title, url = self.get_info(tr)        
        data = {'value1': title, 'value2': url}

        res = requests.post(self.user_url, data=data)

        return res


    def update_tags(self):
        
        self.soup = BeautifulSoup(requests.get(self.notice_url).text, 'html.parser')
        self.tags_tr = self.soup.find('tbody').findAll('tr')


    def check_new(self):

        self.update_tags()
        
        new_tr_list = []

        for tr in self.tags_tr:
            num = self.get_num(tr)
            if num == '공지':
                continue
            elif num == self.latest:
                break
            else: # new things!
                new_tr_list.insert(0, tr)

        return new_tr_list


    def post_new(self):

        new_tr_list = self.check_new()
        
        for tr in new_tr_list:
            print('hello')
            self.request_post(tr)


    def run(self):
        
        self.post_new()

        print('thread running')
        
        threading.Timer(5, self.run).start()
        



# 직접 실행될 때
if __name__ == "__main__":  
    
    WebhookNotice().run()

# import되어 사용될 때
else:  
    pass




'''
boardlist = soup.select_one('CSS 셀렉터') # 구체적인 파싱 부분은 사이트마다 다를테니 생략하겠습니다.
titles = boardlist.select('CSS 셀렉터')
 
lines = [line.rstrip('\n') for line in open('파일명.txt', 'r', encoding='인코딩')] # 파일 -> 리스트
 
f = open('파일명.txt', 'w', encoding='인코딩')
for title in titles: # 기존의 파싱 결과와 하나씩 대조하여 일치하는 것이 없으면 텔레그램 메시지를 보냅니다.
    count = 0
    check = 0
    while (count < len(lines)):
        if title.text == lines[count]:
            check = 1
        count += 1
    if check == 0:
        bot.sendMessage(chat_id=chat_id, text=title.text)
    f.write(title.text  + '\n')
f.close()
'''

