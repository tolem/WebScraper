import requests
from bs4 import BeautifulSoup
import string
import os


def scrape_url(n_page,a_type):
    if int(n_page) and a_type != "":
        page_link = "https://www.nature.com/nature/articles?sort=PubDate&year=2020"

        def find_page(num,page):
            resp = requests.get(f"{page}&page={num}")
            return resp
        for i in range(1, n_page+1):
            page_resp = find_page(i,page_link)
            directory = i
            os.mkdir(f"Page_{directory}")
            if page_resp.status_code == 200:
                page_content = page_resp.content
                soup = BeautifulSoup(page_content, 'html.parser')
                articles_list = soup.find_all('article')
                articles_links = soup.find_all('a', {'data-track-action': 'view article'})
                for idx, news in enumerate(articles_list):
                    if news.find_all(string=a_type):
                        article_link = articles_links[idx].get('href')
                        news_link = requests.get(f" https://www.nature.com{article_link}")
                        soup2 = BeautifulSoup(news_link.content, 'html.parser')
                        article_body = soup2.find("div", {"class": "c-article-body u-clearfix"})
                        title = articles_links[idx].text
                        title = "".join([s for s in str(title) if s not in string.punctuation]).replace(" ", "_")
                        body = article_body.text

                        with open(f"Page_{directory}/{title}.txt", mode="wb") as file:
                            file.write(body.encode())
        return "Saved all articles."
    return ""


if __name__ == "__main__":
    # user_url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=3"
    num_page = int(input())
    article_type = input()
    print(scrape_url(num_page, article_type))


