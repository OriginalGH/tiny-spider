import re
import urllib.request
import spider.baidu_baike.output as output
from bs4 import BeautifulSoup

# 获取url网页内容
def get_web(url):
    response = urllib.request.urlopen(url)
    if response.getcode() == 200:
        html_content = response.read().decode()
        return html_content
    print("获取网页内容失败！")
    return None

# 分析网页内容，返回标题和内容, 收集相关url
def analysis_web(html_content):
    gather = list()  # 保存标题和内容
    soup = BeautifulSoup(html_content, "html.parser")

    dd_tag = soup.find("dd", class_="lemmaWgt-lemmaTitle-title")
    if dd_tag is not None:
        h1_tag = dd_tag.find("h1")
        gather.append(h1_tag.text)
        summary_tag = soup.find("div", class_="lemma-summary")
        if summary_tag is not None:
            para_tags = summary_tag.find_all("div", class_="para")
            if para_tags is not None:
                for para in para_tags:
                    gather.append(para.text)
                    a_urls = para.find_all("a", href=re.compile(r"/item/.+"))
                    for a in a_urls:
                        url = "https://baike.baidu.com" + a["href"]
                        if url not in got_url:
                            ready_url.add(url)

    return gather


if __name__ == "__main__":
    count = 0
    got_url = set()
    ready_url = set()
    result = list()
    ready_url.add("https://baike.baidu.com/item/Python/407313")
    while len(ready_url) != 0:
        count += 1
        if count > 10:
            break
        baike_url = ready_url.pop()
        content = get_web(baike_url)
        if content is not None:
            result.append(analysis_web(content))
        print("剩余未抓取url：", len(ready_url), " 当前url：" + baike_url)
        got_url.add(baike_url)

    output.insert(result)

