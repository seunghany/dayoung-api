from com_dayoung_api.ext.db import db

class MovieDto(db.Model):
    
    __tablename__ = 'movies'
    __table_args__= {'mysql_collate':'utf8_general_ci'}

    id : int = db.Column(db.Integer, primary_key = True, index = True)
    movie_name : str = db.Column(db.String(30))
    genre : str = db.Column(db.String(30))
    country : str = db.Column(db.String(30))
    year : str = db.Column(db.String(4))
    company : str = db.Column(db.String(30))
    director : str = db.Column(db.String(30))
    actor : str = db.Column(db.String(30))
    keyword : str = db.Column(db.String(30))

    articles = db.relationship('ArticleModel', lazy='dynamic')

    def __init__(self, id, movie_name, genre, country, year, company, director, actor, keyword):
        self.id = id
        self.movie_name = movie_name
        self.genre = genre
        self.country = country
        self.year = year
        self.company = company
        self.director = director
        self.actor = actor
        self.keyword = keyword


    def __repr__(self):
        return f'Movie(id=\'{self.id}\',\
            movie_name=\'{self.movie_name}\',\
            genre=\'{self.genre}\',\
            country=\'{self.country}\',\
            year=\'{self.year}\',\
            company=\'{self.company}\',\
            director=\'{self.director}\',\
            actor=\'{self.actor}\',\
            keyword=\'{self.keyword}\',)'

    @property
    def json(self):
        return {
            'id' : self.id,
            'movie_name' : self.movie_name,
            'genre' : self.genre,
            'country' : self.country,
            'year' : self.year,
            'company' : self.company,
            'director' : self.director,
            'actor' : self.actor,
            'keyword' : self.keyword
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
