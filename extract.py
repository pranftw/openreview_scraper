class Extractor:
  def __init__(self, fields, subfields, include_subfield=False):
    self.fields = fields
    self.subfields = subfields
    self.include_subfield = include_subfield
  
  def __call__(self, paper):
    return self.extract(paper)

  def extract(self, paper):
    trimmed_paper = {}
    for field in self.fields:
      trimmed_paper[field] = paper.__getattribute__(field)
    for subfield, fields in self.subfields.items():
      if self.include_subfield:
        trimmed_paper[subfield] = {}
      for field in fields:
        field_value = paper.__getattribute__(subfield)[field]
        if self.include_subfield:
          trimmed_paper[subfield][field] = field_value
        else:
          trimmed_paper[field] = field_value
    return trimmed_paper