from pyppeteer import launch
import asyncio
from bs4 import BeautifulSoup
from creating_database import create_table, insert_data, get_info_by_title


async def get_info_from_page():
    for i in range(1, 301):
        url = f"https://www.eatthismuch.com/food/browse/?q=&type=recipe&page={i}"
        browser = await launch({"headless": False})
        page = await browser.newPage()
        await page.goto(url, {"waitUntil": "domcontentloaded"})

        html = await page.content()
        with open("content.html", "w", encoding="UTF-8") as file:
            file.write(html)

        with open("content.html", encoding="UTF-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, "lxml")
        elements = soup.find_all("div", class_="row food_result")
        for element in elements:
            link = element.find("a", class_="row").get("href")

            image_link = element.find("div", class_="search_result_image col-1").find("img").get("src").replace("thmb", "img")

            title = element.find("div", class_="result_name col-3").text.strip()

            count_calories = element.find("div", class_="row result_stats").find("div", class_="col-2 offset-1 nutrient_cell").text.strip()
            count_carbs = element.find("div", class_="row result_stats").find_all("div", class_="col-2 nutrient_cell")[0].text.strip().replace(' ', '').replace("\n", '')
            count_fat = element.find("div", class_="row result_stats").find_all("div", class_="col-2 nutrient_cell")[1].text.strip().replace(' ', '').replace("\n", '')
            count_protein = element.find("div", class_="row result_stats").find_all("div", class_="col-2 nutrient_cell")[2].text.strip().replace(' ', '').replace("\n", '')

            insert_data(image_link, title, count_calories, count_carbs, count_fat, count_protein, link)
        await page.close()
        await browser.close()
