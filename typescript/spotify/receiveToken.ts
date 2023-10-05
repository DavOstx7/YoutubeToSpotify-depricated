import receiveTokenConfig from '../../receive_token_config.json';
import express from 'express';
import api, {config as apiConfig} from './api';

const tokenConfig = receiveTokenConfig.spotify;

function server() {
    const parsedRedirectUri = new URL(tokenConfig.redirect_uri);
    const app = express();
    
    app.get('/', (req, res) => {
        const queryParams = api.getAuthorizationQueryParams(tokenConfig.client_id, tokenConfig.redirect_uri);
        return res.redirect(`${apiConfig.urls.authorization}?${queryParams}`);
    })

    app.get(parsedRedirectUri.pathname, async (req, res) => {
        const code = req.query.code as string;
        const response = await api.requestAccessToken(tokenConfig.client_id, tokenConfig.client_secret, code, tokenConfig.redirect_uri);
        res.send({"access_token": response.access_token});
    })

    const [port, hostname] = [Number(parsedRedirectUri.port), parsedRedirectUri.hostname];

    app.listen(port, hostname, () => {
        console.log(`Starting to listen on http://${hostname}:${port}`);
    });
}

server();
