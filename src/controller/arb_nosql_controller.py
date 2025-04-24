import traceback
import secrets
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide
from fastapi.encoders import jsonable_encoder
from fastapi import Depends
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from src.module.application_container import ApplicationContainer
from src.service.interface.arb_service.arb_db_service import ARBDBService

nosql_router = APIRouter(tags=["NoSQL Database"])


@nosql_router.post("/insert")
@inject
async def insert(
    request: Request,
    arb_db_service: ARBDBService = Depends(Provide[ApplicationContainer.arb_db_service])
) -> JSONResponse:
    try:
        params = await request.json()
        user_id = params['user_id']
        metadata = params['metadata']
        
        arb_db_service.insert(user_id, metadata)
        
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_200_OK,
                "message": "Data inserted successfully"
            }),
            status_code=HTTP_200_OK
        )
    
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Failed to insert data"
            }),
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    
@nosql_router.get("/get")
@inject
async def get(
    user_id: str,
    arb_db_service: ARBDBService = Depends(Provide[ApplicationContainer.arb_db_service])
) -> JSONResponse:  
    try:
        data = arb_db_service.get(user_id)
        
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_200_OK,
                "message": "Data retrieved successfully",
                "data": data
            }),
            status_code=HTTP_200_OK
        )
    
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Failed to retrieve data"
            }),
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    
@nosql_router.put("/update")
@inject
async def update(
    user_id: str,
    request: Request,
    arb_db_service: ARBDBService = Depends(Provide[ApplicationContainer.arb_db_service])
) -> JSONResponse:  
    try:
        params = await request.json()
        metadata = params['metadata']
        
        arb_db_service.update(user_id, metadata)
        
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_200_OK,
                "message": "Data updated successfully"
            }),
            status_code=HTTP_200_OK
        )
    
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Failed to update data"
            }),
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    
@nosql_router.delete("/delete")
@inject
async def delete(
    user_id: str,
    arb_db_service: ARBDBService = Depends(Provide[ApplicationContainer.arb_db_service])
) -> JSONResponse:
    try:
        arb_db_service.delete(user_id)
        
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_200_OK,
                "message": "Data deleted successfully"
            }),
            status_code=HTTP_200_OK
        )

    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            content=jsonable_encoder({
                "status_code": HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Failed to delete data"
            }),
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        )