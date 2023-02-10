from thefuzz import fuzz


def check_keywords_with_keywords(keywords, paper_keywords, threshold):
  for keyword in keywords:
    for paper_keyword in paper_keywords:
      if fuzz.ratio(keyword, paper_keyword)>=threshold:
        return keyword, True
  return None, False


def check_keywords_with_text(keywords, text, threshold):
  for keyword in keywords:
    if fuzz.partial_ratio(keyword, text)>=threshold:
      return keyword, True
  return None, False


  def apply_filters(papers, filters):
    filtered_papers = {}
    for group, grouped_venues in papers.items():
      filtered_papers[group] = {}
      for venue, venue_papers in grouped_venues:
        filtered_papers[group][venue] = []
        venue_filtered_papers = filtered_papers[group][venue]
        for paper in venue_papers:
          satisfying_keyword, satisfying_filter_type, satisfies = satisfies_any_filters(paper, filters)
          # do something with all these satisfying keyword, satisfying filter, etc 
          if satisfies:
            venue_filtered_papers.append(paper)
    return filtered_papers


  def satisfies_any_filters(paper, filters):
    for filter_, args, kwargs in filters:
      matched_keyword, matched = filter_(paper, *args, **kwargs)
      if matched:
        filter_type = filter_.__name__
        return matched_keyword, filter_type, True
    return None, None, False


def keywords_filter(paper, keywords, threshold=85):
  return check_keywords_with_keywords(keywords, paper.content['keywords'], threshold)


def title_filter(paper, keywords, threshold=85):
  return check_keywords_with_keywords(keywords, paper.content['title'], threshold)


def abstract_filter(paper, keywords, threshold=85):
  return check_keywords_with_keywords(keywords, paper.content['abstract'], threshold)