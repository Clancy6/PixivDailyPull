import requests
import re
import os

headers = {
    'user-agent': 'Mozilla/8.0 (Windows NT 10.0; Win64; x64; x128; iKun OS) AppleWebKit/884.8 (KHTML, like Gecko) Chrome/99.9.1145.14 Safari/666.66',
    'referer': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
}

path = './'
repeat = 1
repeat_user_name = 1


def getSinglePic(url):
    global repeat
    global repeat_user_name
    response = requests.get(url, headers=headers)
    print("response:\n",str(response))
    #if re.search('"xRestrict":(.+?),"sl"', response.text).group() != '"xRestrict":0,"sl"':
    if re.search('"xRestrict":(.+?),"sl"', response.text).group() != '"xRestrict":0,"sl"' or re.search('"original":(.+?),', response.text).group() == '"original":null},':#Thinks to:https://github.com/No5972/pixiv-github-action/issues/4#event-8129779417
        return False
    # 提取图片名称
    name = re.search('"illustTitle":"(.+?)"', response.text)
    name = name.group(1)
    illust_id = re.search('"illustId":"(.+?)"', response.text)
    illust_id = illust_id.group(1)
    user_name = re.search('"userName":"(.+?)"', response.text)
    user_name = user_name.group(1)
    if re.search('[\\\ \/ \* \? \" \: \< \> \|]', name) != None:
        name = re.sub('[\\\ \/ \* \? \" \: \< \> \|]', str(repeat), name)
        repeat += 1
    if re.search('[\\\ \/ \* \? \" \: \< \> \|]', user_name) != None:
        user_name = re.sub('[\\\ \/ \* \? \" \: \< \> \|]', str(repeat_user_name), user_name)
        repeat_user_name += 1
    # 提取图片原图地址
    picture = re.search('"original":"(.+?)"},"tags"', response.text)
    pic = requests.get(picture.group(1), headers=headers)
    img_name = path + '%s_%s-by-%s.%s' % (illust_id, name, user_name, picture.group(1)[-3:])# https://github.com/Clancy6/PixivDailyPull/issues/1
    img_name = img_name.replace('?','？')
    img_name = img_name.replace('#','%23')
    with open(img_name, 'wb+') as f:#优化文件写入方法
        f.write(pic.content)
    with open('pid.data', 'a') as f:#保存图片id
        f.write(illust_id+'\n')
    return True

def getAllPicUrl():
    count = 1
    for n in range(1, 5):
        url = 'https://www.pixiv.net/ranking.php?mode=daily&content=illust&p=%d&format=json' % n
        response = requests.get(url, headers=headers)
        illust_id = re.findall('"illust_id":(\d+?),', response.text)
        picUrl = ['https://www.pixiv.net/artworks/' + i for i in illust_id]
        for url in picUrl:
            print('Downloading the picture %d ' % count, end='   ')
            print('OK' if getSinglePic(url) else "FAILED", end='\n')
            count += 1
    os.system("ls -al")
    return None

getAllPicUrl()
