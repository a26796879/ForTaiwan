import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime
options = Options()
#將chrome設定於背景執行
'''
options.add_argument('--headless')
options.add_argument('--disable-gpu') # 允許在無GPU的環境下運行，可選
'''
#開啟google sheets連線
import pygsheets
gc = pygsheets.authorize(service_file='F:\python codes\google_sheets_API\python-230518-9f6b02dba966.json')
wks = gc.open('For Taiwan').sheet1
wks.clear()
#取得開始時間
starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
threads = []

def for_taiwan(url):
    driver = webdriver.Chrome('G:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe', chrome_options = options)
    driver.get(url)
    #專門抓小標題
    def branch_title(n):
        title = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div['+ str(n) +']/a')
        href = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div['+ str(n) +']/a').get_attribute('href')
        print(title.text,href)                
        wks.append_table(values=[title.text,href])
    
    try:
        for p in range(1,50):
            for i in range(1,11):
                title = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div[1]/h3/a')
                href = driver.find_element_by_xpath('//*[@id="rso"]/div/div['+ str(i) +']/div/div[1]/h3/a').get_attribute('href')
                wks.append_table(values=[title.text,href])
                print(title.text,href)
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
            sleep(2)
    except:
        print('抓取完成')
    driver.quit()
    wks.update_value('G1','更新時間：'+ starttime)


tw_team_url = "https://www.google.com/search?sxsrf=ACYBGNRPb9cvmU2J4PXN6PtaCCPDrJ99ZA:1574443574109&q=%E5%9F%BA%E9%80%B2&tbm=nws&source=univ&tbo=u&sxsrf=ACYBGNRPb9cvmU2J4PXN6PtaCCPDrJ99ZA:1574443574109&sa=X&ved=2ahUKEwjdndCvq_7lAhW1xIsBHapyDuEQt8YBKAF6BAgBEAY&biw=1913&bih=921"
cby_url = "https://www.google.com/search?q=%E9%99%B3%E6%9F%8F%E6%83%9F&tbm=nws&sxsrf=ACYBGNQ-ntYM-DBolXlD6FZOkdkvJYgAAQ:1574503025897&ei=cQLZXbexNsLemAW-prKgCw&start=0&sa=N&ved=0ahUKEwj3rbnsiIDmAhVCL6YKHT6TDLQ4WhDy0wMIVw&biw=1913&bih=921&dpr=1"

urls = [tw_team_url,cby_url]

threads.append(threading.Thread(target = for_taiwan(tw_team_url)))
threads.append(threading.Thread(target = for_taiwan(cby_url)))
for i in range(2):
    #threads.append(threading.Thread(target = for_taiwan(urls[i])))
    threads[i].start()



'''
'//*[@id="rso"]/div/div[1]/div/div[1]/h3/a'
'//*[@id="rso"]/div/div[1]/div/div[2]/a'
'//*[@id="rso"]/div/div[1]/div/div[4]/a'
'//*[@id="rso"]/div/div[1]/div/div[6]/a'
'//*[@id="rso"]/div/div[1]/div/div[8]/a'
'//*[@id="rso"]/div/div[2]/div/div[1]/h3/a'
'//*[@id="rso"]/div/div[2]/div/div[2]/a'
'//*[@id="rso"]/div/div[2]/div/div[4]/a'
'//*[@id="rso"]/div/div[2]/div/div[6]/a'
'//*[@id="rso"]/div/div[2]/div/div[8]/a'
'//*[@id="rso"]/div/div[3]/div/div[2]/a'
'//*[@id="rso"]/div/div[3]/div/div[4]/a'
'//*[@id="rso"]/div/div[3]/div/div[6]/a'
'//*[@id="rso"]/div/div[3]/div/div[8]/a'
'//*[@id="rso"]/div/div[4]/div/div[2]/a'
'//*[@id="rso"]/div/div[4]/div/div[4]/a'
'//*[@id="rso"]/div/div[4]/div/div[6]/a'
'//*[@id="rso"]/div/div[4]/div/div[8]/a'
'''