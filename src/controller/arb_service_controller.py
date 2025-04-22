import traceback
import time

from fastapi import APIRouter, Depends, Request
from dependency_injector.wiring import Provide, inject
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_401_UNAUTHORIZED 

from src.controller.arb_endpoint_filter import EndpointFilter
from src.module.application_container import ApplicationContainer
from src.service.interface.arb_service.arb_service import ARBService
from src.service.interface.arb_service.arb_db_service import ARBDBService
from src.service.interface.arb_service.arb_auth_service import ARBAuthService


arb_router = APIRouter(tags=['Report Chatbot'])
health_check_router = APIRouter(tags=['Health Check'])
   
   
@health_check_router.get('/')
async def health_check() -> JSONResponse:
    return JSONResponse(
        content=jsonable_encoder({
            'message': 'OK', 
            'status_code': HTTP_200_OK}), 
            status_code=HTTP_200_OK
        )

    
    
@arb_router.post('/alpha/chat')
@inject
async def chat(
    request: Request,
    arb_service: ARBService = Depends(Provide[ApplicationContainer.arb_service]),
    arb_db_service: ARBDBService = Depends(Provide[ApplicationContainer.arb_db_service]),
    arb_auth_service: ARBAuthService = Depends(Provide[ApplicationContainer.arb_auth_service])
) -> JSONResponse:
    try:
        params = await request.json()
        
        # Verify API key
        api_key = params['api_key']
        is_authenticated = await arb_auth_service.verify_api_key(api_key)
        if not is_authenticated:
            return JSONResponse(
                content=jsonable_encoder({
                    'status_code': HTTP_401_UNAUTHORIZED,
                    'error_message': 'Unauthorized',
                    'data': None
                }),
                status_code=HTTP_401_UNAUTHORIZED
            )
        
        # Conduct ARB Service
        start_time = time.time()
        response, status_response = await arb_service.chat(
            user_id=params['data']['user_id'], 
            message=params['data']['query']
        )
        end_time = time.time()
        running_time = end_time - start_time
        
        # Insert entity extraction into database
        question = params['data']['query']
        entities = None
        if response.params is not None:
            entities = ', '.join(str(value) for value in response.params.to_dict().values() if value is not None)

        function_called = response.endpoint
                    
        arb_db_service.insert_entity_extraction(
            question=question,
            entities=entities,
            function_called=function_called,
            running_time=running_time
        )
        print(f"🔓 Entity Extraction Inserted into Database Successfully 🎉🎊")
        
        # # Handle error message
        # if status_response.status_code in [104, 209, 200]:
        #     error_message = ""
        # else:
        #     error_message = status_response.message
            
        return JSONResponse(
            content=jsonable_encoder({
                'status_code': HTTP_200_OK,
                'error_message': "",
                'data': response
            }),
            status_code=HTTP_200_OK
        )
        
    except Exception as e:
        
        print(traceback.format_exc())
        return JSONResponse(
                content=jsonable_encoder({
                    'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                    'error_message': traceback.format_exc(),
                }),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

