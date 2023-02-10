from utils import get_client
from venue import get_venues, group_venues
from paper import get_papers


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
    filtered_papers = self.apply_filters(papers)
  
  def apply_filters(self, papers):
    filtered_papers = {}
    for group, grouped_venues in papers.items():
      filtered_papers[group] = {}
      for venue, venue_papers in grouped_venues:
        filtered_papers[group][venue] = []
        venue_filtered_papers = filtered_papers[group][venue]
        for paper in venue_papers:
          if self.satisfies_filters(paper):
            venue_filtered_papers.append(paper)
    return filtered_papers

  def satisfies_filters(self, paper):
    for filter_, args, kwargs in self.filters:
      if not(filter_(paper, *args, **kwargs)):
        return False
    return True

  def add_filter(self, filter_, *args, **kwargs):
    self.filters.append((filter_, args, kwargs))