# Integrating a custom app with CERN SSO

## Requirements

- Python 3.11 or 3.12
- A browser and your CERN account

## Hints and Tricks

- Always "Open in a new window" to avoid security issues with loading Keycloak in an iframe
- To Restart the server (e.g. after you change the code or environment variables), open the Terminal and type `refresh` (this will run start.sh for you)
- Make sure your client secret does not leave the .env file (this file is not shared if someone remixes your project)
- Logs are available at the bottom of the page (next to Terminal)

## 1. CERN SSO Integration (you must use your CERN account)

1. Go to <https://application-portal.web.cern.ch>, create an application and add an OAuth SSO registration
1. Add a redirectURI that is equal to `http://127.0.0.1:5000/*`
1. Add the client ID and Secret to your .env file
1. Test logging in

## 2. Authorisation

1. In the function `authorize`, parse the incoming token for roles and display
   a different html page based on the presence of a role (use your creativity!)

## 3. Call a protected API

1. Open <https://auth.docs.cern.ch/user-documentation/oidc/api-access/>
1. Follow the instructions to get an API token in the function `apitest`
   to get an API access token
1. To trigger the function you will need to access `http://<your glitch project>.glitch.me/apitest`
