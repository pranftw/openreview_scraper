from config import EMAIL, PASSWORD


def get_client():
  return openreview.Client(baseurl='https://api.openreview.net', username=EMAIL, password=PASSWORD)


def papers2csv(final_papers, fpath):
  all_papers = []
  for venue, papers in final_papers.items():
    venue_split = venue.split('/')
    venue_name, venue_year, venue_type = venue_split[0], venue_split[1], venue_split[2]
    for paper in papers:
      paper['venue'] = venue_name
      paper['year'] = venue_year
      paper['type'] = venue_type
      all_papers.append(paper)

  field_names = list(all_papers[0].keys()) # choose one of the papers, get all the keys as they'll be same for rest of them

  def write_csv():
    with open(fpath, 'w') as fp:
      writer = csv.DictWriter(fp, fieldnames=field_names)
      writer.writeheader()
      writer.writerows(all_papers)
  write_csv()    