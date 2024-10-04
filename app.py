from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

import os
import jwt

from microservices.user import router as user_router
from microservices.customer import router as customer_router
from microservices.provider import router as provider_router
from microservices.product import router as product_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "https://liav.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")


def verify_token(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Token")


app.include_router(user_router, prefix='/user',
                   dependencies=[Depends(verify_token)])
app.include_router(customer_router, prefix='/customer',
                   dependencies=[Depends(verify_token)])
app.include_router(provider_router, prefix='/provider',
                   dependencies=[Depends(verify_token)])
app.include_router(product_router, prefix='/product',
                   dependencies=[Depends(verify_token)])
