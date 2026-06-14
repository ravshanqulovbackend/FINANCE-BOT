from .add import router as add_router
from .bonus import router as bonus_router
from .categories import router as categories_router
from .common import router as common_router
from .history import router as history_router
from .start import router as start_router
from .stats import router as stats_router

routers = (
    common_router,
    start_router,
    add_router,
    stats_router,
    history_router,
    categories_router,
    bonus_router,
)
