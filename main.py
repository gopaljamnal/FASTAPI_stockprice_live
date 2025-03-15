from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests
import jwt
import datetime
from database import StockData, SessionLocal
from passlib.context import CryptContext

app = FastAPI()

API_KEY = "3WGRNW7O4DZRMF3D"
BASE_URL = "https://www.alphavantage.co/query"

# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy user database (replace with real DB in production)
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": pwd_context.hash("password123"),  # Store hashed password
    }
}

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.get("/stock/{symbol}")
def get_stock_price(symbol: str):
    """Fetch real-time stock price"""
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "5min",
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

# 🔹 Token Generation (Now Requires Username & Password)
@app.post("/token")
def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and generate JWT token"""
    user = fake_users_db.get(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    payload = {
        "sub": form_data.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# 🔹 Token Verification Function
def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify JWT token and return username"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# 🔹 Protected Endpoint (Requires JWT)
@app.post("/store_stock/{symbol}")
def store_stock_data(symbol: str, username: str = Depends(verify_token)):
    """Fetch stock price and store it in the database (only for authenticated users)"""
    session = SessionLocal()
    data = get_stock_price(symbol)

    if "Time Series (5min)" not in data:
        return {"error": "Invalid symbol or API limit exceeded"}

    latest_time = list(data["Time Series (5min)"].keys())[0]
    latest_price = float(data["Time Series (5min)"][latest_time]["1. open"])

    stock_entry = StockData(symbol=symbol, price=latest_price)
    session.add(stock_entry)
    session.commit()
    session.close()

    return {"message": f"Stock data saved by {username}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
