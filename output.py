from bs4 import BeautifulSoup

def insert(gather):
    f = open("model.html", "r", encoding="utf-8")
    soup = BeautifulSoup(f, "html.parser")
    page = soup.find("div", class_="page")
    for word in gather:
        if word is not None:
            element = soup.new_tag("div")
            element.attrs = {"class": "elements"}
            h1 = soup.new_tag("h1")
            h1.append(word[0])
            del word[0]
            element.append(h1)
            for content in word:
                p = soup.new_tag("p")
                p.append(content)
                element.append(p)
            page.append(element)
    f.close()

    w_f = open("display.html", "w", encoding="utf-8")
    w_f.write(soup.prettify())
    w_f.close()


if __name__ == "__main__":
    test = [["Title", "p11111", "p22222"], ["Title", "p23333", "p34444"]]
    insert(test)


