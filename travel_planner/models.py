class Tip:

    def __init__(self, id, venue_id, content):
        self.id = id
        self.venue_id = venue_id
        self.content = content


class Venue:

    def __init__(self, id, name, description, rating, lat, long, thumbnail):
        self.id = id
        self.name = name
        self.description = description
        self.rating = rating
        self.lat = lat
        self.long = long
        self.thumbnail = thumbnail
