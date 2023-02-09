def get_decision(note):
  replies = [reply for reply in note.details['directReplies'] if reply['invitation'].endswith('Decision')]
  for reply in replies:
    decision = reply['content']['decision']
    decision_type = decision.split([1]) # usually here's where the type of accept is specified
    if 'Accept' in decision:
      return True
  return False


def get_accepted_papers(venues, client):
  accepted_papers = {}
  for venue in venues:
    accepted_papers[venue] = []
    # for confs that have already happened, use venueid, if it has not yet
    # then use the invitation, for both single and double blind
    # if venueid is used, then all the submissions will already have been accepted
    submissions = client.get_all_notes(content={'venueid': venue}, details='directReplies')
    if len(submissions)!=0:
      notes = [note for note in submissions]
      accepted_papers[venue]+=notes
    else:
      single_blind_submissions = client.get_all_notes(invitation=f'{venue}/-/Submission', details='directReplies')
      double_blind_submissions = client.get_all_notes(invitation=f'{venue}/-/Blind_Submission', details='directReplies')
      single_blind_notes = [note for note in single_blind_submissions]
      double_blind_notes = [note for note in double_blind_submissions]
      notes = single_blind_notes + double_blind_notes
      for note in notes:
        if get_decision(note):
          accepted_papers[venue].append(note)
    print(venue)
    print(len(notes))
  return accepted_papers