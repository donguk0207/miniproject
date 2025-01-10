import requests
from bs4 import BeautifulSoup

def get_naver_news_with_time(query="속보"):
    base_url = "https://search.naver.com/search.naver"
    params = {
        "where": "news",
        "query": query,
        "sort": "1",       # 최신순 정렬
        "sm": "tab_smr",   # 검색 모드 간소화
        "nso": "so:dd,p:all,a:all"  # 최신순 및 모든 기간
    }

    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")
    news_items = []

    # 뉴스 제목, 링크 및 시간 정보 가져오기
    for item in soup.select(".news_area"):
        title_tag = item.select_one(".news_tit")
        info_tag = item.select_one(".info_group > span")

        if title_tag and info_tag:
            title = title_tag.get("title")  # 뉴스 제목
            link = title_tag.get("href")   # 뉴스 링크
            time = info_tag.get_text()     # ~분 전 정보

            news_page = requests.get(link)
            news_soup = BeautifulSoup(news_page.text, "html.parser")
#            print(news_soup)
#            content_tag = news_soup.select_one(".div.news_contents > div > div > a")
#요기 본문은 굳이 수집을해야하나 말아야하나 고민하다가 집감
#            content = content_tag.get_text() if content_tag else "본문을 불러올 수 없습니다."

            news_items.append({
                "title": title,
                "link": link,
                "time": time,
 #               "content": content
            })

    return news_items

get_naver_news_with_time()