import traceback
import concurrent.futures
import multiprocessing

from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR 

from src.module.application_container import ApplicationContainer
from src.service.interface.arb_slave_agent.abbreviation_recognizer_agent import AbbreviationRecognizerAgent


vector_db_router = APIRouter(tags=['Vector DB Controller'])

@vector_db_router.get('/index')
@inject
async def index(
    abbreviation_recognizer_agent: AbbreviationRecognizerAgent = Depends(Provide[ApplicationContainer.abbreviation_recognizer_agent])
) -> JSONResponse:
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() - 5) as executor:
            entity_future = executor.submit(abbreviation_recognizer_agent.index_entity_abbreviation)
            report_future = executor.submit(abbreviation_recognizer_agent.index_report_abbreviation)
            entity_future.result()
            report_future.result()
        
        return JSONResponse(
            content=jsonable_encoder({
                'message': 'Indexing successfully',
                'status_code': HTTP_200_OK
            }),
            status_code=HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content=jsonable_encoder({
                'message': 'Failed to index entity',
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR
            }),
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )

@vector_db_router.get('/index/report')
@inject
async def index_report(
    abbreviation_recognizer_agent: AbbreviationRecognizerAgent = Depends(Provide[ApplicationContainer.abbreviation_recognizer_agent])
) -> JSONResponse:
    try:
        abbreviation_recognizer_agent.index_report_abbreviation()
        return JSONResponse(
            content=jsonable_encoder({
                'message': 'Report indexed successfully',
                'status_code': HTTP_200_OK
            }),
            status_code=HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content=jsonable_encoder({
                'message': 'Failed to index report',
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR
            }),
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )


@vector_db_router.get('/index/entity')
@inject
async def index_entity(
    abbreviation_recognizer_agent: AbbreviationRecognizerAgent = Depends(Provide[ApplicationContainer.abbreviation_recognizer_agent])
) -> JSONResponse:
    try:
        abbreviation_recognizer_agent.index_entity_abbreviation()
        return JSONResponse(
            content=jsonable_encoder({
                'message': 'Entity indexed successfully',
                'status_code': HTTP_200_OK
            }),
            status_code=HTTP_200_OK
        )
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(
            content=jsonable_encoder({
                'message': 'Failed to index entity',
                'status_code': HTTP_500_INTERNAL_SERVER_ERROR
            }),
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )


