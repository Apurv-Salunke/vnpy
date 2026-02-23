from enum import Enum
from typing import Any, Literal
import asyncio
import json
from datetime import datetime, timedelta
import secrets

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, status, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from pathlib import Path

from vnpy.rpc import RpcClient
from vnpy.trader.object import (
    AccountData,
    ContractData,
    OrderData,
    OrderRequest,
    PositionData,
    SubscribeRequest,
    CancelRequest,
    TickData,
    TradeData
)
from vnpy.trader.constant import (
    Exchange,
    Direction,
    OrderType,
    Offset,
)
from vnpy.trader.utility import load_json, get_file_path


# WebServiceRunningConfig
SETTING_FILENAME = "web_trader_setting.json"
SETTING_FILEPATH = get_file_path(SETTING_FILENAME)

setting: dict = load_json(SETTING_FILEPATH)
USERNAME = setting["username"]              # Username
PASSWORD = setting["password"]              # Password
REQ_ADDRESS = setting["req_address"]        # RequestServiceAddress
SUB_ADDRESS = setting["sub_address"]        # SubscribeServiceAddress


SECRET_KEY = "test"                     # DataEncryptkey
ALGORITHM = "HS256"                     # EncryptAlgo
ACCESS_TOKEN_EXPIRE_MINUTES = 30        # Token timeout (minutes)


# InstanceizeCryptContextuseatProcesshashPassword
pwd_context: CryptContext = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# FastAPIPasswordauthtool
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

# RPCClient
rpc_client: RpcClient = None


def to_dict(o: object) -> dict:
    """willObjectconvertasDict"""
    data: dict = {}
    for k, v in o.__dict__.items():
        if isinstance(v, Enum):
            data[k] = v.value
        elif isinstance(v, datetime):
            data[k] = str(v)
        else:
            data[k] = v
    return data


class Token(BaseModel):
    """tokenData"""
    access_token: str
    token_type: str


