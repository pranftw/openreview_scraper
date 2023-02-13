import openreview
import csv
from config import EMAIL, PASSWORD
import dill


def get_client():
  return openreview.Client(baseurl='https://api.openreview.net', username=EMAIL, password=PASSWORD)


def papers_to_list(papers):
  all_papers = []
  for grouped_venues in papers.values():
    for venue_papers in grouped_venues.values():
      for paper in venue_papers:
        all_papers.append(paper)
  return all_papers


def to_csv(papers_list, fpath):
  def write_csv():
    with open(fpath, 'a+') as fp:
      fp.seek(0, 0) # seek to beginning of file and then read
      previous_contents = fp.read()
      writer = csv.DictWriter(fp, fieldnames=field_names)
      if previous_contents.strip()=='':
        writer.writeheader()
      writer.writerows(papers_list)
  if len(papers_list)>0:
    field_names = list(papers_list[0].keys()) # choose one of the papers, get all the keys as they'll be same for rest of them
    write_csv()


def save_papers(papers, fpath):
  with open(fpath, 'wb') as fp:
    dill.dump(papers, fp)
    print(f'Papers saved at: {fpath}')


def load_papers(fpath):
  with open(fpath, 'rb') as fp:
    papers = dill.load(fp)
  print(f'Papers loaded from: {fpath}')
  return papers