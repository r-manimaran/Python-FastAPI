# Simple Fastapi endpoint integration with Keycloak

- Install the Keycloak server. You can use Docker, here I have setup locally.
- Start the Keycloak server using the command
  ```console
  start the Keycloak in development mode. For Production , just  use start
  > kc.bat start-dev
  ```
  - Setup the new Realm. Here I have set it as Maransys
  - Create the client and enable client authentication
  ![alt text](image-4.png)

  ![alt text](image-5.png)
  - Add the below redirect urls
    http://127.0.0.1:8000/docs/oauth2-redirect
    http://127.0.0.1:8000/
  - For handle CORS, add the below Web Origins
    http://127.0.0.1:8000

## FastAPI endpoints
![alt text](image.png)

### Before Authentication

![alt text](image-3.png)

### Authorize

![alt text](image-2.png)

![alt text](image-6.png)

![alt text](image-1.png)

### Accessing private endpoint
![alt text](image-7.png)