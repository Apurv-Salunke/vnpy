# WebTrader - Web Server Module

## Function Introduction

WebTrader is a functional module for **Web application backend services**. Users can run and manage VeighNa quantitative strategy trading through a browser (not the PyQt desktop client).

## Architecture Design

WebTrader uses FastAPI as the backend server, supports REST active request calls and WebSocket passive data push, and the runtime overall framework is as follows:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_1.png)

The backend service consists of two independent processes:
- Strategy trading process
  - Runs the VeighNa Trader process, responsible for the operation of all strategy trading functions;
  - Start the RpcServer for the function call of the Web service process;
- Web service process
  - Runs the FastAPI process, responsible for providing Web access services;
  - Start the RpcClient to call the relevant functions of the strategy trading process.

The bidirectional communication mode from the web page to the strategy trading process includes:
- Active request call (subscribe to market data, place/cancel orders, query data)
  - The browser initiates a REST API call (access a URL address to submit data) to the Web service process;
  - After the Web service process receives it, it is converted into an RPC request (Req-Rep communication mode) and sent to the strategy trading process;
  - After the strategy trading process processes the request, it returns the result to the Web service process;
  - The Web service process returns the data to the browser.
- Passive data push (market data push, order push)
  - The browser initiates a WebSocket connection to the Web service process;
  - The strategy trading process pushes the data to the Web service process through RPC (Pub-Sub communication), and the Web service process pushes the data to the browser in real time through the WebSocket API (in JSON format).

## Load and Start

### VeighNa Station Load

After logging in to VeighNa Station, click the 【Trading】 button, and check the 【WebTrader】 in the 【Application Module】 column in the configuration dialog.

### Script Load

Add the following code to your startup script:

```python3
# Write at the top
from vnpy_webtrader import WebTraderApp

# Write after creating the main_engine object
main_engine.add_app(WebTraderApp)
```

### Start Module

Before starting the module, please connect to the trading interface (the connection method is detailed in the basic usage section of the connection interface). After seeing the output of "Contract information query successful" in the VeighNa Trader main interface **Log** column, start the module as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/market_radar/1.png)

After successfully connecting to the trading interface, click **Function** -> **Web Service** in the menu bar, or click the icon on the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_0.png)

You can enter the UI interface of the RPC service module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_3.png)

At this time, only the strategy trading process is running in the system, and the server configuration options in the upper left corner area include:
- Username and password: The username and password used when logging in to the Web application from the web page, please modify it to the username and password you want to use (modify it through the web_trader_setting.json under the startup directory .vntrader), please note that the username and password here are not related to the underlying trading interface;
- Request and subscription address: The address of the RPC communication between the Web service process and the strategy trading process in the architecture diagram, pay attention to the port to avoid conflicts with other programs.

After clicking the start button, the Web service process will be started in the system background according to the configuration information entered by the user, and the relevant log information during the running of Fast API will be output in the right area.

## Interface Demonstration

After starting the Web service, open the URL <http://127.0.0.1:8000/docs> in the browser, and you can see the interface documentation page as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_2.png)

This includes the relevant interface information supported by WebTrader at present. The following will demonstrate the relevant interfaces with the [Jupyter Notebook](https://github.com/vnpy/vnpy_webtrader/blob/main/script/test.ipynb) provided under the vnpy_webtrader project.

### Get Token

```python3
import requests
import json

url = "http://127.0.0.1:8000/"
username = "vnpy"
password = "vnpy"

r = requests.post(
    url + "token",
    data={"username": username, "password": password},
    headers={"accept": "application/json"}
)
token = r.json()["access_token"]
```
First, import the relevant modules requests and json, then define the url and username and password. You can get the token (token) by passing the corresponding parameters through the post method of requests, and then use the token for subsequent access to various interfaces.

### Market Data Subscription

```
r = requests.post(url + "tick/" + "cu2112.SHFE", headers={"Authorization":"Bearer " + token})
```
The above command can be used to subscribe to the contract cu2112.SHFE, and you can also receive the market data push of this contract in the graphical interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_4.png)

### Batch Query

```python3
# Query function
def query_test(name):
    """Query the corresponding type of data"""
    r = requests.get(
        url + name,
        headers={"Authorization": "Bearer " + token}
    )
    return r.json()

# Batch query
for name in ["tick", "contract", "account", "position", "order", "trade"]:
    data = query_test(name)
    print(name + "-" * 20)
    if data:
        print(data[0])
```
If necessary, you can also query related data through active requests, such as tick data, contract data, account data, position data, order data, and trade data.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_5.png)

### Order Test

```python3
# Order test
req = {
    "symbol": "cu2112",
    "exchange": "SHFE",
    "direction": "long",
    "type": "limit",
    "volume": 1,
    "price": 71030,
    "offset": "open",
    "reference": "WebTrader"
}

r = requests.post(
    url + "order",
    json=req,
    headers={"Authorization": "Bearer " + token}
)
vt_orderid = r.json()

print(vt_orderid)
```
After placing an order, you can also see the order information in the graphical interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_6.png)

### Cancel Order Test

```python3
# Cancel order test
r = requests.delete(
    url + "order/" + vt_orderid,
    headers={"Authorization": "Bearer " + token}
)
```
If you want to cancel the order placed earlier, you can send an active request, and the result will also be updated in the graphical interface, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_7.png)

### Websocket Test

```python3
# Websocket test
from websocket import create_connection

ws = create_connection("ws://127.0.0.1:8000/ws/?token=" + token)

while True:
    result =  ws.recv()
    print("Received '%s'" % result)

ws.close()
```
Through Websocket, you can passively receive market data and order data pushed by the strategy trading process, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_8.png)

## Future Plans

WebTrader only implements the backend of the Web application (providing interfaces for browser access), and the front-end page (the web page seen in the browser) is handed over to the community users to implement according to the previous plan. Welcome everyone to contribute code.

At the same time, WebTrader currently only supports basic manual trading functions, and will gradually add management functions related to strategy trading applications (such as the relevant calls of CtaStrategy).
