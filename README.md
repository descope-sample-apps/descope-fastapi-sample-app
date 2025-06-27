# Python FastAPI integration with Descope
This repository contains a Python FastAPI starter project for a backend server that demonstrates how to secure APIs using Descope authentication. It verifies JWT access tokens issued by Descope and enforces authorization for protected routes, including scope-based access control to restrict endpoints based on user permissions (e.g., read:messages, admin:write).

The implementation uses:
- PyJWT along with PyJWKClient for validating JWTs against Descope’s JWKS endpoint
- FastAPI’s Security dependency injection to enforce token validation and optional scope-based access control
- A custom TokenVerifier class for the token verification logic, including automatic key fetching and kid-based resolution

This starter is ideal for integrating Descope-authenticated clients (like web/mobile apps) with a secure Python FastAPI backend

## Setup
To setup this project locally, follow the steps below:
### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```
### 2. Create and Activate a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables
Create a .env file in the root directory of the project by copying the example file:
```bash
cp .env.example .env
```
Then, fill in the required environment variables:
- `DESCOPE_PROJECT_ID` — your Descope project ID, which you can get from https://app.descope.com/settings/project


## Starting the Server
This project uses [Uvicorn](https://www.uvicorn.org/) — a lightning-fast ASGI server — to run the FastAPI application.

To start the development server with auto-reload enabled:
```bash
uvicorn app.main:app --reload
```
Note: The `--reload` flag enables hot-reloading, so the server automatically restarts when you make code changes. This is recommended only for local development.

To verify that the server is up and running,  visit the following public test route in your browser: http://localhost:8000/api/public

## API Routes in this example app
To view all the API routes in this example, visit http://localhost:8000/docs.
1. `/api/public`: A public route, which does not require authentication
2. `/api/private`: A protected route, which requires a valid authentication token (JWT)
3. `/api/private-scoped/readonly`, `/api/private-scoped/write`, `/api/private-scoped/delete`, which are private, and also require the appropriate scopes (`read:messages`, `write:messages`, `delete:messages`) in the presented token.

## Calling the Server
To test your FastAPI endpoints, you can use tools like Postman or the terminal via curl.

### Using Postman
1. Open [Postman](https://www.postman.com/) and set the request URL to http://localhost:8000/<your route here>
2. To test authenticated routes (/private, /private-scoped/*), go to the Authorization tab, select 'Bearer Token' from the dropdown, and paste your JWT (access token) into the token field.

### Using curl
You can also directly use curl to test it on a terminal:

**Sample 'Readonly' Scope:**
```bash
curl -X 'GET' \
  'http://localhost:8000/api/private-scoped/readonly' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <YOUR_TOKEN_WITH_SCOPES>'
```
**Sample 'Write' Scope**
```bash
curl -X 'GET' \
  'http://localhost:8000/api/private-scoped/write' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <YOUR_TOKEN_WITH_SCOPES>'
```

## Testing the Authenticated Route (`/api/private`)

If you open: http://localhost:8000/api/private **without** providing an authorization token, you will receive a `401 Unauthorized` error.

To obtain a valid token for testing:
1. Visit [Descope Explorer](https://explorer.descope.com) in your browser.
2. Click the **⚙️ Settings** icon in the top-right corner.
3. Enter your **Project ID** and **Flow ID**.
4. You can now run your authentication flow directly in the browser.
5. After completing the login process, your **session JWT token** will be displayed in the Explorer UI.

You can then copy this token and:
- Paste it into the **Authorization header** of your requests in Postman.
- Alternatively, use it in `curl` commands as shown in the section on Calling the Server.

## Testing the Authenticated Route with Scopes (`/api/private-scoped/*`)
If you open any of the scoped routes (`/private-scoped/*`) such as http://localhost:8000/api/private-scoped/readonly with a token **that does not include the required scopes**, you will receive a `403 Forbidden` error indicating missing permissions.

To issue tokens containing scopes for testing:

1. Log in to your [Descope Console](https://app.descope.com/).
2. Navigate to **Project Settings > JWT Templates**: [JWT Templates](https://app.descope.com/settings/project/jwt)
3. Click the **➕ JWT Template** button to create a new template.
4. Under **Custom Claims**, add a new claim:
- **Key:** `scope`
- **Type:** `string`
- **Value:** A space-separated list of scopes, for example:
  ```
  read:messages write:messages
  ```
  or
  ```
  delete:messages
  ```
5. Click **Save** to create the template.
6. Next, go to the [**Session Management** settings](https://app.descope.com/settings/project/session):
7. Under **Token Format > User JWT**, select the JWT template you created above.
8. Click **Save** to apply the changes.

After updating your session configuration, new tokens issued via your flow will include the specified scopes, allowing you to successfully call all scoped routes.
