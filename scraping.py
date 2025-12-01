import requests as re
from bs4 import BeautifulSoup

def scrape_movie_info(slug: str) -> dict[int, tuple[str, tuple[str]]]:
    page = "page_1.html"
    movie_info = {}
    while page != "":
        url = slug + page
        response = re.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all('tr')[1:]
        for row in rows:
            id = int(row.find('td', class_ = "movie_id").text.strip())
            title = row.find('td', class_ = "movie_title").text.strip()
            pure_title = title.split("(")[0].strip()
            genres = row.find('td', class_ = "genres").text.strip()
            genre_tuple = tuple(g.strip() for g in genres.split(','))
            movie_info[id] = (pure_title, genre_tuple)
        button = soup.find('button', {"aria-label": "Next page"})
        next_page = button.find('a')["href"]
        page = next_page
    return movie_info
def scrape_ratings(
    slug: str, movie_ids: set[int]
) -> dict[int, dict[int, float]]:
    rating_dict = {}
    for id in movie_ids:
        url = f"{slug}ratings_{id}.html"
        response = re.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all("tr")[1:]
        for r in rows:
            user = int(r.find("td", class_ = "user_id").text.strip())
            rating = float(r.find("td", class_ = "rating").text.strip())
            if user not in rating_dict:
                rating_dict[user] = {}
            rating_dict[user][id] = rating
    return rating_dict