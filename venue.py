def get_venues(client, confs, years):
  def filter_year(venue):
    for year in years:
      if year in venue:
        return venue
    return None
  venues = client.get_group(id='venues').members
  venues = list(map(filter_year, venues))
  venues = filter(lambda venue:venue is not None, venues)
  reqd_venues = []
  for venue in venues:
    for conf in confs:
      if conf.lower() in venue.lower():
        reqd_venues.append(venue)
        break
  reqd_venues = map(filter_year, reqd_venues)
  reqd_venues = list(filter(lambda venue:venue is not None, reqd_venues))
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