from score_display import db

class Gymnast(db.Model):
    __table_args__=(
        db.UniqueConstraint("name", "surname", "club", name="gymnast_ux1"),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True)
    surname = db.Column(db.String(256))
    club = db.Column(db.String(128))
    age_group = db.Column(db.String(128))
    level = db.Column(db.String(128), index=True)
    scores = db.relationship("GymnastScores", backref="gymnast")

class Apparatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    apparatus_name = db.relationship("GymnastScores", backref="apparatus")

class GymnastScores(db.Model):
    __table_args__=(
        db.UniqueConstraint("gymnast_id", "apparatus_id", name="gym_score_ux1"),
    )
    id = db.Column(db.Integer, primary_key=True)
    gymnast_id = db.Column(db.Integer, db.ForeignKey("gymnast.id"))
    apparatus_id = db.Column(db.Integer, db.ForeignKey("apparatus.id"))
    final_score = db.Column(db.String(64))

class ActiveSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(64))
    is_active = db.Column(db.Boolean(), default=False)
