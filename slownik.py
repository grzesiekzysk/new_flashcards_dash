import requests
from bs4 import BeautifulSoup
import re
import contextlib

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
            'english_word': None,
            'popularity': None,
            'polish_words': [],
            'examples': {},
            'synonyms': {},
            'opposites': [],
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

    def translation(self, word):

        polish_words = []
        other_words = []
        examples = {}
        synonyms = {}
        opposites = set()
        
        r = self._bs4_info(word)

        try:
            stars = self.soup.find('a', {'class': 'starsForNumOccurrences'}).text
        except:
            stars = 'OTHER'

        div_class = self.soup.find_all('div','dictionaryEntity')

        for div in div_class:
            with contextlib.suppress(AttributeError):
                if div.find("span", {"class": "hw"}).text.strip() == word:
                    
                    for m in div.find_all('li', re.compile('^meaning\d+')):

                        part_of_speach = m.find_parent('ol').find_previous_sibling('div').text.strip()
                        polish_word = ', '.join([re.sub(r'\s+', ' ', span.text).strip() for span in m.find_all('span', 'hw')])
                        polish_words.append([polish_word, part_of_speach])
                        
                        for n in m.find_all('div', 'exampleSentence'):
                            example = re.sub(r'\s+', ' ', n.text).strip()
                            examples[polish_word] = example

                        divs_syn  = m.find_all('div')

                        for div_syn in divs_syn:
                            if 'synonim' in div_syn.get_text():
                                link_s = div_syn.find('a')
                                if link_s:
                                    synonyms[polish_word] = link_s.get_text()

                            if 'przeciwieństwo' in div_syn.get_text() and 'synonim' not in div_syn.get_text():
                                link_o = div_syn.find('a')
                                if link_o:
                                    opposites.add(link_o.get_text())
                else:
                    other_words.append(div.find("span", {"class": "hw"}).text.strip())
        
        self.translation_return['english_word'] = word
        self.translation_return['popularity'] = self.star_dict[stars]
        self.translation_return['polish_words'] = polish_words
        self.translation_return['examples'] = examples
        self.translation_return['other_words'] = other_words
        self.translation_return['synonyms'] = synonyms
        self.translation_return['opposites'] = list(opposites)
        
        return self.translation_return