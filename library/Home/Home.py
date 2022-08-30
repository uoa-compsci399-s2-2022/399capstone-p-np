from flask import Blueprint, render_template, url_for

from flask import request, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired

import library.adapters.jsondatareader as bookdata
import library.domain.model as model

home_blueprint = Blueprint(
    'home_bp', __name__
)


@home_blueprint.route('/', methods=['GET'])
def home():
    semesters = [["a", "b"],[""],[""]]
    return render_template(
        'Home_Page.html',
        semesters=semesters,
        books=bookdata.reader_instance,
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),
        #user = ("Welcome " + str(session['user_name']))
    )


