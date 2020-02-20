# *_* coding : UTF-8 *_*
# 开发人员   :  CZW
# 开发时间   :  20/2/18 14:06
# 文件名称   :  bookDownload.py
# 开发工具   :  PyCharm

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import os
import time
from fake_useragent import UserAgent
# import requests

# 获取下载地址和文件名称
def getUrl(url_head):
    ua = UserAgent()
    # 请求头
    headers = {"User-Agent": ua.random}
    # 请求网址
    response = Request(url=url_head, headers=headers)
    print(response.headers)

    html = urlopen(response)
    # html = getHtml(raw_url)
    print('html:', html)
    bsobj = BeautifulSoup(html, 'lxml')
    url_list = bsobj.findAll(name='a', attrs={"href": re.compile('.pdf$')})
    title_list = bsobj.findAll({"h6"})
    # file_url = urlopen(response)
    # response.close()  # 使用urlopen方法太过频繁，会引起远程主机的怀疑
    # print('bsobj:', bsobj)

    # print('title_lst:', title_list)
    return url_list,  title_list


def getFile(url, one_name):
    file_name = url.split('/')[-1]
    u = urlopen(url)
    f = open(file_name, 'wb')

    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break
        f.write(buffer)
    f.close()
    print("原文件下载成功：" + " " + file_name)
    # 新增重命名操作
    # dir1 = 'F:\\DOC\\Project\\2020\\Virus\\pdf_download0\\' + file_name
    # dir2 = 'F:\\DOC\\Project\\2020\\Virus\\pdf_download0\\' + one_name + '.pdf'
    dir1 = file_path + file_name
    dir2 = file_path + one_name + '.pdf'
    if os.path.exists(dir1):
        if os.path.exists(dir2):
            print('%s 文件已存在！' % dir2)
        else:
            os.rename(dir1, dir2)
    else:
        print('%s 下载失败！' % dir1)
    # os.rename(file_name, title)
    print("下载成功：" + " " + one_name + '.pdf')
    time.sleep(30)



if __name__ == '__main__':
    # 下载地址中相同的部分
    # root_url = 'http://bp.pep.com.cn/jc/yjcz'  # 义务教育初中教材下载地址
    root_url = 'http://bp.pep.com.cn/jc/ptgzjks'  # 普通高中教材下载地址
    # 目前版本在下载高中教材的时候会显示远程服务器拒绝
    file_path = 'F:\\DOC\\Project\\2020\\Virus\\pdf_download0\\'
    print('文件保存地址：', file_path)

    # if not os.path.exists('pdf_download0'):  # 文件夹不存在时，再进行创建
    #     os.mkdir('pdf_download0')
    #     print('文件夹pdf_download0新建成功！')
    # os.chdir(os.path.join(os.getcwd(), 'pdf_download0'))
    if not os.path.exists(file_path):  # 文件夹不存在时，再进行创建
        os.mkdir(file_path)
        print('文件夹 %s 新建成功！' % file_path)
    os.chdir(os.path.join(os.getcwd(), file_path))

    url_lst, title_lst = getUrl(root_url)
    # print('url_lst:', url_lst)
    print('获取地址和文件名成功！')
    print('准备开始下载文件！')
    for i in range(len(title_lst)):
        url = re.sub('\A\.', '', url_lst[i].get('href'))  # 获得的下载地址是'./'开头的，需要进行修剪
        url = root_url + url  # 形成完整的下载地址
        title = title_lst[i].get_text()
        print('下载地址：', url)
        getFile(url, title)
        print('共%d本书，已下载%d本' % len(title_lst) % i)
        print('**********开始下载第%d本书**********' % i+1)
    print('全部文件下载完成！')