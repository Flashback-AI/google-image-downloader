import os
import json
import requests # for get requests
from bs4 import BeautifulSoup


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
    number = input("Number of Images: ")

    print("Searching...")

    search_url = base_url + 'q=' + keyword
    print(search_url)

    response = requests.get(search_url,user_agent)
    markup = response.text

    crawler = BeautifulSoup(markup,'html.parser')
    results = crawler.find_all(name = 'div',attrs = {'class':'rg_meta'},limit=number)

    links = []

    for i in results:
        print(i.text)
        dic = json.loads(i.text)
        link = dic['ou']
        links.append(link)

    print(f'found {len(links)} images')
    print('downloading...')

    for i, imagelink in enumerate(links):
        # open image link and save as file
        response = requests.get(imagelink)
        
        imagename = folder + '/' + keyword + str(i+1) + '.jpg'
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print('Done')


if __name__ == "__main__":

    main()