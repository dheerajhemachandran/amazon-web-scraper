
# part1


from bs4 import BeautifulSoup
import requests
import csv


def csv_write(result_arr):

    with open("result.csv", "a", encoding="utf-8",) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(result_arr)
        print(result_arr)
        print()


def page_scraper(search_item, page):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
    }
    html_text = requests.get(
        f"https://www.amazon.in/s?k={search_item}&page={page}&crid=2M096C61O4MLT&qid=1658557531&sprefix=ba%2Caps%2C283&ref=sr_pg_2", headers=headers).text
    soup = BeautifulSoup(html_text, "lxml")
    results = soup.find_all('div', class_="s-asin")

    for result in results:

        if("AdHolder" not in result['class']):
            url = ("amazon.in" +
                   result.find('a', class_="s-no-outline")['href'])
            result_arr.append(url)
            result_arr.append(result.find('h2', class_="a-size-mini").text)
            result_arr.append(result.find('span', class_="a-price-whole").text)

            rating = result.find('div', class_="a-size-small")
            if(rating == None):
                result_arr.append("rating not found!!try running again")
            else:
                result_arr.append(rating.find('span')['aria-label'])

            review = result.find('span', class_="a-size-base")
            if(rating == None):
                result_arr.append("review not found!!try running again")
            else:
                result_arr.append(review.text)

            item_scraper(url, headers)
            result_arr.clear()


# part2


def item_scraper(url, headers):
    html_text = requests.get(f"https://{url}", headers=headers).text
    soup = BeautifulSoup(html_text, "lxml")
    discriptions = soup.find(id="feature-bullets").find('ul').find_all('li')
    disc_arr = []
    for disc in discriptions:
        disc_arr.append(disc.find('span').text)
    result_arr.append(disc_arr)

    asin = (soup.find(id="averageCustomerReviews"))
    if (asin != None):
        result_arr.append(asin["data-asin"])
    else:

        result_arr.append("not found")

    seller = soup.find(id="sellerProfileTriggerId")
    if(seller == None):
        result_arr.append(soup.find(id="bylineInfo").text)
    else:
        result_arr.append(seller.text)

    csv_write(result_arr)


search_item = "bags"
pages = 20
result_arr = []
with open("result.csv", "w", encoding="utf-8", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Product url", "Product name", "Price", "Rating",
                     "Number of Reviews", "Product Discription", "ASIN", "Manufacturer"]
                    )


for page in range(pages):
    page_scraper(search_item, str(page+1))
    print()
