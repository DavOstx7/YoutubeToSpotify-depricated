import flask
import urllib.parse
from python.spotify import utils

CLIENT_ID = "?"
CLIENT_SECRET = "?"
REDIRECT_URI = "?"


def manual():
    # step 1: run the function below, authorize against spotify, grab the code from the redirect uri query parameter.

    utils.authorize_via_browser(CLIENT_ID, REDIRECT_URI)

    code = "?"

    # step 2: run the function below, only after you have set the code variable with the value from step 1.
    # p.s do not forget to comment out the function from step 1.

    utils.print_authorization_token(CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI)


def server():
    parsed_redirect_uri = urllib.parse.urlparse(REDIRECT_URI)

    app = flask.Flask(__name__)

    @app.route("/")
    def authorize():
        headers = utils.get_authorization_headers(CLIENT_ID, REDIRECT_URI)
        query_params = urllib.parse.urlencode(headers)
        return flask.redirect(f"{utils.spotify_api.AUTHORIZATION_URL}?{query_params}")

    @app.route(parsed_redirect_uri.path)
    def access_token():
        code = flask.request.args.get("code")
        response = utils.request_authorization_token(CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI)
        return {"access_token": response["access_token"]}

    app.run(host=parsed_redirect_uri.hostname, port=parsed_redirect_uri.port)


if __name__ == "__main__":
    server()
    # manual()
