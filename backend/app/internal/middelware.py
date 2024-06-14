from app.internal.config import access_secret_manager
from app.internal.firebase import log
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIASGIMiddleware
from slowapi.util import get_remote_address


def cors(app: FastAPI):
    # TODO Update origins to FE URL
    origins = ["*", "https://localhost:19006"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def rate_limiting(app: FastAPI):
    limiter = Limiter(key_func=get_remote_address, default_limits=["120/minute"])
    setattr(app.state, "limiter", limiter)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIASGIMiddleware)


def app_middleware(app: FastAPI):
    cors(app)
    rate_limiting(app)

    @app.middleware("http")
    async def validate_cud_api_key(request: Request, call_next):
        protected_methods = ["POST", "PATCH", "PUT", "DELETE"]
        method, route = request.method, request.url.path
        if method in protected_methods:
            # for protected_route in app.routes:
            #     match, scope = protected_route.matches(request)
            #     if match == Match.FULL: # from starlette.routing import Match
            log.info(f"🔒 CUD API Key needed for {method} to {route}")
            cud_api_key = access_secret_manager("CUD_API_KEY", "latest")
            request_api_key = request.headers.get("X-CUD-Api-Key")
            if not request_api_key:
                return JSONResponse(
                    status_code=401, content="Unauthenticated, restricted method"
                )
            if request_api_key != cud_api_key:
                return JSONResponse(status_code=403, content="Unauthorised, bad key")
            log.info(f"🔑 CUD API Key validated")
        return await call_next(request)
