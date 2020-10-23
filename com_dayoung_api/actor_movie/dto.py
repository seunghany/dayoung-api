from com_dayoung_api.ext.db import db

class ActorMovieDto(db.Model):

    __tablename__ = 'ActorMovie'
    __table_args__={'mysql_collate':'utf8_general_ci'}

    userid: str = db.Column(db.String(30))
    moveid: str = db.Column(db.String(30))

    def __init__(self, userid, movieid):
        self.userid = userid
        self.moveid = movieid

    def __repr__(self):
        return f'User_Movie(id={self.id},userid={self.userid},\
            moveid={self.movieid})'

    @property
    def json(self):
        return {
            'userid' : self.userid,
            'moveid' : self.movieid
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

