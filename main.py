import collections

import requests
from pprint import pprint
from bs4 import BeautifulSoup


def extract_lyrics(url):
    r = requests.get(url)
    if r.status_code != 200:
        print("Page impossible à récupérer")
        return []
    soup = BeautifulSoup(r.content, 'html.parser')
    #print(r.content)
    lyrics = soup.find("div", class_="SongPageGriddesktop-sc-1px5b71-0 Lyrics__Root-sc-1ynbvzw-1 giibkh")
    #print(type(lyrics))
    #print(lyrics)

    all_words = []
    for sentence in lyrics.stripped_strings:
        sentence_word = [word.strip(",").strip(".").lower() for word in sentence.split() if len(word) > 2]
        all_words.extend(sentence_word)
    pprint(all_words)

    counter = collections.Counter(all_words)
    print(counter.most_common(10))


#Ce sont les classes des div que j'ai essayé
    #Lyrics__Container-sc-1ynbvzw-6 YYrds
    #InreadContainer__Container-sc-19040w5-0 cujBpY PrimisPlayer__InreadContainer-sc-1tvdtf7-0 juOVWZ
    #InreadContainer__Container-sc-19040w5-0 cujBpY PrimisPlayer__InreadContainer-sc-1tvdtf7-0 juOVWZ
    #PrimisPlayer__Container-sc-1tvdtf7-1 csMTdh
def get_all_urls():
    page_number = 1
    links = []
    while True:
        r = requests.get(f"https://genius.com/api/artists/29743/songs?page={page_number}&sort=popularity")
        if r.status_code == 200:
            response = r.json().get("response", {})
            next_page = response.get("next_page")

            songs = response.get("songs")

            all_song_links = [song.get("url") for song in songs]
            links.extend(all_song_links)

            page_number += 1

            if not next_page:
                print("No more page to fetch ...")
                break
    pprint(links)
    print(len(links))
get_all_urls()

extract_lyrics(url="https://genius.com/Patrick-bruel-elle-mregardait-comme-ca-lyrics")

