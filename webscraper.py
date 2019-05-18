# Python addon to browse collections of subreddits as a bookmark
from bs4 import BeautifulSoup
import requests 

class Page:
    def __init__(self, link = None):
        if not link: link = input('Enter site link: ')
        if link[0] in "\'\"" and link[-1] in "\'\"": link = link[1:-1]
        
        self.link = link
        self.response = requests.get(self.link, 'html.parser')
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.title = self.soup.title.text

    # count the tags
    def tagCount(self, tag, attrs = None):
        return len(self.soup.find_all(tag, attrs))

    # returns an array of all the mainly relevant text on the site.
    @property
    def textArray(self):
        # to check website type. Later, I plan to have a dictionary for more websites and their text identifiers.
        tag, identifier = ('p', None) if not 'cnn' in self.link else ('div', {"class": "zn-body__paragraph"})
        return [self.soup.find_all(tag, identifier)[i].text for i in range(self.tagCount(tag, identifier))]

# Reads a file's words and inserts them into a dictionary with a
# key: value association of word: number of occurrences. 
def createMap(textArray):
    para = ' '.join(textArray).lower()
    bare_para = list(c if any((c.isalnum(), c.isspace(), c == "'")) else ' ' for c in para.split())

    hashMap = {}
    for w in set(bare_para):
        hashMap[w] = bare_para.count(w)
    return hashMap

# This function calculates the jaccard index, used commonly to find similarity.
def jaccard(set1, set2):
    return 100*len(set1 & set2)/len(set1 | set2)

# Take user input and determine the web pages' similarity to each other. If the similarity is greater than 50%, then
# the articles can be concluded to be significantly similar according to the Jaccard index.
def main():
    page1 = Page()
    print('\nYour first article to compare: ' + page1.title + '\n\nNow enter the second page.\n')
    page2 = Page()
    print('\nYour second article for comparison: ' + page2.title)
    p1Map, p2Map = createMap(page1.textArray), createMap(page2.textArray)
    print('\nProceeding to compare...')
    similarity = jaccard(set(p1Map), set(p2Map))
    print('\nThe articles are {:.2f}{} similar.'.format(similarity,'%'))
    print('According to the Jaccard index, these articles are {}significantly similar.'.format(('', 'not ')[similarity < 50]))

if __name__ == '__main__':
    main()
