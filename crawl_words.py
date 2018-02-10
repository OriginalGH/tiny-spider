import re
import time
import threading
import urllib.request
import spider.baidu_baike.output as output
from bs4 import BeautifulSoup

# 获取url网页内容
def get_web(num):
    global count
    while count < num and len(ready_url) > 0:
        # 爬取下一条 url
        lock.acquire()  # 上锁, acquire()和 release()之间的语句一次只能有一个线程进入，其余线程在acquire()处等待
        url = ready_url.pop()
        got_url.add(url)
        count += 1
        lock.release()  # 解锁

        # 设置代理 IP, 请求网址时会调用网址对应的传输协议 所对应的代理 IP
        proxy = urllib.request.ProxyHandler({'http': '121.237.141.217:808', 'https': '119.28.152.208:80'})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)

        # 设置请求头信息 headers, 还可以添加要提交数据 data等等
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            html_content = response.read().decode()
            if html_content is not None:
                lock.acquire()
                # 打印剩余未抓取的 url个数 和 当前 url地址
                print("剩余未抓取url:", len(ready_url), " 当前url：" + url)
                # 分析网页内容，提取想要的内容，添加到 result列表中
                result.append(analysis_web(html_content))
                lock.release()
        else:
            print("获取网页内容失败！url:", url)
        response.close()

# 分析网页内容，返回标题和内容, 收集相关url
def analysis_web(html_content):
    gather = list()  # 保存标题和每一段内容
    soup = BeautifulSoup(html_content, "html.parser")

    dd_tag = soup.find("dd", class_="lemmaWgt-lemmaTitle-title")
    if dd_tag is not None:
        h1_tag = dd_tag.find("h1")
        gather.append(h1_tag.text)  # 保存词条标题
        summary_tag = soup.find("div", class_="lemma-summary")
        if summary_tag is not None:
            para_tags = summary_tag.find_all("div", class_="para")
            if para_tags is not None:
                for para in para_tags:
                    gather.append(para.text)  # 保存词条介绍的每一段内容
                    a_urls = para.find_all("a", href=re.compile(r"/item/.+"))
                    for a in a_urls:
                        url = "https://baike.baidu.com" + a["href"]  # 拼接 url
                        if url not in got_url:
                            ready_url.add(url)  # 将相关的 url保存到 ready_url列表中

    return gather


if __name__ == "__main__":
    start_t = time.time()

    # 创建 可重入锁
    lock = threading.RLock()

    # 创建全局变量
    got_url = set()
    ready_url = set()
    result = list()
    threads = list()

    # 添加初始 url地址
    ready_url.add("https://baike.baidu.com/item/Python/407313")

    # 统计已爬取的 url的个数
    count = 0

    # 先爬取初始 url，获取相关的 url保存到 ready_url列表中
    get_web(1)

    # 创建7个线程
    for n in range(7):
        # 创建一个新线程，目标函数target, 参数列表args
        threads.append(threading.Thread(target=get_web, args=[100]))
        threads[n].start()

    # 挂起程序，直到所有线程都执行完
    for t in threads:
        t.join()

    # 将 result列表中的所以内容输出到 html页面
    output.insert(result)

    end_t = time.time()
    print(end_t - start_t)
