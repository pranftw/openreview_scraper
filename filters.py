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


def satisfies_any_filters(paper, keywords, filters):
  for filter_, args, kwargs in filters:
    matched_keyword, matched = filter_(paper, keywords=keywords, *args, **kwargs)
    if matched:
      filter_type = filter_.__name__
      return matched_keyword, filter_type, True
  return None, None, False


def keywords_filter(paper, keywords, threshold=85):
  paper_keywords = paper.content.get('keywords')
  if paper_keywords is not None:
    return check_keywords_with_keywords(keywords, paper_keywords, threshold)
  return None, False


def title_filter(paper, keywords, threshold=85):
  paper_title = paper.content.get('title')
  if paper_title is not None:
    return check_keywords_with_text(keywords, paper_title, threshold)
  return None, False


def abstract_filter(paper, keywords, threshold=85):
  paper_abstract = paper.content.get('abstract')
  if paper_abstract is not None:
    return check_keywords_with_text(keywords, paper_abstract, threshold)
  return None, False