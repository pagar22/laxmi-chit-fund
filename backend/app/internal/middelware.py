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


def set_protected_routes(app: FastAPI):
    if not hasattr(app.state, "protected_routes"):
        protected_routes = {}
        protected_methods = ["POST", "PATCH", "DELETE"]
        for route in app.routes:
            if any(method in protected_methods for method in route.methods):
                protected_routes[route.path] = route.methods
        setattr(app.state, "protected_routes", protected_routes)


def app_middleware(app: FastAPI):
    cors(app)
    rate_limiting(app)
    set_protected_routes(app)

    @app.middleware("http")
    async def validate_cud_api_key(request: Request, call_next):
        method, route = request.method, request.url.path
        protected_routes = getattr(app.state, "protected_routes")

        if route in protected_routes and method in protected_routes[route]:
            log.info(f"🔑 CUD API Key needed for {method} to {route}")
            cud_api_key = access_secret_manager("CUD_API_KEY", "latest")
            request_api_key = request.headers.get("X-CUD-Api-Key")
            if not request_api_key:
                return JSONResponse(status_code=401, content="Unauthenticated")
            if request_api_key != cud_api_key:
                return JSONResponse(
                    status_code=403, content="Unauthorized Restricted Method"
                )
        return await call_next(request)
