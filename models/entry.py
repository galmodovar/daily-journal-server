class Entry():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, date, concept, entry, mood_id):
        self.id = id
        self.date = date
        self.concept = concept
        self.entry = entry
        self.mood_id = mood_id
        self.mood = None
