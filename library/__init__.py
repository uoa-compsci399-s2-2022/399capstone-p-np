from flask import Flask, request, url_for

import library.adaptersold.jsondatareader as reader

import library.adaptersold.repository as repo

#<!--from library.domain.model import Person-->

def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')

    reader.reader_instance = reader

    repo.repositoryInstance = repo.MemoryRepository()

    with app.app_context():
        from .Home import Home
        app.register_blueprint(Home.home_blueprint)

        from .browse_catalogue import Browse
        app.register_blueprint(Browse.browse_blueprint)

        from .find_book import find_book
        app.register_blueprint(find_book.find_book_blueprint)



    return app
