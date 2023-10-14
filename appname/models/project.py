from appname.models import db, Model
from appname.models.clip import Clip

class Project(Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    title = db.Column(db.String())
    description = db.Column(db.String())

    clips = db.relationship('Clip', backref='project')

    GDPR_EXPORT_COLUMNS = {
        "created": "When the invite was created",
        "creator_id": "Who created the file",
        "description": "The description of the file",
    }