def get_grouped_venue_papers(client, grouped_venue, only_accepted):
  papers = {}
  for venue in grouped_venue:
    papers[venue] = []
    if only_accepted:
      submissions = client.get_all_notes(content={'venueid': venue}, details='directReplies')
    else:
      single_blind_submissions = client.get_all_notes(invitation=f'{venue}/-/Submission', details='directReplies')
      double_blind_submissions = client.get_all_notes(invitation=f'{venue}/-/Blind_Submission', details='directReplies')
      submissions = single_blind_submissions + double_blind_submissions
    papers[venue]+=submissions

    print(venue)
    print(f'Number of papers: {len(submissions)}')
  return papers


def get_papers(client, grouped_venues, only_accepted):
  papers = {}
  for group, grouped_venue in grouped_venues.items():
    papers[group] = get_grouped_venue_papers(client, grouped_venue, only_accepted)
  return papers