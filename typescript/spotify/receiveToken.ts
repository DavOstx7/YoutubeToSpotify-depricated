import express from 'express';
import api, {config} from './api';

const CLIENT_ID = "?";
const CLIENT_SECRET = "?";
const REDIRECT_URI = "?";

function server() {
    const parsedRedirectUri = new URL(REDIRECT_URI);
    const app = express();
    
    app.get('/', (req, res) => {
        const queryParams = api.getAuthorizationQueryParams(CLIENT_ID, REDIRECT_URI);
        return res.redirect(`${config.urls.authorization}?${queryParams}`);
    })

    app.get(parsedRedirectUri.pathname, async (req, res) => {
        const code = req.query.code as string;
        const response = await api.requestAccessToken(CLIENT_ID, CLIENT_SECRET, code, REDIRECT_URI);
        res.send({"access_token": response.access_token});
    })

    const [port, hostname] = [Number(parsedRedirectUri.port), parsedRedirectUri.hostname];

    app.listen(port, hostname, () => {
        console.log(`Starting to listen on http://${hostname}:${port}`);
    });
}

server();
