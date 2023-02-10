# Paper Scraper
Scrape papers from top conferences like ICML, ICLR, NeurIPS, etc using OpenReview API based on searching for specific keywords in title, abstract or keywords in the submissions and save them to a CSV file.

## Installation
```python
git clone https://github.com/pranftw/paper_scraper.git # clone repo
python -m venv venv # create virtual environment
source venv/bin/activate # activate virtual environment
pip install -r requirements.txt # install requirements
cp config.py.example config.py # enter your OpenReview credentials here
```

## Example
```python
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
```