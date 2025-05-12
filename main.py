import os
import sys
import uvicorn
import warnings

warnings.filterwarnings('ignore')

import logging

import psutil
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from dependency_injector.wiring import inject

from src.utils.debugger import pretty_errors
from src.module.application_container import ApplicationContainer
from src.controller.arb_service_controller import arb_router, health_check_router
from src.controller.arb_auth_controller import auth_router
from src.controller.arb_nosql_controller import nosql_router
from src.controller.arb_vector_db_controller import vector_db_router
from src.controller import arb_service_controller, arb_auth_controller, arb_nosql_controller, arb_vector_db_controller
from src.utils.utils import load_yaml



@inject
def create_app(env: str) -> FastAPI:
    config = load_yaml(f"config/{env}.yml")
    app = FastAPI(
        title=f"{config['default']['app_name']} | {config['default']['env']}", 
        description="""<h2>Made by S.A.I team (Key members: Hani, Leon)</h2>"""
    )
    
    application_container = ApplicationContainer()
    application_container.wire(modules=["src.module.application_container"])

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    env = os.environ['APP_MODE']

    modules = [
        sys.modules[__name__]
        , arb_service_controller
        , arb_auth_controller
        , arb_nosql_controller
        , arb_vector_db_controller
    ]
    # Load all report configs at once
    report_files = config['report_configs']
    for report_file in report_files:
        application_container.report_config.from_json(report_file)

    # Load all service configs at once
    service_files = config['service_configs']
    service_files.append(f"config/{env}.yml")
    for service_file in service_files:
        application_container.service_config.from_yaml(service_file)
        
    application_container.wire(modules)
    
    app.container = application_container
    app.include_router(health_check_router, tags=['Health Check'])
    app.include_router(arb_router, prefix="/api/v1", tags=['Report Chatbot'])
    app.include_router(auth_router, prefix="/api/v1", tags=['API Key Authentication & Authorization'])
    app.include_router(nosql_router, prefix="/api/v1", tags=['NoSQL Database'])
    app.include_router(vector_db_router, prefix="/api/v1", tags=['Vector DB Controller'])

    logging.info("Wire completed")
    logging.basicConfig(level=logging.INFO)

    return app, config



os.environ['APP_MODE'] = sys.argv[1] if len(sys.argv) > 1 else 'development'
app, config = create_app(env=os.environ['APP_MODE']) 

if __name__ == "__main__":   
    uvicorn.run(
        app='main:app', 
        host=config['server']['http']['host'], 
        port=int(config['server']['http']['port']), 
        reload=True,
        workers=psutil.cpu_count(logical=False) - 2, 
        timeout_keep_alive=20
    )