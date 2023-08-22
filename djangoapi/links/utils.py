import requests
from bs4 import BeautifulSoup
import httpx

# def fetch_open_graph_data(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                       'Chrome/91.0.4472.124 Safari/537.36'
#     }
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, 'html.parser')
#
#     og_title = soup.find("meta", property="og:title")
#     og_description = soup.find("meta", property="og:description")
#     og_image = soup.find("meta", property="og:image")
#     og_type = soup.find("meta", property="og:type")
#
#     title = og_title["content"] if og_title else soup.title.string
#     description = og_description["content"] if og_description else \
#         soup.find("meta", attrs={"name": "description"})["content"]
#     image = og_image["content"] if og_image else None
#     type = og_type["content"] if og_type else "website"
#
#     return {
#         "title": title,
#         "description":description,
#         "image": image,
#         "type": type
#     }


async def fetch_open_graph_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

    soup = BeautifulSoup(response.content, 'html.parser')

    og_title = soup.find("meta", property="og:title")
    og_description = soup.find("meta", property="og:description")
    og_image = soup.find("meta", property="og:image")
    og_type = soup.find("meta", property="og:type")

    title = og_title["content"] if og_title else soup.title.string
    description = og_description["content"] if og_description else \
        soup.find("meta", attrs={"name": "description"})["content"]
    image = og_image["content"] if og_image else None
    type = og_type["content"] if og_type else "website"

    return {
        "title": title,
        "description": description,
        "image": image,
        "type": type
    }