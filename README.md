### Runs a flask server (python) which accepts http requests and sends corresponding commands to freenet Funk servers to get your data from their servers or order a specific cell phone tariff using [this freenet Funk API](https://github.com/lagmoellertim/freenet-funk-api)

## Setup

- ### On a windows machine

1. start a terminal session in the root directory of this repository's folder  
2. in your terminal run `powershell -ExecutionPolicy ByPass -File "./setup/windows.ps1"`  
3. edit **configuration/credentials.py** by filling in your freenet Funk credentials  
4. run the server with `python server.py`  

- ### As a docker container

    - #### Using pre-built image from docker hub (recommended) 

        [See documentation on docker hub](https://hub.docker.com/repository/docker/doganm95/freenet_funk-rest-api-server)

    - #### Building it locally

    1. `git clone https://github.com/DoganM95/Freenet_Funk-rest-api-server`  
    2. Open a terminal session in the cloned folder  
    3. Build the docker image using the cloned files:  
   `docker build -t doganm95/freenet_funk-rest-api-server -f ./docker/Dockerfile .`  
    4. Run the image as a container:  
   `docker run -p <port>:5000 -e "FUNK_USERNAME=<your_username>" -e "FUNK_PASSWORD=<your_password>" doganm95/freenet_funk-rest-api-server`  
       >Replace `<your_username>` and `<your_password>` with your credentials and `<port>` with your desired port

## Requests

### Get data from funk servers

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

### Order a specific cell-tariff (mobile plan)

`POST`-request to the server with the following body as a full example

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

>each of these respond with an object containing information of whether or not the action was successful and what your current plan is afterwards.
