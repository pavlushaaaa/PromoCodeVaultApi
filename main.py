from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.api.endpoints import user, product, token, voucher, voucher_code, analytics
from app.schemas import DefaultSuccessResponse

tags_metadata = [
    {
        "name": "users",
        "description": "Operations related to users",
    },
    {
        "name": "products",
        "description": "Operations related to products",
    },
    {
        "name": "tokens",
        "description": "Tokens related to products",
    },
    {
        "name": "index",
    },
]

app = FastAPI(
    title="PromoCodeVault API",
    description="This is project to help businesses implement discounts and vouchers logic",
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)
app.include_router(user.router)
app.include_router(product.router)
app.include_router(token.router)
app.include_router(voucher.router)
app.include_router(voucher_code.router)
app.include_router(analytics.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="PromoCodeVault API",
        version="1.0.0",
        description="This is project to help businesses implement discounts and vouchers logic",
        routes=app.routes,
        license_info={
            "name": "Apache 2.0",
            "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        },
    )
    openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"]["flows"]["password"]["tokenUrl"] = "token"
    # Remove client_id and client_secret from the OpenAPI schema
    openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"]["flows"]["password"].pop("client_id", None)
    openapi_schema["components"]["securitySchemes"]["OAuth2PasswordBearer"]["flows"]["password"].pop("client_secret", None)
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # Allows the FE to communicate with the BE.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=['index'])
async def get():
    return DefaultSuccessResponse()
