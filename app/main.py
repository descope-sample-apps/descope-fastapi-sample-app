from fastapi import FastAPI, Security
from app.utils import TokenVerifier

import urllib.request

# We use PyJWKClient, which internally uses Python's built-in urllib.request, which sends requests
# without a standard User-Agent header (e.g., it sends "Python-urllib/3.x").
# Some CDNs or API gateways (like the one serving Descope's JWKS) may block such requests as they resemble bot traffic or security scanners.
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (DescopeFastAPISampleApp)')]
urllib.request.install_opener(opener)

app = FastAPI()
auth = TokenVerifier()

@app.get("/api/public")
def public():
    """Public Route: No Authentication required."""
    result = {
        "status": "success",
        "msg": "Success! This endpoint is publicly available and requires no authentication."
    }
    return result


@app.get("/api/private")
def private(auth_result: str = Security(auth)):
    """
    This is a protected route.

    Access to this endpoint requires a valid JWT access token.
    The `auth` dependency uses FastAPI's `Security` to perform token verification before entering this route.
    """
    return auth_result


@app.get("/api/private-scoped/readonly")
def private_scoped(auth_result: str = Security(auth, scopes=['read:messages'])):
    """
    This is a protected route with scope-based access control.

    Access to this endpoint requires:
    - A valid access token (authentication), and
    - The presence of the `read:messages` scope in the token.
    """
    return auth_result

@app.get("/api/private-scoped/write")
def private_scoped(auth_result: str = Security(auth, scopes=['read:messages', 'write:messages'])):
    """
    This is a protected route with scope-based access control.

    Access to this endpoint requires:
    - A valid access token (authentication), and
    - The presence of the `read:messages` and `write:messages` scope in the token.
    """
    return auth_result

@app.get("/api/private-scoped/delete")
def private_scoped(auth_result: str = Security(auth, scopes=['delete:messages'])):
    """
    This is a protected route with scope-based access control.

    Access to this endpoint requires:
    - A valid access token (authentication), and
    - The presence of the `delete:messages` scope in the token.
    """
    return auth_result
