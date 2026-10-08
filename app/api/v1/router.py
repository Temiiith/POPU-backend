from fastapi import APIRouter

from app.api.v1.agent import router as agent_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.health import router as health_router
from app.api.v1.scenarios import router as scenarios_router
from app.api.v1.signals import router as signals_router
from app.api.v1.llm import router as llm_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(scenarios_router)
api_router.include_router(analysis_router)
api_router.include_router(agent_router)
api_router.include_router(signals_router)
api_router.include_router(llm_router)