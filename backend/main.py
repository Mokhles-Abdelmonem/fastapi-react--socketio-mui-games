import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth.exceptions import AuthJWTException

from routes.user import users_router
from routes.games import games_router
from routes.auth import auth_router
from sockets.server import sio_app
app = FastAPI()

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(games_router)



@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )



################# Socket IO #################

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.mount('/', app=sio_app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
