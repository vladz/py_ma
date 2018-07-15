import os
import logging

from flask import Flask, render_template

from app.models import db
from app.settings import Config

from app.models import Source
from app.workers import import_rss_data

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/')
def index():
    sources = Source.query.all()
    return render_template('index.html', sources=sources)


@app.route('/load_habra', endpoint='load_habra', methods=['get'])
def load_habra():
    logger.debug('Load habra')
    err = import_rss_data('habra')
    return err or 'Habra loaded!'


@app.route('/load_reddit', endpoint='load_reddit', methods=['get'])
def load_reddit():
    logger.debug('Load reddit')
    err = import_rss_data('reddit')
    return err or 'Reddit loaded!'


if __name__ == '__main__':
    logging.getLogger().handlers = []  # drop all previous logger handlers
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if os.getenv('DEBUG') else logging.INFO)
    logger.info('Init app')

    app.run(host='0.0.0.0')
