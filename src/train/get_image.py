import pathlib
import re
import requests
import traceback


image_dir = pathlib.Path(__file__).parent.joinpath('neg')
image_dir.mkdir(exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
search_word = '图库'
num = 0
for i in range(500):
    url = f'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={search_word}&pn=' + str(i*30)
    res = requests.get(url, headers=headers)
    image_urls = re.findall('"objURL":"(.*?)",', res.text)
    for image_url in image_urls:
        num += 1
        print(f'Start to download {url}')
        try:
            image = requests.get(image_url)
        except requests.exceptions.RequestException as e:
            print(f'Failed to download image {num}, url: {image_url}')
            traceback.print_exc()
            continue
        with open(str(image_dir.joinpath(f'{num}.jpg')), 'ab') as f:
            f.write(image.content)
print('Done')


if __name__ == '__main__':
    pass
