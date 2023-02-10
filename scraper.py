from utils import get_client
from venue import get_venues, group_venues
from paper import get_papers
from filter import apply_filters


class Scraper:
  def __init__(self, conferences, years, keywords, groups=['conference', 'workshop'], only_accepted=True):
    self.confs = conferences
    self.years = years
    self.keywords = keywords
    self.groups = groups
    self.only_accepted = only_accepted
    self.filters = []
    self.client = get_client()
  
  def execute(self):
    venues = get_venues(self.client, self.confs)
    papers = get_papers(self.client, group_venues(venues, self.groups), self.only_accepted)
    filtered_papers = apply_filters(papers, self.filters)

  def add_filter(self, filter_, *args, **kwargs):
    self.filters.append((filter_, args, kwargs))