# RpcService - RPC Server Module

## Function Overview

RpcService is a functional module for **converting VeighNa Trader processes into RPC servers**, providing functions such as trading routing, market data push, and position/capital query to the outside.

For specific application scenarios of RPC, please refer to the [RPC Application Scenarios] section at the end of this document.

## Loading and Launching

### Loading via VeighNa Station

After launching and logging into VeighNa Station, click the [Trading] button. In the configuration dialog, check [RpcService] in the [Application Module] section.

### Loading via Script

Add the following code to the startup script:

```python3
# Write at the top
from vnpy_rpcservice import RpcServiceApp

# Write after creating the main_engine object
main_engine.add_app(RpcServiceApp)
```

### Starting the Module

Before starting the module, please connect and log in to the trading interface first (for connection methods, see the Interface Connection section in the Basic Usage chapter). After seeing "Contract information query successful" output in the [Log] section of the VeighNa Trader main interface, start the module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/market_radar/1.png)

After successfully connecting to the trading interface, click [Function] -> [RPC Service] in the menu bar, or click the icon in the left button bar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/1.png)

You can then enter the UI interface of the RPC service module, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/2.png)

## Configuration and Usage

### Configuring RPC Service
RPC service is developed based on ZeroMQ, and external communication addresses include:

* **Request-Response Address**
    * Used to passively receive requests sent by clients, execute corresponding tasks, and return results;
    * Function examples:
        * Market subscription;
        * Order placement;
        * Order cancellation;
        * Initialization information query (contracts, positions, capital, etc.);
* **Event Broadcast Address**
    * Used to actively push event data received by the server to all connected clients;
    * Function examples:
        * Market push;
        * Order push;
        * Trade push.

The above addresses all use ZeroMQ address format, consisting of two parts: **communication protocol** (such as tcp://) and **communication address** (such as 127.0.0.1:2014).

Communication protocols supported by RPC service include:

* **TCP Protocol**
    * Protocol prefix: tcp://
    * Can be used on both Windows and Linux systems
    * Can be used for local communication (127.0.0.1) or network communication (network IP address)
* **IPC Protocol**
    * Protocol prefix: ipc://
    * Can only be used on Linux systems (POSIX local port communication)
    * Can only be used for local communication, suffix is any string content

It is generally recommended to use the TCP protocol (and default address) directly. For users using Ubuntu systems and hoping to pursue lower communication latency, the IPC protocol can be used.

### Running RPC Service

After completing the communication address configuration, click the [Start] button to start the RPC service. The log area will output "RPC service started successfully", as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/3.png)

After successful startup, you can use RpcGateway to connect in another VeighNa Trader process (client)

If you need to stop the RPC service, you can click the [Stop] button. At this time, the log outputs "RPC service stopped".


### Connecting Clients

VeighNa provides RpcGateway matching RpcService as a standard interface for clients to connect to the server and conduct trading, transparent to upper-layer applications.

From the client's perspective, RpcGateway is an interface similar to CTP. Because external trading account configuration and connection are uniformly completed on the server side, the client only needs to communicate with the server side and does not need to enter account password and other information again.

After loading the RpcGateway interface on the client, enter the VeighNa Trader main interface, click [System] -> [Connect RPC] in the menu bar, and click the [Connect] button in the pop-up window to connect and use, as shown in the figure below.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/5.png)

[Active Request Address] and [Push Subscription Address] correspond to [Request-Response Address] and [Event Broadcast Address] configured on the server side respectively. Note not to write them in reverse.


## RPC Introduction

Due to the existence of the Global Interpreter Lock (GIL), a single Python process can only use the computing power of one CPU core. Remote Procedure Call Protocol (RPC) service can be used for **cross-process or cross-network service function calls**, effectively solving the above problem.

A specific process connects to the trading interface to act as a **server**, actively pushing events to other independent **client** processes in the local physical machine or local area network, and processing client-related requests, as shown in the figure below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/7.png)

## Application Scenarios of RPC Service (RpcService)

- For users running a large number of strategies, only one market and trading channel is needed locally, which can support multiple client processes trading simultaneously, and trading strategies in each client run independently without interfering with each other;
- For small and medium-sized investment institution users, by loading various trading interfaces and RiskManagerApp on the server side, a lightweight asset management trading system can be implemented. Multiple traders share a unified trading channel and achieve fund product-level risk management.
