def get_venues(clients, confs, years):
  """
  Get venues from both API v1 and API v2 clients and merge the results.
  
  Args:
    clients: Tuple of (client_v1, client_v2)
    confs: List of conference names
    years: List of years
    
  Returns:
    List of venue IDs
  """
  client_v1, client_v2 = clients
  
  def filter_year(venue):
    if venue is None:
      return None
    for year in years:
      if year in venue:
        return venue
    return None
  
  # Get venues from API v1
  venues_v1 = []
  try:
    venues_v1 = client_v1.get_group(id='venues').members
  except Exception as e:
    print(f"Error getting venues from API v1: {e}")
  
  # Get venues from API v2
  venues_v2 = []
  try:
    venues_v2 = client_v2.get_group(id='venues').members
  except Exception as e:
    print(f"Error getting venues from API v2: {e}")
  
  # Merge venues from both APIs
  venues = list(set(venues_v1 + venues_v2))
  
  venues = list(map(filter_year, venues))
  venues = filter(lambda venue: venue is not None, venues)
  reqd_venues = []
  for venue in venues:
    for conf in confs:
      if conf.lower() in venue.lower():
        reqd_venues.append(venue)
        break
  reqd_venues = map(filter_year, reqd_venues)
  reqd_venues = list(filter(lambda venue: venue is not None, reqd_venues))
  return reqd_venues


def group_venues(venues, bins):
  def get_bins_dict():
    bins_dict = {bin:[] for bin in bins}
    return bins_dict
  
  bins_dict = get_bins_dict()
  for venue in venues:
    for bin in bins:
      if bin.lower() in venue.lower():
        bins_dict[bin].append(venue)
        break
  
  return bins_dict