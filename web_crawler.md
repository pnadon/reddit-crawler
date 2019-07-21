# Web Crawler with Python
This tutorial will show to make a web crawler using simple Python and built-in packages.

## Prerequisites
You must have gone through the setup tutorial, or at least have python installed along with a basic text editor.

## Reddit's JSON api
### visualizing the JSON
The first thing to do is obtain a list of posts from our favorite subreddit.
For this tutorial I have chosen **r/Eyebleach**, which I occasionally visit for pictures
of cats and other soul-cleansing content. 

Luckily for us, Reddit offers a [JSON](https://www.json.org/) [api](https://en.wikipedia.org/wiki/Application_programming_interface), which gives developers like us easy access to content.

For example, if you visit [https://www.reddit.com/r/Eyebleach/new.json?sort=new](https://www.reddit.com/r/Eyebleach/new.json?sort=new), you will see a wall of text appear. While it looks like a mess
right now, [VSCode](https://code.visualstudio.com/) has a neat trick which lets
us automatically format a document and make it more readable. Copy and paste the
wall of text into VSCode, and then press `ctrl` + `shift` + `p` for Windows, or 
`command` + `shift` `p` for MacOS, to bring up the command palette. Use this
palette to search for the `Format Document` command, and press enter. You should
see the wall of text organize itself into a hierarchical structure. 
This is JSON.

Familiarize yourself with the content, and notice the sort of information this
gives you.

### Using Python to obtain the JSON object
We can obtain this information and turn it into a format that Python can use, by
using the following code:

```python
import urllib.request, json, time, requests, os

url = 'https://www.reddit.com/r/Eyebleach/new.json?sort=new'
with requests.get(url, headers = {'User-agent': 'phils bot heh'}) as req:
    data = req.json()
```

The first line simply assigns the JSON's url to the variable `url`, so we can use
it elsewhere. In the second line, we see that we make a request, with the first
parameter being `url` (the url), and the second being `headers`, which basically
tells reddit who is accessing the JSON (otherwise we get the default one, which
will almost always gives us an error since its overused). Notice the `as req`, 
that simply tells Python that we're calling this request `req` from now on.

Lastly, we assign the variable `data` the value of `req.json()`, which basically
converts the JSON to a Python Dictionary (similar, but something Python can use).

## Post information in JSON
### JSON Structure
Now we need to obtain all the posts in the JSON response. If we look at the structure
of the JSON object, we see that it looks something like the following:
```python
{
    "kind": "Listing",
    "data": {
        ...
        "children": [
            ...
        ]
    }
}
```

We can see visually that the posts are separated by commas inside the brackets after `"children"`,
sort of like this `"children": [post, post, post, ...]`. In turn, `"children"` is inside of `"data"`,
and `"data"` is inside of the surrounding braces. Thus, the hierarchy is as follows:
`"json" -> "data" -> "children" -> post`.

### Obtaining posts from JSON
Remember that the JSON object was converted to a Python Dictionary, which we can
for the most part assume is the same thing. From now on we will refer to the
converted JSON object as the data.

To access the list of posts from the dictionary, we can assign a variable to
`"children"` in the data, which holds the posts, and then iterate through them:

```python
import urllib.request, json, time, requests, os

url = 'https://www.reddit.com/r/Eyebleach/new.json?sort=new'
with requests.get(url, headers = {'User-agent': 'phils bot heh'}) as req:
    data = req.json()
    posts = data['data']['children'] # children is the list of posts

    for post in posts: # to something to each post in posts
        # do something
```

This means we will do something to each post inside of `posts`, which is equal to
the "children" key inside of the JSON object

## Obtaining the image
### Make sure its a JPG
now we need to define what we're doing to the posts. First off, we have to ask ourselves,
*do we want to obtain images from every post? What if the post doesn't contain an image?*
If we try to download an image from a text-only post, our code will run into a problem!

To make sure our post contains an image, specifically a `JPG`, we can look at the
value of the `url`, which appears to holds the url to the full-resolution image.
If it's a `JPG` image, it will end with `.jpg`, so we can use that as criteria
for which post we want to use:

```python
import urllib.request, json, time, requests, os

url = 'https://www.reddit.com/r/Eyebleach/new.json?sort=new'
with requests.get(url, headers = {'User-agent': 'phils bot heh'}) as req:
    data = req.json()
    posts = data['data']['children']

    for post in posts:
        if post['data']['url'].endswith('.jpg'): # make sure url ends with .jpg
            # only runs if the above is true
```

This newly-added line checks this criteria, and the code inside only runs if that
criteria is met.

### Get the url, and title (for the file name)
We can assign to variables the url and title of the image.


```python
            img_url = str(post['data']['url'])
            title = post['data']['title']
```

But if you notice, the title can get pretty long, and contains spaces. Because
we are developers, we dont like file names with spaces in them (you see why eventually),
so lets shorten the title to 32 characters, replace spaces with `_`, and make it lowercase!

```python
            img_name = title[:32].replace(' ', '_').lower()
```

`title[:32]` returns a "slice" of `title`, containing only the first 32 characters.
`.replace(' ', '_')` replaces the first parameter (a space) with the second (an underscore).
`.lower()`  makes it lowercase.

We also need to assign to a variable the full file name of our image, which is
a concatenation (combination) of the folder name, the file, and extention. 
Together, this makes:

```python
import urllib.request, json, time, requests, os

folder = 'downloaded_reddit_images/' # THIS LINE WAS ADDED!!!!
if not os.path.exists(folder): # THIS LINE WAS ADDED!!!!
        os.makedirs(folder) # THIS LINE WAS ADDED!!!!

url = 'https://www.reddit.com/r/Eyebleach/new.json?sort=new'
with requests.get(url, headers = {'User-agent': 'phils bot heh'}) as req:
    data = req.json()
    posts = data['data']['children']

    for post in posts:
        if post['data']['url'].endswith('.jpg'): # make sure url ends with .jpg
            # str( ...) is used to convert some weird symbols into a proper string
            img_url = str(post['data']['url'])

            title = post['data']['title']
            img_name = title[:32].replace(' ', '_').lower()
            full_img_name = folder + img_name + '.jpg'
```

The 3 lines added near the top assign the folder's name to `folder`, and then
creates the folder if it doesnt exist.

### download the image

Finally, we can download the image, by using `urllib.request.urlretrieve` and passing
the url to get the image from, and the file to save it to as parameters. After
doing this, we should wait a second before downloading another; if we download
too many at once, Reddit will get mad at us! Here is the full code:

```python
import urllib.request, json, time, requests, os

folder = 'downloaded_reddit_images/'
if not os.path.exists(folder):
        os.makedirs(folder)

url = 'https://www.reddit.com/r/Eyebleach/new.json?sort=new'
with requests.get(url, headers = {'User-agent': 'phils bot heh'}) as req:
    data = req.json()
    posts = data['data']['children']

    for post in posts:
        if post['data']['url'].endswith('.jpg'): # make sure url ends with .jpg
            # str( ...) is used to convert some weird symbols into a proper string
            img_url = str(post['data']['url'])

            title = post['data']['title']
            img_name = title[:32].replace(' ', '_').lower()
            full_img_name = folder + img_name + '.jpg'

            urllib.request.urlretrieve(img_url, full_img_name)
            time.sleep(1)
```

If you run this (`python web_crawler.py`), you will see a folder appear and images
start appearing in it!

## BONUS: Command line arguments
Command line argumennts are essentially parameters which you can pass into a program
from the terminal. Currently, when you are running `python web_crawler.py`, you are
only passing one argument to `web_crawler.py`; its own name! 

The challenge is to modify the code so that you can create a program which takes
4 arguments: its own name, the subreddit to download images from, which sorting
algorithm to use (top, new, hot, etc.), and lastly the folder name to download to.

For example, `python web_crawler_cli.py ProgrammerHumor top programmer_memes` will
download images from the subreddit *Programmerhumor* sorted by the top-ranking posts,
into the folder *programmer_memes*. Good luck! 

## About Dictionaries
Python dictionaries are structured in "key": "value" pairs. For example, if I had
```python
data = {
    "key": "apple"
}
```

"key" would be the key, and "apple" the value. To access the value "apple" and assign it
to the variable `apple`, we would do the following:

```python
apple = data["key"]
```
So what if the value is another dictionary holding multiple keys and values, like:

```python
data = {
    "key_1": {
        "key_2": "apple",
        "key_3": "oranges"
    }
}
```
Well, we can assign "oranges" to `oranges` with the following:
```python
oranges = data["key_1"]["key_3"]
```
