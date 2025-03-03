def get_grouped_venue_papers(clients, grouped_venue, only_accepted):
  """
  Get papers from both API v1 and API v2 clients and merge the results.
  
  Args:
    clients: Tuple of (client_v1, client_v2)
    grouped_venue: List of venue IDs
    only_accepted: Boolean to filter only accepted papers
    
  Returns:
    Dictionary of papers by venue
  """
  client_v1, client_v2 = clients
  papers = {}
  
  for venue in grouped_venue:
    papers[venue] = []
    
    # Get papers from API v1
    submissions_v1 = []
    try:
      if only_accepted:
        submissions_v1 = client_v1.get_all_notes(content={'venueid': venue}, details='directReplies')
      else:
        single_blind_submissions = client_v1.get_all_notes(invitation=f'{venue}/-/Submission', details='directReplies')
        double_blind_submissions = client_v1.get_all_notes(invitation=f'{venue}/-/Blind_Submission', details='directReplies')
        submissions_v1 = single_blind_submissions + double_blind_submissions
    except Exception as e:
      print(f"Error getting papers from API v1 for venue {venue}: {e}")
    
    # Get papers from API v2
    submissions_v2 = []
    try:
      if only_accepted:
        submissions_v2 = client_v2.get_all_notes(content={'venueid': venue}, details='directReplies')
      else:
        single_blind_submissions = client_v2.get_all_notes(invitation=f'{venue}/-/Submission', details='directReplies')
        double_blind_submissions = client_v2.get_all_notes(invitation=f'{venue}/-/Blind_Submission', details='directReplies')
        submissions_v2 = single_blind_submissions + double_blind_submissions
    except Exception as e:
      print(f"Error getting papers from API v2 for venue {venue}: {e}")
    
    # Merge submissions from both APIs
    # Use forum IDs to avoid duplicates
    forum_ids = set()
    merged_submissions = []
    
    for submission in submissions_v1 + submissions_v2:
      if hasattr(submission, 'forum') and submission.forum not in forum_ids:
        forum_ids.add(submission.forum)
        merged_submissions.append(submission)
    
    papers[venue] += merged_submissions
    
    print(venue)
    print(f'Number of papers: {len(merged_submissions)}')
  
  return papers


def get_papers(clients, grouped_venues, only_accepted):
  """
  Get papers for all grouped venues.
  
  Args:
    clients: Tuple of (client_v1, client_v2)
    grouped_venues: Dictionary of venue IDs by group
    only_accepted: Boolean to filter only accepted papers
    
  Returns:
    Dictionary of papers by group and venue
  """
  papers = {}
  for group, grouped_venue in grouped_venues.items():
    papers[group] = get_grouped_venue_papers(clients, grouped_venue, only_accepted)
  return papers