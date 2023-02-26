from utils import get_client, to_csv, papers_to_list
from venue import get_venues, group_venues
from paper import get_papers
from filters import satisfies_any_filters


class Scraper:
  def __init__(self, conferences, years, keywords, extractor, fpath, selector=None, fns=[], groups=['conference'], only_accepted=True):
    # fns is a list of functions that can be specified by the user each taking in a single paper object as a parameter and returning the modified paper
    self.confs = conferences
    self.years = years
    self.keywords = keywords
    self.extractor = extractor
    self.fpath = fpath
    self.fns = fns
    self.groups = groups
    self.only_accepted = only_accepted
    self.selector = selector
    self.filters = []
    self.client = get_client()
    self.papers = None # this'll contain all the papers returned from apply_on_papers
  
  def __call__(self):
    self.scrape()
  
  def scrape(self):
    print("Getting venues...")
    venues = get_venues(self.client, self.confs, self.years)
    print("Getting papers...\n")
    papers = get_papers(self.client, group_venues(venues, self.groups), self.only_accepted)
    self.papers = papers
    print("\nFiltering papers...")
    papers = self.apply_on_papers(papers)
    if self.selector is not None:
      papers_list = self.selector(papers)
    else:
      papers_list = papers_to_list(papers)
    print("Saving as CSV...")
    to_csv(papers_list, self.fpath)
    print(f"Saved at {self.fpath}")
  
  def apply_on_papers(self, papers):
    modified_papers = {}
    for group, grouped_venues in papers.items():
      modified_papers[group] = {}
      for venue, venue_papers in grouped_venues.items():
        modified_papers[group][venue] = []
        venue_split = venue.split('/')
        venue_name, venue_year, venue_type = venue_split[0], venue_split[1], venue_split[2]
        for paper in venue_papers:
          # FILTERS
          satisfying_keyword, satisfying_filter_type, satisfies = satisfies_any_filters(paper, self.keywords, self.filters)
          if satisfies:
            # creating a new field(key) in content attr which is a dict
            paper.content['match'] = {satisfying_filter_type: satisfying_keyword}
            paper.content['group'] = group
            # Execute some custom functions
            for fn in self.fns:
              paper = fn(paper)
            # FIELD EXTRACTION here paper object will be converted into a dict
            extracted_paper = self.extractor(paper)
            # add some extra fields
            extracted_paper['venue'] = venue_name
            extracted_paper['year'] = venue_year
            extracted_paper['type'] = venue_type
            modified_papers[group][venue].append(extracted_paper)
    return modified_papers

  def add_filter(self, filter_, *args, **kwargs):
    self.filters.append((filter_, args, kwargs))