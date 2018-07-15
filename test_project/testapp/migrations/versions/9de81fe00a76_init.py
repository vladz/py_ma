"""init

Revision ID: 9de81fe00a76
Revises: 
Create Date: 2018-07-15 00:32:24.462202

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9de81fe00a76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()

    connection.execute("""
        create table source (
            id integer primary key autoincrement not null,
            name text unique not null
        );
    """)

    connection.execute("""
        create table author (
            id integer primary key autoincrement not null,
            name text unique not null
        );
    """)

    connection.execute("""
        create table tag (
            id integer primary key autoincrement not null,
            data text unique not null
        );
    """)
    connection.execute("create index tag_idx_data on tag(data);")

    connection.execute("""
        create table article (
            id integer primary key autoincrement not null,
            title text not null,
            author_id integer references author(id) on delete cascade,
            description text,
            dt_create datetime not null,
            link text not null,
            source_id integer references source(id) on delete cascade
        );
    """)
    connection.execute("""
        create unique index article_uq_link on article(link);
    """)

    connection.execute("""
        create table article_tags (
            article_id integer not null 
                references article(id) on delete cascade,
            tag_id integer not null
                references tag(id) on delete cascade,
            primary key (article_id, tag_id)
        );
    """)
    connection.execute("""
        create index article_tag_idx_reverse on 
            article_tags(tag_id, article_id);
    """)


def downgrade():
    connection = op.get_bind()
    connection.execute("drop table source;")
    connection.execute("drop table author;")
    connection.execute("drop table tag;")
    connection.execute("drop table article;")
    connection.execute("drop table article_tags;")
