import sys

import requests
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self, url):
        self.datasets = []
        self.url = url

    def scrap_url(self):
        request = requests.get(self.url)
        html = request.content
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")

        headings = [th.get_text().strip() for th in table.find("tr").find_all("th")]

        for row in table.find_all("tr")[1:]:
            dataset = dict(zip(headings, (td.get_text() for td in row.find_all("td"))))
            self.datasets.append(dataset)

    def search_mode(self, mode):
        for data in self.datasets:
            try:
                if int(mode) == int(data["Hash-Mode"]):
                    print(
                        "{:<8} | {:20} | {} ".format(
                            data["Hash-Mode"], data["Hash-Name"], data["Example"]
                        )
                    )
                    break
            except ValueError:
                print("Mode must be intiger!")
                break

    def search_name(self, name):
        for data in self.datasets:
            if name.lower() in data["Hash-Name"].lower():
                print(
                    "{:<8} | {:20} | {} ".format(
                        data["Hash-Mode"], data["Hash-Name"], data["Example"]
                    )
                )

    def print_table(self):
        print("{:<8} | {:<50} | {} ".format("Hash-Mode", "Hash-Name", "Example"))
        for data in self.datasets:
            print(
                "{:<8} | {:50} | {} ".format(
                    data["Hash-Mode"], data["Hash-Name"], data["Example"]
                )
            )

    def run(self):
        self.scrap_url()
        print("0. Exit")
        print("1. Search mode")
        print("2. Search name")
        print("3. Print database")
        while True:
            user_input = input(">>> ")
            if user_input == "0":
                sys.exit()
            elif user_input == "1":
                mode = input("Enter mode to search: ")
                self.search_mode(mode)
            elif user_input == "2":
                name = input("Enter name to search: ")
                self.search_name(name)
            elif user_input == "3":
                self.print_table()
            else:
                print("[-] Invalid option.")


if __name__ == "__main__":
    HASHCAT_URL = "https://hashcat.net/wiki/doku.php?id=example_hashes"
    scrap = Scraper(HASHCAT_URL)
    scrap.run()
