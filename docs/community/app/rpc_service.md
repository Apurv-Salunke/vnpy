# RpcService - RPC Server Module

## Function Overview

RpcService is a functional module designed to **convert the VeighNa Trader process into an RPC server**, offering external services such as trade routing, market data push, and position fund inquiries.

For specific application scenarios of RPC, please refer to the "RPC Application Scenarios" section at the end of this document.

## Loading and Starting

### VeighNa Station Loading

After logging in to VeighNa Station, click the "Trade" button, and in the configuration dialog box, check the "RpcService" under the "Application Module" column.

### Script Loading

Add the following code to your startup script:
›
```python3
# Write at the top
from vnpy_rpcservice import RpcServiceApp

# Write after creating the main_engine object
main_engine.add_app(RpcServiceApp)
```

### Starting the Module

Before starting the module, please first connect and log in to the trading interface (connection methods are detailed in the basic usage section's connection interface part). Wait until you see "Contract information query successful" in the VeighNa Trader main interface's "Log" column before starting the module, as shown below:  

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/market_radar/1.png) 

After successfully connecting to the trading interface, click "Function" -> "RPC Service" in the menu bar, or click the icon in the left sidebar:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/1.png) 

This will enter the RPC service module's UI interface, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/2.png) 

## Configuration and Usage

### Configuring RPC Service
RPC service is developed based on ZeroMQ, and the external communication addresses include:

* **Request Response Address**
    * Used to passively receive requests sent by clients, execute corresponding tasks, and return results;
    * Function examples:
        * Market subscription;
        * Order placement;
        * Order cancellation;
        * Initial information inquiry (contracts, positions, funds, etc.);
* **Event Broadcast Address**
    * Used to actively push event data received by the server to all connected clients;
    * Function examples:
        * Market push;
        * Order push;
        * Trade push.

Both addresses adopt the ZeroMQ address format, consisting of two parts: **communication protocol** (e.g., tcp://) and **communication address** (e.g., 127.0.0.1:2014).

RPC service supports the following communication protocols:

* **TCP Protocol**
    * Protocol prefix: tcp://
    * Can be used on both Windows and Linux systems
    * Can be used for local communication (127.0.0.1) or network communication (network IP address)
* **IPC Protocol**
    * Protocol prefix: ipc://
    * Can only be used on Linux systems (POSIX local port communication)
    * Can only be used for local communication, with any string content as the suffix

It is generally recommended to directly use the TCP protocol (and the default address), and for users using Ubuntu systems who want to pursue lower communication latency, the IPC protocol can be used.

### Running RPC Service

After configuring the communication addresses, click the "Start" button to start the RPC service. The log area will output "RPC service started successfully", as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/3.png) 

After successful startup, you can use RpcGateway in another VeighNa Trader process (client) to connect

If you need to stop the RPC service, you can click the "Stop" button, at which point the log will output "RPC service stopped".

### Connecting Clients

VeighNa provides RpcGateway, which is designed to be used with RpcService, as a standard interface for clients to connect to the server and perform transactions, making it transparent to upper-layer applications.

From the client's perspective, RpcGateway is similar to a CTP interface. Since the external trading account configuration and connection have already been unified on the server side, clients only need to communicate with the server, without needing to re-enter account passwords and other information.

After loading the RpcGateway interface on the client, enter the VeighNa Trader main interface, click "System" -> "Connect RPC", and in the pop-up window, click "Connect" to connect and use, as shown below.

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/5.png)

The "Active Request Address" and "Push Subscription Address" correspond to the "Request Response Address" and "Event Broadcast Address" configured on the server side, respectively. Note not to write them in reverse.

## RPC Introduction

Due to the existence of the Global Interpreter Lock (GIL), a single Python process can only utilize the computing power of a single CPU core. The Remote Procedure Call (RPC) service can be used for **cross-process or cross-network service function calls**, effectively solving the above problem.

A specific process connects to the trading interface as the **server**, actively pushing events to other independent **client** processes within the local physical machine or local area network, and processing client-related requests, as shown below:

![](https://vnpy-doc.oss-cn-shanghai.aliyuncs.com/rpc_service/7.png)

## RPC Service (RpcService) Application Scenarios

- For users with a large number of running strategies, only one local market and trading channel is needed, supporting multiple client processes to trade simultaneously, with each client's trading strategies running independently and unaffected by each other;
- For small and medium-sized investment institutions, by loading various trading interfaces and RiskManagerApp on the server side, a lightweight asset management trading system can be implemented, allowing multiple traders to share a unified trading channel, and achieving fund-level risk management.
