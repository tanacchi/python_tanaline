from app import db

class Talk(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80))
    content = db.Column(db.String(200))

    def __init__(self, user_id, content):
        self.user_id = user_id
        self.content = content
