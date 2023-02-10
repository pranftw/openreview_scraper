from utils import get_client
from venue import get_venues, group_venues
from paper import get_papers
from filter import satisfies_any_filters


class Scraper:
  def __init__(self, conferences, years, keywords, extractor, groups=['conference', 'workshop'], only_accepted=True):
    self.confs = conferences
    self.years = years
    self.keywords = keywords
    self.extractor = extractor
    self.groups = groups
    self.only_accepted = only_accepted
    self.filters = []
    self.client = get_client()
  
  def execute(self):
    venues = get_venues(self.client, self.confs)
    papers = get_papers(self.client, group_venues(venues, self.groups), self.only_accepted)
    papers = apply_on_papers(papers)
  
  def apply_on_papers(self, papers, fns=None):
    # fns is a list of functions that can be specified by the user each taking in a single paper object as a parameter and returning the modified paper
    modified_papers = {}
    for group, grouped_venues in papers.items():
      modified_papers[group] = {}
      for venue, venue_papers in grouped_venues:
        modified_papers[group][venue] = []
        for idx, paper in enumerate(venue_papers):
          # FILTERS
          satisfying_keyword, satisfying_filter_type, satisfies = satisfies_any_filters(paper, self.filters)
          if satisfies:
            # creating a new field(key) in content attr which is a dict
            paper.content['match'] = {satisfying_filter_type: satisfying_keyword}
            # Execute some custom functions
            for fn in fns:
              paper = fn(paper)
            # FIELD EXTRACTION
            modified_papers[group][venue].append(self.extractor.extract(paper))

  def add_filter(self, filter_, *args, **kwargs):
    self.filters.append((filter_, args, kwargs))