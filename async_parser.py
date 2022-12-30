import asyncio
import aiohttp
import aiofiles
import unicodedata

from bs4 import BeautifulSoup
from datetime import datetime


report_date = datetime.now().strftime("%d_%m_%Y")


async def fetch_page(url):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers=headers)
        return await response.text()


async def parse_site(url):
    soup = BeautifulSoup(await fetch_page(url), "lxml")

    book_data = {}

    book_data["name"] = soup.find(
        "div", attrs={"class": "biblio_book_name"}
    ).find("h1", attrs={"itemprop": "name"}).text

    authors = soup.find("div", attrs={"class": "biblio_book_author"})
    book_data["authors"] = ", ".join(
        [
            name.text for name in authors.find_all("span", attrs={"itemprop": "name"})
        ]
    )

    book_data["price"] = unicodedata.normalize('NFKC', soup.find(
        "div",
        attrs={"class": "biblio_book_buy_block"}
    ).find(
        "span",
        attrs={"class": "simple-price"}
    ).text)

    await write_report(book_data)


async def write_report(book_data):
    async with aiofiles.open(f"parsing_report_{report_date}.csv", "a+") as f:
        await f.write(
            f"{book_data['name']};{book_data['authors']};{book_data['price']}\n"
        )


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()

    with open('source.txt', 'r') as f:
        tasks = [
            event_loop.create_task(parse_site(url.strip('\n')))
            for url in f
        ]
    wait_tasks = asyncio.wait(tasks)

    event_loop.run_until_complete(wait_tasks)
    event_loop.close()
