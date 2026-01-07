from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from jwt import PyJWKClient

app = FastAPI()


keycloack_realm = "https://kubernetes.cosmotech.com/keycloak/realms/sphinx"


oauth_2_scheme = OAuth2AuthorizationCodeBearer(
    tokenUrl=f"{keycloack_realm}/protocol/openid-connect/token",
    authorizationUrl=f"{keycloack_realm}/protocol/openid-connect/auth",
    refreshUrl=f"{keycloack_realm}protocol/openid-connect/token",
)


async def valid_access_token(access_token: Annotated[str, Depends(oauth_2_scheme)]):
    url = f"{keycloack_realm}/protocol/openid-connect/certs"
    optional_custom_headers = {"User-agent": "custom-user-agent"}
    jwks_client = PyJWKClient(url, headers=optional_custom_headers)

    try:
        signing_key = jwks_client.get_signing_key_from_jwt(access_token)
        data = jwt.decode(
            access_token,
            signing_key.key,
            algorithms=["RS256"],
            audience="account",
            options={"verify_exp": True},
        )
        return data
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Not authenticated")


@app.get("/")
async def root(token: Annotated[str, Depends(valid_access_token)]):
    return {"message": "Hello World"}


@app.get("/about")
async def root():
    from cosmotech.aip import __version__

    return {"version": __version__}