def authenticate_user(current_username: str, username: str, password: str) -> str | Literal[False]:
    """verifyUser"""
    hashed_password = pwd_context.hash(PASSWORD)

    if not secrets.compare_digest(current_username, username):
        return False

    if not pwd_context.verify(password, hashed_password):
        return False

    return username


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Createtoken"""
    to_encode: dict = data.copy()

    if expires_delta:
        expire: datetime = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_access(token: str = Depends(oauth2_scheme)) -> bool:
    """RESTauth"""
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_value = payload.get("sub")
        if username_value is None:
            raise credentials_exception
        username: str = username_value
    except JWTError as err:
        raise credentials_exception from err

    if not secrets.compare_digest(USERNAME, username):
        raise credentials_exception

    return True


# CreateFastAPIapply
app: FastAPI = FastAPI()


@app.get("/")
def index() -> HTMLResponse:
    """GetMain page"""
    index_path: Path = Path(__file__).parent.joinpath("static/index.html")
    with open(index_path) as f:
        content: str = f.read()

    return HTMLResponse(content)


@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:  # noqa: B008
    """User login"""
    auth_result = authenticate_user(USERNAME, form_data.username, form_data.password)
    if not auth_result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token: str = create_access_token(
        data={"sub": auth_result}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/tick/{vt_symbol}")
def subscribe(vt_symbol: str, access: bool = Depends(get_access)) -> None:
    """Subscribe market data"""
    contract: ContractData | None = rpc_client.get_contract(vt_symbol)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found contract{vt_symbol}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    req: SubscribeRequest = SubscribeRequest(contract.symbol, contract.exchange)
    rpc_client.subscribe(req, contract.gateway_name)


@app.get("/tick")
def get_all_ticks(access: bool = Depends(get_access)) -> list:
    """QueryMarket dataInfo"""
    ticks: list[TickData] = rpc_client.get_all_ticks()
    return [to_dict(tick) for tick in ticks]


class OrderRequestModel(BaseModel):
    """OrderRequestmodel"""
    symbol: str
    exchange: Exchange
    direction: Direction
    type: OrderType
    volume: float
    price: float = 0
    offset: Offset = Offset.NONE
    reference: str = ""


@app.post("/order")
def send_order(model: OrderRequestModel, access: bool = Depends(get_access)) -> str:
    """Orderplace order"""
    req: OrderRequest = OrderRequest(**model.__dict__)

    contract: ContractData | None = rpc_client.get_contract(req.vt_symbol)
    if not contract:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found contract{req.symbol} {req.exchange.value}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    vt_orderid: str = rpc_client.send_order(req, contract.gateway_name)
    return vt_orderid


@app.delete("/order/{vt_orderid}")
def cancel_order(vt_orderid: str, access: bool = Depends(get_access)) -> None:
    """Ordercancel order"""
    order: OrderData | None = rpc_client.get_order(vt_orderid)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not found order{vt_orderid}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    req: CancelRequest = order.create_cancel_request()
    rpc_client.cancel_order(req, order.gateway_name)


@app.get("/order")
def get_all_orders(access: bool = Depends(get_access)) -> list:
    """QueryOrderInfo"""
    orders: list[OrderData] = rpc_client.get_all_orders()
    return [to_dict(order) for order in orders]


@app.get("/trade")
def get_all_trades(access: bool = Depends(get_access)) -> list:
    """QueryTradeInfo"""
    trades: list[TradeData] = rpc_client.get_all_trades()
    return [to_dict(trade) for trade in trades]


@app.get("/position")
def get_all_positions(access: bool = Depends(get_access)) -> list:
    """QueryPositionInfo"""
    positions: list[PositionData] = rpc_client.get_all_positions()
    return [to_dict(position) for position in positions]


@app.get("/account")
def get_all_accounts(access: bool = Depends(get_access)) -> list:
    """QueryaccountAccount"""
    accounts: list[AccountData] = rpc_client.get_all_accounts()
    return [to_dict(account) for account in accounts]


@app.get("/contract")
def get_all_contracts(access: bool = Depends(get_access)) -> list:
    """QueryContractInfo"""
    contracts: list[ContractData] = rpc_client.get_all_contracts()
    return [to_dict(contract) for contract in contracts]


# activeStatusWebsocketConnect
active_websockets: list[WebSocket] = []

# globalEventLoop
event_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()


async def get_websocket_access(
    websocket: WebSocket,
    token: str | None = Query(None)
) -> bool:
    """Websocketauth"""
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise credentials_exception
    else:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username_value = payload.get("sub")
        if username_value is None:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise credentials_exception
        username: str = username_value
        if not secrets.compare_digest(USERNAME, username):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise credentials_exception

    return True


# websocketpassData
@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, access: bool = Depends(get_websocket_access)) -> None:
    """Websocket connect process"""
    await websocket.accept()
    active_websockets.append(websocket)

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        active_websockets.remove(websocket)


async def websocket_broadcast(msg: str) -> None:
    """WebsocketDatabroadcast"""
    for websocket in active_websockets:
        await websocket.send_text(msg)


def rpc_callback(topic: str, data: Any) -> None:
    """RPCCallbackFunction"""
    if not active_websockets:
        return

    message_data: dict = {
        "topic": topic,
        "data": to_dict(data)
    }
    msg: str = json.dumps(message_data, ensure_ascii=False)
    asyncio.run_coroutine_threadsafe(websocket_broadcast(msg), event_loop)


@app.on_event("startup")
def startup_event() -> None:
    """applyStartEvent"""
    global rpc_client
    rpc_client = RpcClient()
    rpc_client.callback = rpc_callback
    rpc_client.subscribe_topic("")
    rpc_client.start(REQ_ADDRESS, SUB_ADDRESS)


@app.on_event("shutdown")
def shutdown_event() -> None:
    """applyStopEvent"""
    rpc_client.stop()
