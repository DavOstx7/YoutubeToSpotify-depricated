import asyncio
import urllib.parse
import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from python.spotify import api
from python.config.receive_token import SpotifyReceiveTokenConfig

config = SpotifyReceiveTokenConfig()


async def manual():
    # step 1: run the function below, authorize against spotify, grab the code from the redirect uri query parameter.

    # api.authorize_via_browser(config.client_id, config.redirect_uri)

    code = "?"

    # step 2: run the functions below, only after you have set the code variable with the value from step 1.
    # p.s do not forget to comment out the function from step 1.

    # response = await api.request_access_token(config.client_id, config.client_secret, code, config.redirect_uri)
    # print({"access_token": response["access_token"]})


def server():
    parsed_redirect_uri = urllib.parse.urlparse(config.redirect_uri)

    app = FastAPI()

    @app.get("/")
    async def authorize():
        query_params = api.get_authorization_query_params(config.client_id, config.redirect_uri)
        return RedirectResponse(f"{api.config.authorization_url}?{query_params}")

    @app.get(parsed_redirect_uri.path)
    async def access_token(code: str):
        response = await api.request_access_token(config.client_id, config.client_secret, code, config.redirect_uri)
        return {"access_token": response["access_token"]}

    uvicorn.run(app, port=parsed_redirect_uri.port, host=parsed_redirect_uri.hostname)


if __name__ == "__main__":
    server()
    # asyncio.run(manual())
