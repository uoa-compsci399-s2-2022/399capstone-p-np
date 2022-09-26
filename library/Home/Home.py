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
semesters = [["2020 Semester 1",["399 Compsci", "3 courses at 3rd level"], ["315 Compsci", "215 Compsci"], ["315 Compsci", "215 Compsci"],["399 Compsci", "3 courses at 3rd level"], ["315 Compsci", "215 Compsci"], ["315 Compsci", "215 Compsci"], ["315 Compsci", "215 Compsci"]],
                 ["2020 Semester 2",["215 Compsci", "120 Compsci"]],
                 ["2021 Semester 1",["230 Compsci", "130 Compsci"]]]

@home_blueprint.route('/', methods=['GET'])
def home():
    global semesters
    return render_template(
        'Home_Page.html',
        semesters=semesters,
        books=bookdata.reader_instance,
        home_url=url_for('home_bp.home'),
        find_book=url_for('find_book_bp.find_book'),
        #user = ("Welcome " + str(session['user_name']))
    )


