"""Implement Flask and provide endpoints to interact with Descriptr."""

import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED
from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file
from functions.parse_scrape import add_course_capacity
from functions.save_webadvisor_courses import scrape_and_parse_webadvisor_courses
from classes.descriptr import Descriptr
import json

""" Change working directory to one level above here """
os.chdir(os.path.dirname(os.path.dirname(__file__)))


def create_app(test_config=None):
    app = Flask(__name__)
    dcptr = Descriptr()

    def scrape_handler(dcptr):
        """
        Wrap the Webadvisor scrape functionality.

        Params:
            dcptr: (Descriptr object): The Descriptr object.
        """
        print("Starting a scrape of Webadvisor")
        scrape_and_parse_webadvisor_courses()
        print("Scrape script SUCCESS.")
        print("Now parsing file.")
        dcptr.all_courses = add_course_capacity(dcptr.all_courses)
        print("DONE parsing file.")

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(lambda: scrape_handler(dcptr), 'interval', hours=24)
    sched.start()

    @app.route("/")
    def root():
        """
        List available endpoints in the API.

        Returns:
            (flask.response): A response with a JSON body of available endpoints.
        """
        return jsonify({'available_endpoints': ["/search", "/prerequisite", "/pkg"]})

    @app.route("/search", methods=['GET', 'POST'])
    def search():
        """
        GET available search filters. POST searches to Descriptr.

        Returns:
            (flask.response): A response with a JSON body of filters or courses.
        """
        if request.method == 'GET':
            # Make a list of methods of Decriptr that start with 'do_search_'
            searches = [method for method in dir(
                dcptr) if method.startswith("do_search_")]
            endpts = map(lambda x: x.replace("do_search_", "", 1), searches)
            return jsonify({'available_filters': list(endpts)})

        results = json.loads(dcptr.apply_filters(request.get_json()))
        status = 200 if results["error"] is None else 400
        return jsonify(results), status

    @app.route("/prerequisite/<course_id>", methods=['GET'])
    def prerequisite_search(course_id):
        """
        GET tree of prerequisites for a course by course id (eg. CIS-2750)

        Args:
            - course_id (string)    Id of a course with a hyphen (eg. CIS-2750 instead of CIS*2750)

        Returns:
            (flask.response): A response with a JSON body courses
        """
        try:
            dcptr.do_search_course_prerequisites({
                'query': course_id.replace("-", "*").upper(),
                'comparison': None
            })
            results = json.loads(dcptr.export_json())
            status = 200 if results["error"] is None else 400
        except Exception as e:
            status = 400
            results = {
                'courses': [],
                'error': str(e)
            }

        return jsonify(results), status

    @app.route("/pkg", methods=['GET'])
    def electron_executable_download():
        executable_target = request.args.get('type')

        path = None

        if executable_target == 'linux':
            path = "../electron-dist/descriptrly-0.1.0.AppImage"
        if executable_target == 'windows':
            path = "../electron-dist/descriptrly Setup 0.1.0.exe"

        if path is not None:
            return send_file(path, as_attachment=True)

        return jsonify({
            'error': True,
            'message': "Executable target not found"
        })

    return app
