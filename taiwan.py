import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime
import pygsheets

options = Options()
#將chrome設定於背景執行

options.add_argument('--headless')
options.add_argument('--disable-gpu') # 允許在無GPU的環境下運行，可選

threads = []
def for_taiwan(url):
    #開啟google sheets連線
    #My MAC
    #gc = pygsheets.authorize(service_file='/Users/kkday/Documents/Python_Codes/python-230518-9f6b02dba966.json')
    #My Acer
    #gc = pygsheets.authorize(service_file='D:/Python Codes/ForTaiwan/ForTaiwan/python-230518-9f6b02dba966.json')
    #小博
    gc = pygsheets.authorize(service_file='/Users/peter/Documents/ForTaiwan/python-230518-9f6b02dba966.json')
    wks = gc.open('For Taiwan').sheet1
    wks.clear()
    #取得開始時間
    starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #My MAC
    #driver = webdriver.Chrome(chrome_options = options)
    #小博
    driver = webdriver.Chrome('/Users/peter/Documents/ForTaiwan/chromedriver',chrome_options = options)
    #My Acer
    #driver = webdriver.Chrome('D:/Python Codes/ForTaiwan/ForTaiwan/chromedriver.exe',chrome_options = options)
    driver.get(url)
    #專門抓小標題
    def branch_title(n):
        title = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div['+ str(n) +']/a')
        href = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div['+ str(n) +']/a').get_attribute('href')
        media = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div['+ str(n) +']/span[1]')
        print(title.text,media.text,href)                
        wks.append_table(values=[title.text,media.text,href])

    try:
        for p in range(1,8):
            for i in range(1,11):
                title = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div[1]/h3/a')
                href = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div[1]/h3/a').get_attribute('href')
                media = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div/div[1]/span[1]')
                wks.append_table(values=[title.text,media.text,href])
                print(title.text,media.text,href)
                try:
                    branch_title(2)
                    branch_title(4)
                    branch_title(6)
                    branch_title(8)
                    branch_title(10)
                    branch_title(12)
                except:
                    print('')
            driver.find_element_by_xpath('//*[@id="pnnext"]/span[1]').click()
            sleep(1)
    except:
        print('抓取完成')
    driver.quit()
    wks.update_value('G1','更新時間：'+ starttime)

tw_team_url = "https://www.google.com/search?q=%E5%9F%BA%E9%80%B2&tbm=nws&sxsrf=ACYBGNQJ9yDtKxuwpJnX68MTTSDMimXwaw:1574778340751&source=lnt&tbs=sbd:1&sa=X&ved=0ahUKEwjav-a8iojmAhVwyYsBHT4cAxcQpwUIIA&biw=1396&bih=612&dpr=1.38"
cby_url = "https://www.google.com/search?q=%E9%99%B3%E6%9F%8F%E6%83%9F&tbm=nws&sxsrf=ACYBGNQ-ntYM-DBolXlD6FZOkdkvJYgAAQ:1574503025897&ei=cQLZXbexNsLemAW-prKgCw&start=0&sa=N&ved=0ahUKEwj3rbnsiIDmAhVCL6YKHT6TDLQ4WhDy0wMIVw&biw=1913&bih=921&dpr=1"

urls = [tw_team_url,cby_url]

threads.append(threading.Thread(target = for_taiwan,args=(urls[0],)))
threads[0].start()






