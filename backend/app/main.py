from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, tenants, rooms, meters, usage, invoices, payments
from .security.rbac import RBACMiddleware


app = FastAPI(title="Dom Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RBACMiddleware)

app.include_router(auth.router)
app.include_router(tenants.router)
app.include_router(rooms.router)
app.include_router(meters.router)
app.include_router(usage.router)
app.include_router(invoices.router)
app.include_router(payments.router)


@app.get("/healthz")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
