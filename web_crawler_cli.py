'''
web_crawler.py

a short script that pulls images from reddit and downloads them

author: Philippe Naon
'''
import urllib.request, json, time, requests, os, sys

if sys.argv[1] == '-help':
    print('takes 3 arguments; the subreddit, how to sort, and the folder to download to')
    print('example: python web_crawler.py Eyebleach new download_reddit_images')
    print('Eyebleach: the subreddit')
    print('new: posts sorted by newest')
    print('download_reddit_images: images are downloaded to this folder')
elif len(sys.argv) != 4:
    print('argument count', len(sys.argv), 'should be 3, exiting...')
else:
    folder = sys.argv[3] + '/'
    if not os.path.exists(folder):
            os.makedirs(folder)
    url = 'https://www.reddit.com/r/' + sys.argv[1] + '/' + sys.argv[2] + '.json?sort=' + sys.argv[2]
    with requests.get(
        url, 
        headers = {'User-agent': 'phils bot heh'}) as req:
        data = req.json()
        print('getting images from', url)
        posts = data['data']['children']

        for post in posts:
            if post['data']['url'].endswith('.jpg'):
                img_url = str(post['data']['url'])

                title = post['data']['title']
                img_name = title[:32].replace(' ', '_').lower()
                full_img_name = folder + img_name + '.jpg'

                urllib.request.urlretrieve(img_url, full_img_name)
                time.sleep(1)
