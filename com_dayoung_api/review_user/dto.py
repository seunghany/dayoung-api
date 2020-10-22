from com_dayoung_api.ext.db import db

class ReviewUserDto(db.Model):

    __tablename__ = 'Actor_Movie'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    userid: str = db.Column(db.String(30))
    reviewid: str = db.Column(db.String(30))

    def __init__(self, userid, reviewid):
        self.userid = userid
        self.reviewid = reviewid

    def __repr__(self):
        return f'User_Movie(id={self.id},userid={self.userid},\
            moveid={self.movieid})'

    @property
    def json(self):
        return {
            'userid' : self.userid,
            'reviewid' : self.reviewid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

