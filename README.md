### Runs a flask server (python) which accepts http requests and sends corresponding commands to freenet Funk servers to get your data from their servers or order a specific cell phone tariff using [this freenet Funk API](https://github.com/lagmoellertim/freenet-funk-api).

## Setup
- ### On a windows machine:
1. start a terminal session in the root directory of this repository's folder
2. in your terminal run `powershell -ExecutionPolicy ByPass -File "./setup/windows.ps1"`
3. edit **configuration/credentials.py** by filling in your freenet Funk credentials
4. run the server with `python server.py`

## Requests

### Get data from funk servers:
`GET`-request to the server with the following body as a full example
```
{
    "retrieve": data
}
```
`retrieve` can have one of the following values:  
    - `data`: responds with an object containing all your freenet FUNK data  
    - `personalInfo`: responds with your personal information (email, name, bday, etc.)  
    - `orderedProducts`: responds with a list of all of your ordered products (sim-cards, plans, etc.)  
    - `currentPlan`: resonds with your currently running cell-tariff


### Order a specific cell-tariff (mobile plan)
`POST`-request to the server with the following body as a full example
```
{  
    "order": "1gb"
}
```

`order` can have one of the following values:  
    - `1gb`: orders the 1gb plan for tomorrow  
    - `unlimited`: orders unlimited for tomorrow  
    - `pause`: pauses your plan beginning tomorrow  
    - `undo`: cancels your current plan (for details, [see here](https://github.com/lagmoellertim/freenet-funk-api))  

>each of these resond with an object containing information of wether or not the action was successful and what your current plan is afterwards.

<br/>  

## Docker:

### Image on Docker Hub:

https://hub.docker.com/repository/docker/doganm95/freenet_funk-rest-api-server

### Local build:

`docker build -t doganm95/freenet_funk-rest-api-server -f ./docker/Dockerfile .`

### Run the image: 
`docker run -p <port>:5000 -e "FUNK_USERNAME=<your_username>" -e "FUNK_PASSWORD=<your_password>" doganm95/freenet_funk-rest-api-server`  

Note: replace `<your_username>` and `<your_password>` with your credentials and `<port>` with your desired port
