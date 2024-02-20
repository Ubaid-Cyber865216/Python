import requests,random,uuid,string,time,json,getpass,threading,os
import webbrowser
na = webbrowser.open('https://t.me/uiujq')    
from colorama import Fore
class StoryWatch():

    
    def __init__(self):
        
        self.uid = str(uuid.uuid4())
        
        self.str = string.digits + string.ascii_lowercase
        
        self.r = requests.Session()
        
        self.watched = 0
        
        self.error = 0
        
        self.skipped=0
        
        self.people = []
        
        self.stories_seen = []
        os.system('cls||clear')
        
        print(Fore.CYAN+"""\x1b[1;31mStory Instagram """)
        
        
        
        self.login()
        
    
    def  login(self):
        
        username = str(input(Fore.LIGHTBLUE_EX+'[+] username : '))
        password = str(getpass.getpass(Fore.LIGHTBLUE_EX+'[+] password : '))

        url = 'https://i.instagram.com/api/v1/accounts/login/'
        self.headers = {
            'X-Pigeon-Session-Id': str(uuid.uuid4()),
            'X-IG-Device-ID': str(uuid.uuid4()),
            'X-IG-App-Locale': 'en_US',
            'X-IG-Device-Locale': 'en_US',
            'X-IG-Mapped-Locale': 'en_US',
            'X-IG-Connection-Type': 'WIFI',
            'X-IG-Capabilities': '3brTvw8=',
            'User-Agent': 'Instagram 148.0.0.33.121 Android (28/9; 480dpi; 1080x2137; HUAWEI; JKM-LX1; HWJKM-H; kirin710; en_US; 216817344)',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'i.instagram.com'
        }

        data = {
            '_uuid': uuid.uuid4(),
            'username': username,
            'enc_password': '#PWD_INSTAGRAM_BROWSER:0:1589682409:{}'.format(password),
            'queryParams': '{}',
            'optIntoOneTap': 'false',
            'device_id': uuid.uuid4(),
            'from_reg': 'false',
            '_csrftoken': 'missing',
            'login_attempt_count': '0'
        }
        
        req = requests.post(url, headers=self.headers, data=data)
        if ('logged_in_user') in req.text:
            print(Fore.GREEN+f"[+] Logged in with {username}")
            self.cookies = req.cookies
            self.pk = req.json()['logged_in_user']['pk']
            
            self.getinfo()
            
        elif ('challenge') in req.text:
            print(
                Fore.BLUE+f"[!] challenge_requierd please accept and login again ...")
            input("")
            exit()
        else:
            print(Fore.RED+f"[-] bad username or password ...")
            input("")
            exit()

            
            
    def getinfo(self):
        
        self.target = str(input(Fore.LIGHTBLUE_EX+'[+] User : '))
        
        try:
            get = self.r.get(
                f'https://www.instagram.com/{self.target}/?__a=1', cookies=self.cookies).json()

            self.target_id = str(get["logging_page_id"]).split('_')[1]
        except:

            print(Fore.RED+"[x] No User Found !!")
            self.getinfo()
        
        self.sleep = str(input(Fore.LIGHTCYAN_EX+'[+] sleep : '))
        threading.Thread(target=self.start).start()
        
    def _generate_device(self,N):
    	return ''.join([random.choice('0123456789ABCDEF') for x in range(N)])
        
    def start(self):
        self.csfr = self.r.cookies['csrftoken']
        head = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
        
        info = requests.get(
            f"https://www.instagram.com/{self.target}/?__a=1", headers=head, cookies=self.cookies)
        
        self.count = info.json()[
            "graphql"]["user"]["edge_followed_by"]["count"]
        
        self.h = "https://www.instagram.com/graphql/query/?query_hash=5aefa9893005572d237da5068082d8d5"
        self.follow_url = f"{self.h}&variables=%7B%22id%22%3A%22{self.target_id}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A50%7D"
        
        while 1:
            
            self.people.clear()
            
            while len(self.people) < self.count:
                
                req = requests.get(
                    self.follow_url, headers=head, cookies=self.cookies)
                try:
                    self.end_cursor = req.json(
                )["data"]["user"]["edge_followed_by"]["page_info"]["end_cursor"]
                except:
                    break
                for user in req.json()["data"]["user"]["edge_followed_by"]["edges"]:
                    self.device = '%s-%s-%s-%s-%s' % (self._generate_device(8),  self._generate_device(
                        4), self. _generate_device(4), self. _generate_device(4), self. _generate_device(12))
                    username = user["node"]["username"]
                    pk = user["node"]["id"]
                    private = user["node"]["is_private"]
                    if not username in self.people:
                        if private:
                            self.people.append(username)
                            pass
                        else:
                            
                            self.people.append(username)
                            
                            get = self.r.get(
                                f"https://i.instagram.com/api/v1/feed/reels_media/?reel_ids={pk}", headers=self.headers,cookies=self.cookies).json()
                            try:
                                for i in get["reels"][pk]["items"]:
                                    id = i['pk']
                                    taken_at = i['taken_at']
                                    str1 = '%s_%s' % (id, pk)
                                    str2 = '%s_%s' % (taken_at, int(time.time()))
                                    
                                    
                                    dataPost = {
                    'reelMediaId':str(id),
                    'reelMediaOwnerId':str(pk),
                    'reelId':str(pk),
                    'reelMediaTakenAt':str(taken_at),
                    'viewSeenAt':taken_at
                }
                                    head = {
                                        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
                                        'x-csrftoken': self.csfr,
                                    }
                                    
                                    if id in self.stories_seen:
                                        pass
                                    else:
                                    
                                        see = self.r.post(
                                            "https://www.instagram.com/stories/reel/seen", headers=head, data=dataPost, cookies=self.cookies)
                                        
                                        if '{"status":"ok"}' in see.text:
                                            
                                            self.watched+=1
                                            
                                            self.stories_seen.append(id)
                                        
                                        else:
                                            self.error+=1
                                        ln = len(self.people)
                                        os.system('cls||clear')
                                        print(Fore.CYAN+"--------- sufi ---------\n"+Fore.WHITE+f"username : {username}\n"+Fore.LIGHTGREEN_EX +
                                            f"watched : {self.watched}\n"+Fore.LIGHTRED_EX+f"error : {self.error}\n"+Fore.LIGHTCYAN_EX+f"people loaded : {ln}\n"+Fore.LIGHTMAGENTA_EX+f"skipped : {self.skipped}")
                                time.sleep(self.sleep)
                            except Exception as e:
                                    self.skipped+=1
                                    ln = len(self.people)
                                    os.system('cls||clear')
                                    print(Fore.CYAN+"--------- sufi ---------\n"+Fore.WHITE+f"username : {username}\n"+Fore.LIGHTGREEN_EX +
                                          f"watched : {self.watched}\n"+Fore.LIGHTRED_EX+f"error : {self.error}\n"+Fore.LIGHTCYAN_EX+f"people loaded : {ln}\n"+Fore.LIGHTMAGENTA_EX+f"skipped : {self.skipped}")
                self.follow_url = f"{self.h}&variables=%7B%22id%22%3A%22{self.target_id}%22%2C%22include_reel%22%3Atrue%2C%22fetch_mutual%22%3Atrue%2C%22first%22%3A50%2C%22after%22%3A%22{self.end_cursor}%22%7D"

if __name__ == '__main__':
    StoryWatch()
