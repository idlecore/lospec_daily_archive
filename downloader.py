from datetime import date
import os
import requests
from bs4 import BeautifulSoup
import git

BASE_URL = "https://lospec.com"
TODAY = date.today().strftime("%Y-%m-%d")


def create_folder():
    folder_name = TODAY
    folder_path = os.path.join(os.getcwd(), folder_name)

    if not os.path.exists(folder_path):
        # This should panic if it fails
        os.mkdir(folder_path)

    return folder_path


def parse_website():
    r = requests.get(BASE_URL + "/dailies/", timeout=1)
    soup = BeautifulSoup(r.text, 'html.parser')

    topic = soup.find("div", class_="daily tag").get_text().strip("#")

    palette = soup.find("div", class_="daily palette")\
                  .find("p").find_all("a")[1]['href']

    return (topic, palette)


def download_palette(folder, url):
    file_name = url.split('/')[-1]
    p = requests.get(BASE_URL + url)
    with open(os.path.join(folder, file_name), 'wb') as f:
        f.write(p.content)


def touch(path):
    open(path, 'w+').close()


def commit_and_push(folder, topic):
    repo = git.Repo(".")
    repo.index.add(folder)
    repo.index.commit("Add {}".format(topic))
    repo.remote(name='origin').push()


if __name__ == "__main__":
    folder = ""
    topic = ""
    try:
        folder = create_folder()
        (topic, palette) = parse_website()
        touch(os.path.join(folder, topic))

        download_palette(folder, palette)
    except e:
        print(e)
        exit(1)
    else:
        commit_and_push(folder, topic)
