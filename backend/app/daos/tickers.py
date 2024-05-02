from app.internal.firebase import db


class TickerDAO:

    def __init__(self, collection_path):
        self.collection_ref = db.collection(collection_path)
