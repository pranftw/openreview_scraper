import os
from utils import papers_to_list


class Selector:
  def __init__(self, fields=None, options=None, start_idx=0):
    self.idx = start_idx
    self.fields = fields if fields is not None else ['title', 'abstract']
    if options is None:
      self.options = {
        'y':{
          'desc':'yes',
          'fn':lambda paper, selected_papers:selected_papers.append(paper)
        },
        'n':{
          'desc':'no'
        }
      }
    else:
      self.options = options
    self.options['e'] = {'desc':'exit'}
  
  def __call__(self, papers):
    return self.select(papers)
  
  def select(self, papers):
    os.system('clear') # i only support unix based systems
    papers_list = papers_to_list(papers)
    selected_papers = []
    while self.idx<len(papers_list):
      paper = papers_list[self.idx]
      self.print_paper(paper)
      decision = self.handle_options(paper, selected_papers)
      if decision=='e': # e will be exit
        print()
        break
      self.idx+=1
    return selected_papers
  
  def print_paper(self, paper):
    paper_str = ''
    paper_str+='\n' + '-'*os.get_terminal_size().columns + '\n'
    paper_str+=f'Paper {self.idx}\n'
    for field in self.fields:
      paper_str+=f'{field.upper()}: {paper[field]}\n'
    print(f'\r{paper_str}', end='')

  def handle_options(self, paper, selected_papers):
    options_str = ''
    for option, option_dict in self.options.items():
      options_str+=f"{option}: {option_dict['desc']}  "
    decision = input(options_str)
    while decision not in self.options.keys():
      print("Invalid input!")
      decision = input(options_str)
    if self.options[decision].get('fn') is not None:
      self.options[decision]['fn'](paper, selected_papers)
    return decision