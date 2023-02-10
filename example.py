from scraper import Scraper
from extract import Extractor
from filters import title_filter, keywords_filter, abstract_filter


years = [
    '2023',
    '2022',
    '2021'
]
conferences = [
    'NeurIPS'
]
keywords = [
    'generalization'
]

def modify_paper(paper):
  paper.forum = f"https://openreview.net/forum?id={paper.forum}"
  paper.content['pdf'] = f"https://openreview.net{paper.content['pdf']}"
  return paper

extractor = Extractor(fields=['forum'], subfields={'content':['title', 'keywords', 'abstract', 'pdf', 'match']})
scraper = Scraper(conferences=conferences, years=years, keywords=keywords, extractor=extractor, fpath='example.csv', fns=[modify_paper])

scraper.add_filter(title_filter)
scraper.add_filter(keywords_filter)
scraper.add_filter(abstract_filter)

scraper.execute()