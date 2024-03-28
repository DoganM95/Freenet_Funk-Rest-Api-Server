# Intro

Runs a flask server which sends commands to freenet Funk servers to get user data or order a specific cell phone tariff using [this freenet Funk API](https://github.com/lagmoellertim/freenet-funk-api)

## Docker

```bash
docker run \
  -p <port>:5000 \
  -e "FUNK_USERNAME=<your_username>" \
  -e "FUNK_PASSWORD=<your_password>" \
  -e "PASSWORD_HASHING_ALGORITHM=<your_preferred_algorithm>" \
  -e "SSL_PRIVATE_KEY=<your_server_ssl_private_key>" \
  -e "SSL_CERT=<your_server_ssl_cert>" \
  -e "SERVER_MODE=dev" \
  -v "<your_local_pem_certs_folder>:/usr/src/app/volume/ssl/"
  doganm95/freenet_funk-rest-api-server
```  

## Usage

### Authorization

If ssl encryption is used (by providing a `privkey.pem` and a `cert.pem`, see docker hub), every request needs an `Authorization` header, containing a Bearer Token. The Bearer Token is your Funk password, hashed using the algorithm you chose before (default: `sha3_512`). Running the container in dev mode logs the hashed pw, which can be copied.

### Requests

Responses contain an object with information on whether or not the action was successful and what your current plan is afterwards.

#### Get data from funk servers

`GET`-request to the server with the following body as a full example:

```json
{
  "retrieve": "data"
}
```

`retrieve` can have one of the following values:  
  - `data`: responds with an object containing all your freenet FUNK data  
  - `personalInfo`: responds with your personal information (email, name, bday, etc.)  
  - `orderedProducts`: responds with a list of all of your ordered products (sim-cards, plans, etc.)  
  - `currentPlan`: resonds with your currently running cell-tariff

#### Order a specific cell-tariff (mobile plan)

`PUT`-request to the server with the following body as a full example

```json
{  
  "order": "1gb"
}
```

`order` can have one of the following values:  
  - `1gb`: orders the 1gb plan for tomorrow  
  - `unlimited`: orders unlimited for tomorrow  
  - `pause`: pauses your plan beginning tomorrow  
  - `undo`: cancels your current plan (for details, [see here](https://github.com/lagmoellertim/freenet-funk-api))  
