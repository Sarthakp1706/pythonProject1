import requests
from bs4 import BeautifulSoup
import csv

csv_file = open("amazon_products.csv", "r", encoding="utf-8")
csv_reader = csv.reader(csv_file)
next(csv_reader)  # Skip the header row

csv_file_details = open("amazon_product_details.csv", "w", newline="", encoding="utf-8")
csv_writer_details = csv.writer(csv_file_details)
csv_writer_details.writerow(["Product URL", "Description", "ASIN", "Product Description", "Manufacturer"])

counter = 0
for row in csv_reader:
    if counter >= 200:
        break

    product_url = row[0]
    if not product_url.startswith("http"):
        product_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1" + product_url

    try:
        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, "html.parser")

        feature_bullets = soup.find("div", id="feature-bullets")
        if feature_bullets:
            description = feature_bullets.text.strip()
        else:
            description = ""

        asin_element = soup.find("div", {"data-asin": True})
        if asin_element:
            asin = asin_element.get("data-asin")
        else:
            asin = ""

        product_desc_element = soup.find("div", id="productDescription")
        if product_desc_element:
            product_desc = product_desc_element.text.strip()
        else:
            product_desc = ""

        manufacturer_element = soup.find("a", id="bylineInfo")
        if manufacturer_element:
            manufacturer = manufacturer_element.text.strip()
        else:
            manufacturer = ""

        csv_writer_details.writerow([product_url, description, asin, product_desc, manufacturer])

        counter += 1
    except requests.exceptions.MissingSchema as e:
        print(f"Skipping URL: {product_url}. Error: {e}")
        continue

csv_file.close()
csv_file_details.close()