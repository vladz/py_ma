from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship

db = SQLAlchemy(session_options={'autocommit': False})


def create_or_get_one(session, model, **kwargs):
    try:
        with session.begin_nested():
            instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance
    except IntegrityError:
        session.rollback()
        return session.query(model).filter_by(**kwargs).one()


def get_one_or_create(session, model, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance


def upsert(session, model, search, data):
    instance: model
    try:
        with session.begin_nested():
            instance = model(**data)
        session.add(instance)
        session.commit()
    except IntegrityError:
        session.rollback()
        instance = session.query(model).filter_by(**search).one()
        map(lambda key, value: setattr(instance, key, value), data.items())
        session.flush()
    finally:
        return instance


class Source(db.Model):
    __tablename__ = 'source'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    articles = relationship('Article', backref='source')


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    articles = relationship('Article', backref='author')


article_tags = db.Table('article_tags',
                        db.Column('article_id', db.Integer,
                                  ForeignKey('article.id'),
                                  nullable=False),
                        db.Column('tag_id', db.Integer, ForeignKey('tag.id'),
                                  nullable=False))


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String, unique=True, nullable=False)


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('author.id'))
    description = db.Column(db.String)
    dt_create = db.Column(db.DateTime, nullable=False)
    link = db.Column(db.String, nullable=False)
    tags = relationship('Tag',
                        secondary=article_tags,
                        backref='articles')
    source_id = db.Column(db.Integer, ForeignKey('source.id'))
