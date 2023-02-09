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


def extract_required_fields(paper, required_fields, required_subfields, include_subfield):
  trimmed_paper = {}
  
  for field in required_fields:
    trimmed_paper[field] = paper.__getattribute__(field)

  for subfield, fields in required_subfields.items():
    if include_subfield:
      trimmed_paper[subfield] = {}
    for field in fields:
      field_value = paper.__getattribute__(subfield)[field]
      if include_subfield:
        trimmed_paper[subfield][field] = field_value
      else:
        trimmed_paper[field] = field_value
  return trimmed_paper


def get_required_fields(filtered_papers, required_fields=['forum'], required_subfields={'content':['title', 'keywords', 'abstract', 'pdf', 'matches']}, include_subfield=False):
  # matches is not part of the original openreview response
  required_fields_papers = {}
  for venue, papers in filtered_papers.items():
    required_fields_papers[venue] = []
    for paper in papers:
      required_fields_papers[venue].append(extract_required_fields(paper, required_fields, required_subfields, include_subfield))
  return required_fields_papers