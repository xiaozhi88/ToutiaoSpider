# https://www.toutiao.com/search_content/?offset=0&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab
# https://www.toutiao.com/search_content/?offset=20&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab
# https://www.toutiao.com/search_content/?offset=40&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab

'''
今日头条抓取'街拍'图片并按文件夹保存
'''

import requests
import os
from hashlib import md5
from multiprocessing.pool import Pool


def get_page(offset):
    '''
    获取响应数据
    :param offset: 偏移量
    :return: 返回json格式的数据
    '''
    url_set = 'https://www.toutiao.com/search_content/?offset={}&format=json&keyword=%E8%A1%97%E6%8B%8D&autoload=true&count=20&cur_tab=1&from=search_tab'
    url = url_set.format(offset)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_image(json):
    '''
    解析json数据
    :param json: json数据
    :return: 获取图片及标题
    '''
    if json.get('data'):
        for item in json.get('data'):
            if item.get('title') and item.get('image_list'):
                title = item.get('title')
                images = item.get('image_list')
                for image in images:
                    yield {
                        'title': title,
                        'image': image.get('url')
                    }


# http://p9.pstatp.com/list/pgc-image/1533521917134c5c689eca4

def save_image(item):
    '''
    保存图片
    :param item: 图片数据
    :return: 图片保存
    '''
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        response = requests.get('http:' + item.get('image'))
        # response = item.get('image')
        if response.status_code == 200:
            file_path = '{}/{}.{}'.format(item.get('title'), md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('已经下载', file_path)
    except requests.ConnectionError:
        print('保存失败')


def main(offset):
    json = get_page(offset)
    items = get_image(json)
    for item in items:
        save_image(item)
        print(item)


if __name__ == '__main__':
    #使用进程池进行多进程执行任务
    pool = Pool()
    groups = ([x * 20 for x in range(1, 5)])
    # for i in range(5):
    #     main(offset=i*20)
    pool.map(main, groups)
    pool.close()
    pool.join()
