from appname.models import db, Model

class Clip(Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.ForeignKey("user.id"), index=True,
                        nullable=True)

    file_name = db.Column(db.String())

    file_object_name = db.Column(db.String())

    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))

    GDPR_EXPORT_COLUMNS = {
        "created": "When the invite was created",
        "creator_id": "Who created the file",
        "file_name": "The name of the file",
    }
