# WebTrader - Web Server Module

## Function Overview

WebTrader is a functional module for **web application backend services**. Users can run and manage VeighNa quantitative strategy trading through browsers (rather than PyQt desktop clients).

## Architecture Design

WebTrader adopts FastAPI as the backend server, supporting REST active request calls and WebSocket passive data push. The overall framework diagram during operation is as follows:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_1.png)

The backend service includes two independent processes:
- Strategy Trading Process
  - The process running VeighNa Trader, responsible for running all strategy trading functions;
  - Started RpcServer for function calls to the web service process;
- Web Service Process
  - The process running FastAPI, responsible for providing web access services externally;
  - Started RpcClient for calling related functions of the strategy trading process.

Bidirectional communication modes from the web end to the strategy trading process include:
- Active Request Calls (market subscription, order placement/cancellation, data query)
  - Browser initiates REST API calls (accessing a certain URL address to submit data) to the web service process;
  - After receiving, the web service process converts them into RPC requests (Req-Rep communication mode) and sends them to the strategy trading process;
  - After executing request processing, the strategy trading process returns results to the web service process;
  - The web service process returns data to the browser.
- Passive Data Push (market push, order push)
  - Browser initiates Websocket connection to the web service process;
  - The strategy trading process pushes data received through RPC (Pub-Sub communication mode) to the web service process;
  - After receiving, the web service process pushes data to the browser in real-time through Websocket API (JSON format).

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [WebTrader] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_webtrader import WebTraderApp

# Write after creating the main_engine object
main_engine.add_app(WebTraderApp)
```

### Starting the Module

Before starting the module, please connect and log in to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/market_radar/1.png)

After successfully connecting to the trading interface, click [Function] -> [Web Service] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_0.png)

You can then enter the UI interface of the RPC service module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_3.png)

At this time, only the strategy trading process is running in the system. Server configuration options in the upper left area include:
- Username and Password: Username and password used when logging into the web application from the web end. When using, please modify to the username and password you want to use (modified through web_trader_setting.json under the .vntrader directory in the startup directory). Please note that the username and password here have nothing to do with the underlying trading interface;
- Request and Subscription Addresses: Addresses for RPC communication between the web service process and the strategy trading process in the architecture diagram. Note that ports should not conflict with other programs.

After clicking the start button, the web service process will be started in the system background according to the user's input configuration information, and relevant log information during Fast API operation will be output in the right area at the same time.


## Interface Demonstration
After starting the web service, open the URL <http://127.0.0.1:8000/docs> in the browser, and you will see the interface documentation webpage as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_2.png)

This contains information about interfaces currently supported by WebTrader. Below is a combination with the [Jupyter Notebook](https://github.com/vnpy/vnpy_webtrader/blob/main/script/test.ipynb) provided under the vnpy_webtrader project for related interface demonstrations.

### Obtaining Token
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
First import the corresponding modules requests and json, then define the URL, username, and password. By using the post method of requests to pass in corresponding parameters, you can obtain the token. Subsequently, you can directly pass in the token when accessing and using various interfaces.

### Market Subscription
```
r = requests.post(url + "tick/" + "cu2112.SHFE", headers={"Authorization":"Bearer " + token})
```
The above command can be used to subscribe to the contract cu2112.SHFE, and at the same time, the contract's market data push can be received on the GUI, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_4.png)

###  Batch Query
```python3
# Query function
def query_test(name):
    """Query corresponding type of data"""
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
If needed, you can also send active requests to query related data, such as tick data, contract data, account data, position data, order data, and trade data.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_5.png)

### Order Test
```python3
# Order test
req = {
    "symbol": "cu2112",
    "exchange": "SHFE",
    "direction": "Long",
    "type": "Limit",
    "volume": 1,
    "price": 71030,
    "offset": "Open",
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
After placing an order, you can also see order information on the GUI, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/web_trader/web_trader_6.png)

### Cancel Order Test
```python3
# Cancel order test
r = requests.delete(
    url + "order/" + vt_orderid,
    headers={"Authorization": "Bearer " + token}
)
```
If you want to cancel the previously placed order, you can send an active request. The result will also be updated on the GUI, as shown in the figure below:

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
WebTrader only implements the backend of web applications (provides interfaces for browsers to access data), while frontend pages (i.e., webpages seen in browsers) are left to community users to implement according to previous plans. Everyone is welcome to contribute code.

At the same time, WebTrader currently only supports basic manual trading functions. Subsequently, management functions related to strategy trading applications (such as CtaStrategy related calls) will be gradually added.
