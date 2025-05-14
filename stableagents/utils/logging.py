import logging 

from typing import Any

from starlette.applications import Starlette

##

logger = logging.getLogger(__name__)

class StableAgentsServer:
    pass


def start(self, **kwargs: Any):
    logger.info('Start Server')
    import uvicorn




    uvicorn.run(self.app(), **kwargs)