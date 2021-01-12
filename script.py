import os
import json
import requests # for get requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

base_url = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'

user_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}
folder = "Images"



def main():

    if not os.path.exists(folder):
        os.mkdir(folder)

    download()


def download():

    keyword = input("Keyword: ")
    number = int(input("Number of Images: "))

    print("Searching...")

    options = Options()
    options.binary_location = 'C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/brave.exe'
    driver_path = 'C:/Program Files (x86)/BraveSoftware/Brave-Browser/Application/chromedriver.exe'
    driver = webdriver.Chrome(options = options, executable_path = driver_path)

    search_url = base_url + 'q=' + keyword
    print(search_url)

#   response = requests.get(search_url,user_agent)
#   markup = response.text # idhar gadbad ho sakti hai

    driver.get(search_url)

    i=0

    while i<7:  
	    #for scrolling page
        driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")
    
    try:
		#for clicking show more results button
        driver.find_element_by_xpath("/html/body/div[2]/c-wiz/div[3]/div[1]/div/div/div/div/div[5]/input").click()
    except Exception as e:
        pass
    time.sleep(5)
    i+=1

    crawler = BeautifulSoup(driver.page_source,'html.parser')
    results = crawler.find_all(name = 'img',attrs = {'class':'t0fcAb'},limit=number)

    links = []

    for i in results:
        
        img_link = i['src']
        links.append(img_link) # Storing all the image links to a list 

    if len(links) == 0:
        print("ERROR, No Images Found")
        exit(0) # Exception Handling

    print(f'found {len(links)} images')
    print('downloading...')

    for i, imagelink in enumerate(links):
        # open image link and save as file
        response = requests.get(imagelink)
        
        imagename = folder + '/' + keyword + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)
    
    driver.close()
    print('Done')


if __name__ == "__main__":

    main()
