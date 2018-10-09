import requests
import lxml, string, time, json, os
from bs4 import BeautifulSoup
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

dts = []


class TestBook:

    def __init__(self):
        self.exams = self.exams()

    def login(self):
        path = 'C://chromedriver.exe'
        chromeOptions = Options()
        chromeOptions.add_argument('--disable-extensions')
        chromeOptions.add_argument('--profile-directory=Default')
        chromeOptions.add_argument("--disable-infobars")
        chromeOptions.add_argument("--incognito")
        chromeOptions.add_argument("--disable-plugins-discovery")
        chromeOptions.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(chrome_options=chromeOptions, executable_path=path)
        self.driver.get('https://testbook.com/login?tile=login&modal=true&redirect_url=%2F')
        self.driver.find_element_by_class_name('btn-google').click()
        time.sleep(1)
        email = ""
        password = ""
        #glink = 'https://accounts.google.com/signin/oauth?client_id=507873004357-e1fud3dkucl8g9i17dtl1hqfmjhnj5vp.apps.googleusercontent.com&as=l7jOPt7NLvHsNkEdKFIvGg&destination=https://testbook.com&approval_state=!ChRKRDd1S3BwYVp0aFV1anVNTWo3NxIfZzg3Mi1TVWpsdW9kOEhuU1JuY2dubW91cHd3YVlCWQ%E2%88%99ANKMe1QAAAAAW6efhmqII8Pfylo1du1TIBF1c5EAWpnC&oauthgdpr=1&xsrfsig=AHgIfE9QTtqdf-Rsx-AehWy1VM6j1uCytQ'
        #self.driver.get(glink)
        self.driver.find_element_by_id('identifierId').send_keys(email)
        time.sleep(1)
        self.driver.find_element_by_css_selector('#identifierNext').click()
        time.sleep(3.5)
        self.driver.find_element_by_name('password').send_keys(password)
        time.sleep(1)
        self.driver.find_element_by_css_selector('#passwordNext').click()

    def complete(self, test_type='bank-po', test_id='5b3a4f1f28ba9f0cbbb6b87b'):
        data_link = "https://testbook.com/{}/tests/{}#/lt-test".format(test_type, test_id)
        self.driver.get(data_link)
        time.sleep(2)
        try:
            try:
                myElem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#sidebar > div > div.marks-action > button.btn.btn-theme.btn-block.for-all-exams')))
            except:
                myElem = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#sidebar > div > div.marks-action > button.btn.btn-yellow-green.btn-block.for-ssc')))
            try:
                self.driver.find_element_by_css_selector(
                '#sidebar > div > div.marks-action > button.btn.btn-theme.btn-block.for-all-exams').click()
            except:
                self.driver.find_element_by_css_selector('#sidebar > div > div.marks-action > button.btn.btn-yellow-green.btn-block.for-ssc').click()

            time.sleep(2)
            self.driver.find_element_by_css_selector(
                'body > div.bootbox.modal.fade.bootbox-confirm.in > div > div > div.modal-footer > button.btn.btn-test-primary').click()
            time.sleep(5)
            self.driver.find_element_by_link_text('Continue').click()
        except Exception as e:
            print(e)
            print("Already Submitted")

    def save_file(self, obj, test_type):
        """Check if exam json file exists or not"""
        path = obj[1][0] + obj[0] + '_inst.json'
        # print(path)
        if not os.path.exists(path):
            try:
                os.makedirs(obj[1][0])
            except:
                pass
            cont = self.instruction(obj[0])
            with open(obj[0] + '_inst.json', 'w') as outfile:
                json.dump(cont, outfile)
            os.rename(obj[0] + '_inst.json', path)
            print("Instruction Done")
            "after downloading instruction file we will get testId json, first call complete function then get data"
            #self.complete()
            self.complete(test_type,obj[0])
            #now_getting_data
            cont = self.get_data(test_type,obj[0])
            with open(obj[0] + '.json', 'w') as outfile:
                json.dump(cont, outfile)
            os.rename(obj[0] + '.json', obj[1][0] + obj[0] + '.json')
            print("Json Done")

    def get_data(self, t_type='bank-po', t_id='5add58785513640c227bc182'):
        link = "https://api.testbook.com/api/v2/tests/{}?auth_code=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJUQiIsImVtYWlsIjoiaGFyc2hpdHBhcmVla2pudW5ld2FpQGdtYWlsLmNvbSIsImV4cCI6IjIwMTgtMDktMDNUMTc6MDc6MjMuNzYyMzE5MzU2WiIsImlhdCI6IjIwMTgtMDgtMDRUMTc6MDc6MjMuNzYyMzE5MzU2WiIsImlzcyI6Imh0dHBzOi8vdGVzdGJvb2suY29tIiwibmFtZSI6IkhhcnNoaXQgUGFyZWVrIiwicm9sZXMiOiJzdHVkZW50Iiwic3ViIjoiNWIwYWViNDQ4MTU3MjYwYzM5MWNmZmEyIn0.RS01D_tequgCLsCDqC0__1FNWZEgigB2Q-NTY6-cLRg6j9zigsXMfVMGt1kmED1-kUEtOCurNs02uE96LbhqyWOG9Z8alfxY-pStVMR0e9-vks6mvDuiVO_nyjo8yAGP-GuMuC_ugftHvm6xlp_uThIiTPgnghF3oHM5l5N8TGk&X-Tb-Client=web,1.2"
        r = requests.get(url=link.format(t_id + '/answers'))
        cont = json.loads(r.text)
        return cont
        '''
        if not os.path.exists(t_type+"/"+t_id+'.json'):
          try:
            os.makedirs(t_type)
          except:
            pass
          with open(t_id+'.json', 'w') as outfile:
            json.dump(cont,outfile)
          os.rename(t_id+'.json',str(t_type)+"/"+str(t_id)+'.json')
          print(str(t_id)+" Done")
        '''

    def exams(self):
        url = "https://testbook.com/wcapi/v1/courses.json?fields=id,URL"
        response = requests.get(url)
        data = response.json()
        return [i for i in data["data"]]

    def format_filename(self, s):
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        filename = ''.join(c for c in s if c in valid_chars)
        filename = filename.replace(' ', '_')
        return filename

    def instruction(self, examId):
        url = "https://api.testbook.com/api/v2/tests/{}/instructions?X-Tb-Client=web,1.2".format(examId)
        r = requests.get(url)
        cont = json.loads(r.text)
        return cont

    def examName(self, exam):
        url = "https://api.testbook.com/api/v2/courses/{}/products?X-Tb-Client=web,1.2".format(exam)
        response = requests.get(url)
        data = response.json()
        category = ""
        _data = {}
        # main content
        try:
            for i in data["data"]["products"]:
                category = i['courses'][0]['name']
                examNames = i["specificExams"][0]['name']
                path = self.format_filename(category) + "/" + self.format_filename(examNames) + "/"
                for j in i['items']:
                    _data[j['id']] = [path]
        except Exception as e:
            pass
        try:
            for i in data["data"]["tests"]:
                examNames = i["specificExams"][0]['name']
                path = self.format_filename(category) + "/" + self.format_filename(examNames) + "/"
                _data[i['id']] = [path]
        except:
            pass
        try:
            for i in data["data"]["quizzes"]:
                paths = []
                for j in i["specificExams"]:
                    examNames = j['name']
                    path = self.format_filename(category) + "/" + self.format_filename(examNames) + "/"
                    paths.append(path)
                _data[i['id']] = paths
        except:
            pass
        print("-------------")
        return _data


obj = TestBook()
obj.login()
for everyExam in obj.exams:
    if 'ssc' in everyExam['URL']:
        # print(everyExam['id'])
        resp = obj.examName(everyExam['id'])
        time.sleep(2)
        '''after getting data of a single exam login to account call save function with object and check if instruction file exists '''
        for items in resp.items():
            obj.save_file(items,everyExam['URL'])
