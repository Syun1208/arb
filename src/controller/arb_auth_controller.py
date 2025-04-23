import traceback
import secrets
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED


from src.service.interface.arb_service.arb_auth_service import ARBAuthService
from src.module.application_container import ApplicationContainer
from src.utils.constants import DEPARTMENT_MAPPING_NAME

auth_router = APIRouter(tags=["API Key Authentication & Authorization"])


@auth_router.get('/{department}/generate_key')
@inject
async def generate_key(
    department: str,
    arb_auth_service: ARBAuthService = Depends(Provide[ApplicationContainer.arb_auth_service])
) -> JSONResponse:
    
    try:
        # Generate API key
        if department.capitalize() in DEPARTMENT_MAPPING_NAME:
            api_key = await arb_auth_service.generate_api_key(department)

            print(f'🏢 Department: {department}')
            print(f'🔑 API Key: {api_key}')
            
            return JSONResponse(
                content=jsonable_encoder({
                    "status_code": HTTP_200_OK, 
                    "error_message": "",
                    "data": {
                        "api_key": api_key
                    }
                }), 
                status_code=HTTP_200_OK
            )
            
        return JSONResponse(
                content=jsonable_encoder({
                    "status_code": HTTP_400_BAD_REQUEST, 
                    "error_message": "Invalid department",
                    "data": None
                }),
                status_code=HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        
        print(traceback.format_exc())
        return JSONResponse(
                content=jsonable_encoder({
                    'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                    'error_message': traceback.format_exc(),
                    "data": None
                }),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
@auth_router.get("/authenticate")
@inject
async def authenticate(
    api_key: str,
    arb_auth_service: ARBAuthService = Depends(Provide[ApplicationContainer.arb_auth_service])
) -> JSONResponse:
    
    try:
        is_authenticated = await arb_auth_service.verify_api_key(api_key)
        
        if is_authenticated:
            return JSONResponse(
                content=jsonable_encoder({
                    "status_code": HTTP_200_OK, 
                    "error_message": "",
                    "data": {
                        "message": "Authenticated"
                    }
                }),
                status_code=HTTP_200_OK
            )
        else:
            return JSONResponse(
                content=jsonable_encoder({
                    "status_code": HTTP_401_UNAUTHORIZED, 
                    "error_message": "Unauthenticated",
                    "data": None
                }),
                status_code=HTTP_401_UNAUTHORIZED
            )
    
    except Exception as e:
        
        print(traceback.format_exc())
        return JSONResponse(
                content=jsonable_encoder({
                    'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                    'error_message': traceback.format_exc(),
                    "data": None
                }),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

@auth_router.delete("/{department}/delete_key")
@inject
async def delete_key(
    department: str,
    arb_auth_service: ARBAuthService = Depends(Provide[ApplicationContainer.arb_auth_service])
) -> JSONResponse:
    
    try:
        await arb_auth_service.delete_api_key(department)
        print(f'🔑 API Key Deleted for {department}')
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_200_OK, 
                "error_message": "",
                "data": {
                    "message": "API Key Deleted"
                }
            }),
            status_code=HTTP_200_OK
        )
        
    except Exception as e:
        
        print(traceback.format_exc())
        return JSONResponse(
                content=jsonable_encoder({
                    'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                    'error_message': traceback.format_exc(),
                    "data": None
                }),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        
@auth_router.get("/{department}/get_key")
@inject
async def get_key(
    department: str,
    arb_auth_service: ARBAuthService = Depends(Provide[ApplicationContainer.arb_auth_service])
) -> JSONResponse:
    
    try:
        api_key = await arb_auth_service.get_api_key(department)
        print(f"🔑 Get API Key for {department}: {api_key}")
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_200_OK, 
                "error_message": "",
                "data": {
                    "api_key": api_key
                }
            }),
            status_code=HTTP_200_OK
        )
        
    except Exception as e:
        
        print(traceback.format_exc())
        return JSONResponse(
                content=jsonable_encoder({
                    'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                    'error_message': traceback.format_exc(),
                    "data": None
                }),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
    
@auth_router.put("/{department}/update_key")
@inject
async def update_key(
    department: str,
    request: Request,
    arb_auth_service: ARBAuthService = Depends(Provide[ApplicationContainer.arb_auth_service])
) -> JSONResponse:
    
    try:
        params = await request.json()
        if 'api_key' in list(params.keys()):
            api_key = params['api_key']
        else:
            api_key = secrets.token_urlsafe(32)
        
        await arb_auth_service.update_api_key(department, api_key)
        print(f"🔑 Update API Key for {department}: {api_key}")
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_200_OK, 
                "error_message": "",
                "data": {
                    "api_key": api_key,
                    "message": "API Key Updated"
                }
            }),
            status_code=HTTP_200_OK
        )
        
    except Exception as e:
        
        print(traceback.format_exc())
        return JSONResponse(
                content=jsonable_encoder({
                    'status_code': HTTP_500_INTERNAL_SERVER_ERROR,
                    'error_message': traceback.format_exc(),
                    "data": None
                }),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )