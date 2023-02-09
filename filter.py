from thefuzz import fuzz


def check_keywords_with_keywords(paper_keywords, threshold=85):
  for keyword in keywords:
    for paper_keyword in paper_keywords:
      if fuzz.ratio(keyword, paper_keyword)>=threshold:
        return keyword, True
  return None, False


def check_keywords_with_text(text):
  for keyword in keywords:
    if keyword in text:
      return keyword, True
  return None, False


def filter_on_requirements(accepted_papers):
  filtered_papers = {}
  for venue, papers in accepted_papers.items():
    filtered_papers[venue] = []
    for paper in papers:
      checker = {
        'keywords': check_keywords_with_keywords(paper.content['keywords']),
        'title': check_keywords_with_keywords(paper.content['title']),
        'abstract': check_keywords_with_keywords(paper.content['abstract'])
      }
      paper.content['matches'] = {}
      any_match = False
      for field, field_checker in checker.items():
        matched_keyword, matched = field_checker
        if matched:
          if not any_match:
            any_match = True
          paper.content['matches'][field] = matched_keyword
      if any_match:
        filtered_papers[venue].append(paper)
  return filtered_papers