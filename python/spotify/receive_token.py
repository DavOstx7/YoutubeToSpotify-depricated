import flask
import urllib.parse
from python.spotify import api
from python.config.receive_token import SpotifyReceiveTokenConfig

config = SpotifyReceiveTokenConfig()


def manual():
    # step 1: run the function below, authorize against spotify, grab the code from the redirect uri query parameter.

    # api.authorize_via_browser(config.client_id, config.redirect_uri)

    code = "?"

    # step 2: run the function below, only after you have set the code variable with the value from step 1.
    # p.s do not forget to comment out the function from step 1.

    # print(api.get_access_token(config.client_id, config.client_secret, code, config.redirect_uri))


def server():
    parsed_redirect_uri = urllib.parse.urlparse(config.redirect_uri)

    app = flask.Flask(__name__)

    @app.route("/")
    def authorize():
        query_params = api.get_authorization_query_params(config.client_id, config.redirect_uri)
        return flask.redirect(f"{api.config.authorization_url}?{query_params}")

    @app.route(parsed_redirect_uri.path)
    def access_token():
        code = flask.request.args.get("code")
        response = api.request_access_token(config.client_id, config.client_secret, code, config.redirect_uri)
        return {"access_token": response["access_token"]}

    app.run(host=parsed_redirect_uri.hostname, port=parsed_redirect_uri.port)


if __name__ == "__main__":
    server()
    # manual()
