'''
web_crawler.py

a short script that pulls images from reddit and downloads them

author: Philippe Naon
'''
import urllib.request, json, time, requests, os

folder = 'downloaded_reddit_images/'
if not os.path.exists(folder):
        os.makedirs(folder)

url = 'https://www.reddit.com/r/Eyebleach/new.json?sort=new'
with requests.get(url, headers = {'User-agent': 'phils bot heh'}) as req:
    data = req.json()
    posts = data['data']['children']

    for post in posts:
        if post['data']['url'].endswith('.jpg'):
            img_url = str(post['data']['url'])

            title = post['data']['title']
            img_name = title[:32].replace(' ', '_').lower()
            full_img_name = folder + img_name + '.jpg'

            urllib.request.urlretrieve(img_url, full_img_name)
            time.sleep(1)
