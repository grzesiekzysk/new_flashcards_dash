import requests
from bs4 import BeautifulSoup
import re
import contextlib
import eng_to_ipa
import pandas as pd

class Diki:
    def __init__(self, lang='english'):
        self.lang = lang
        self.star_dict = {
            '*****': 'TOP 1000',
            '****': 'TOP 2000',
            '***': 'TOP 3000',
            '**': 'TOP 4000',
            '*': 'TOP 5000',
            'OTHER': 'OTHER'
        }
        self.translation_return = {
            'polish_words': [],
            'english_word': None,
            'popularity': None,
            'pronunciation': None,
            'examples': {},
            'other_words': []
        }

    def _bs4_info(self, word):
        langs = {
            "english": "angielskiego",
            "german": "niemieckiego",
            "spanish": 'hiszpanskiego',
            "italian": 'wloskiego',
            "french": 'francuskiego'
        }
        
        result = requests.get(f'https://www.diki.pl/slownik-{langs[self.lang]}?q={word}')
        soup = BeautifulSoup(result.text, 'html.parser')
        self.soup = soup

    def translation(self, word, exact_word = 1):

        polish_words = []
        other_words = []
        examples = {}
        
        r = self._bs4_info(word)

        try:
            stars = self.soup.find('a', {'class': 'starsForNumOccurrences'}).text
        except:
            stars = 'OTHER'

        pronunciation  = '/' + eng_to_ipa.convert(word) + '/'

        div_class = self.soup.find_all('div','dictionaryEntity')

        for div in div_class:
            with contextlib.suppress(AttributeError):
                if exact_word == 1 and div.find("span", {"class": "hw"}).text.strip() == word or exact_word != 1:
                    
                    for m in div.find_all('li', re.compile('^meaning\d+')):

                        part_of_speach = m.find_parent('ol').find_previous_sibling('div').text.strip()
                        
                        for span in m.find_all('span', 'hw'):
                            polish_word = re.sub(r'\s+', ' ', span.text).strip()
                            # If word not exist in list
                            if polish_word not in [i[0] for i in polish_words]:
                                polish_words.append([polish_word, part_of_speach])
                        
                        for m in m.find_all('div', 'exampleSentence'):
                            example = re.sub(r'\s+', ' ', m.text).strip()
                            examples[polish_word] = example
                else:
                    other_words.append(div.find("span", {"class": "hw"}).text.strip())

        self.translation_return['polish_words'] = polish_words
        self.translation_return['english_word'] = word
        self.translation_return['popularity'] = self.star_dict[stars]
        self.translation_return['pronunciation'] = pronunciation
        self.translation_return['examples'] = examples
        self.translation_return['other_words'] = other_words
        
        return self.translation_return