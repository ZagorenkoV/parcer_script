import requests
from tqdm import tqdm
import json
import os
import math
from config import API_KEY

# функция, которая принимает запрос
# в виде ключевого слова на основе которого формируются изображения или видео
def scrap_pexels(query=''):
    headers = {'Authorization': f'{API_KEY}'}
    query_str = f'https://api.pexels.com/v1/search?query={query}&per_page=80&orientation=landscape'

    # if you can't get access without VPN you could use such code. You need use your login
    # password, ip adress and port
    # proxies = {
    #     'https': f'http://{os.getenv("LOGIN")}: {os.getenv("PASSWORD")}@163.198.214.169:8000'
    # }

    response = requests.get(url=query_str, headers=headers) # you need add proxies=proxies if use it

    if response.status_code != 200:
        return f'Error: Status code - {response.status_code}, {response.json()}'
    
    img_dir_path = '_'.join(i for i in query.split(' ') if i.isalnum())

    if not os.path.exists(img_dir_path):
        os.makedirs(img_dir_path)

    json_data = response.json()

    # with open(f'result_{query}.json', 'w') as file:
    #     json.dump(json_data, file, indent=4, ensure_ascii=False)

    images_count = json_data.get('total_results')

    if not json_data.get('next_page'):
        img_urls = [item.get('src', {}).get('original') for item in json_data.get('photos')]
        download_images(img_list=img_urls, img_dir_path=img_dir_path)
    else:
        print(f'[INFO] Total images: {images_count}. Saving images may take some time. ')

        images_list_urls = []
        for page in range(1, math.ceil(images_count/80)+1):
            query_str = f'{query_str}&page={page}'
            response = requests.get(url=query_str, headers=headers) # if use proxies add proxies=proxies
            json_data = response.json()
            img_urls = [item.get('src', {}).get('original') for item in json_data.get('photos')]
            images_list_urls.extend(img_urls)
        download_images(img_list=img_urls, img_dir_path=img_dir_path)

def download_images(img_list=[], img_dir_path=''):
    for item_url in tqdm(img_list): #tqdm help us to add progress bar 
        response = requests.get(url=item_url)

        if response.status_code == 200:
            with open(f'./{img_dir_path}/{item_url.split("-")[-1]}', 'wb') as file:
                file.write(response.content)
        else:
            print('Oops, smth go wrong')

def main():
    query = input('Enter the key phrase: ')
    scrap_pexels(query=query)


if __name__ == '__main__':
    main()