from flask import Flask, send_from_directory
from flask_graphql import GraphQLView

from models import db_session
from schema import schema, Department

import logging
from slack_logger import SlackHandler, SlackFormatter
from flask.logging import default_handler

app = Flask(__name__)
app.debug = True

root = logging.getLogger()

# def yashlogger(abc,level="asd"):
#     print(abc)

app.add_url_rule(
    '/gqlsecretpathhuehuehuehue',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True # for having the GraphiQL interface
    )
)
# Custom static data
@app.route('/app/<path:filename>')
def custom_static(filename):
    return send_from_directory("app-static", filename)

@app.route('/asdasdafgwgwrgregergerger')
def yash():
    pass

@app.route('/', methods=['GET'])
def home():
    return "<a href='app/index.html'>Hello there</h1></a>"


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(port=8002, host="0.0.0.0")
