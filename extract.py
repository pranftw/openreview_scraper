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