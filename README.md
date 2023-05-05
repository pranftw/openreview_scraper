# OpenReview Scraper
Scrape papers from top conferences like ICML, ICLR, NeurIPS, etc using OpenReview API, by searching for specific keywords in title, abstract or keywords in the submissions and save them to a CSV file.<br>
Brings down the time taken to gather papers from several hours to a few minutes through automation

## Installation
```python
git clone https://github.com/pranftw/openreview_scraper.git # clone repo
python -m venv venv # create virtual environment
source venv/bin/activate # activate virtual environment
pip install -r requirements.txt # install requirements
cp config.py.example config.py # enter your OpenReview credentials in config.py
```

## Example
```python
from scraper import Scraper
from extract import Extractor
from filters import title_filter, keywords_filter, abstract_filter
from selector import Selector
from utils import save_papers, load_papers


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

# what fields to extract
extractor = Extractor(fields=['forum'], subfields={'content':['title', 'keywords', 'abstract', 'pdf', 'match']})

# if you want to select papers manually among the scraped papers
# selector = Selector()

# select all scraped papers
selector = None

scraper = Scraper(conferences=conferences, years=years, keywords=keywords, extractor=extractor, fpath='example.csv', fns=[modify_paper], selector=selector)

# adding filters to filter on
scraper.add_filter(title_filter)
scraper.add_filter(keywords_filter)
scraper.add_filter(abstract_filter)

scraper()

# if you want to save scraped papers as OpenReview objects using pickle
save_papers(scraper.papers, fpath='papers.pkl')
saved_papers = load_papers(fpath='papers.pkl')
```
