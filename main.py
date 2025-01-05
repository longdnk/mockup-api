from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from user_entity import UserEntity, User
from params import param_compile
from typing import Optional
from typing import List
import uuid
import uvicorn
import time

app = FastAPI()

user_list: List[UserEntity] = []


@app.get("/")
async def root():
    return {"code": 200, "message": "Check health OK Done"}


@app.get("/users", status_code=status.HTTP_200_OK)
async def list_users(page: int = 1, limit: int = 10):
    time.sleep(1)
    # Kiểm tra số lượng limit không quá lớn
    if limit > 100:
        limit = 100  # Giới hạn tối đa là 100 người dùng mỗi trang

    # Tính toán phạm vi phân trang
    start = (page - 1) * limit
    end = start + limit

    # Lấy danh sách người dùng trong phạm vi phân trang
    paginated_users = user_list[start:end]

    # Định dạng dữ liệu phản hồi
    response_data = {
        "code": status.HTTP_200_OK,
        "message": "Fetch users with pagination success",
        "data": paginated_users,
        "page": page,
        "limit": limit,
        "total": len(user_list),  # Tổng số người dùng
        "total_pages": (len(user_list) // limit)
        + (1 if len(user_list) % limit > 0 else 0),
    }

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def get_detail(user_id: str):
    time.sleep(1)
    # Tìm kiếm người dùng theo ID
    user_detail = next((user for user in user_list if user["id"] == user_id), None)

    # Nếu không tìm thấy, trả về lỗi 404
    if not user_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User is not exist in list !!!",
        )

    response_data = {
        "code": status.HTTP_200_OK,
        "message": "Get user detail success",
        "data": user_detail,
    }

    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)

    # API tìm kiếm người dùng với các tham số tìm kiếm và sắp xếp


@app.get("/search", status_code=status.HTTP_200_OK)
async def search_users(
    name: Optional[str] = None,
    address: Optional[str] = None,
    age: Optional[int] = None,
    sort_by: Optional[str] = "name",  # Trường sắp xếp (mặc định là 'name')
    order: Optional[str] = "asc",  # Thứ tự sắp xếp (mặc định là 'asc')
):
    time.sleep(1)
    # Lọc danh sách người dùng theo các tham số tìm kiếm
    filtered_users = user_list
    if name:
        filtered_users = [
            user for user in filtered_users if name.lower() in user["name"].lower()
        ]
    if address:
        filtered_users = [
            user
            for user in filtered_users
            if address.lower() in user["address"].lower()
        ]
    if age is not None:
        filtered_users = [user for user in filtered_users if user["age"] == age]

    # Sắp xếp kết quả theo trường và thứ tự chỉ định
    if sort_by and order:
        if sort_by not in ["name", "address", "age"]:
            raise HTTPException(status_code=400, detail="Invalid sort field")

        reverse_order = True if order == "desc" else False
        filtered_users = sorted(
            filtered_users, key=lambda x: x[sort_by], reverse=reverse_order
        )

    response_data = {
        "code": status.HTTP_200_OK,
        "message": "Search results",
        "data": filtered_users,
    }
    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def add_user(user: User):
    time.sleep(1)
    global user_list
    user.id = str(uuid.uuid4())
    new_user = UserEntity(**user.dict())

    user_list.append(new_user.dict())

    response_data = {
        "code": status.HTTP_201_CREATED,
        "message": "Create new user success",
        "data": new_user.dict(),
    }
    return JSONResponse(content=response_data, status_code=status.HTTP_201_CREATED)


@app.put("/users/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user: User):
    time.sleep(1)
    global user_list
    # Tìm người dùng trong danh sách
    user_detail = next((user for user in user_list if user["id"] == user_id), None)

    if not user_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    # Cập nhật thông tin người dùng
    user_detail["name"] = user.name
    user_detail["address"] = user.address
    user_detail["age"] = user.age

    response_data = {
        "code": status.HTTP_200_OK,
        "message": "User updated successfully",
        "data": user_detail,
    }
    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


@app.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: str):
    time.sleep(1)
    global user_list
    # Tìm người dùng trong danh sách
    user_detail = next((user for user in user_list if user["id"] == user_id), None)

    if not user_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found!"
        )

    # Xóa người dùng khỏi danh sách
    user_list = [user for user in user_list if user["id"] != user_id]

    response_data = {
        "code": status.HTTP_200_OK,
        "message": "User deleted successfully",
        "data": {"id": user_id},
    }
    return JSONResponse(content=response_data, status_code=status.HTTP_200_OK)


# Hàm chung để tạo response lỗi
def generate_error_response(code: int, message: str, error: dict = {}):
    return JSONResponse(
        status_code=code, content={"code": code, "message": message, "error": error}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    error_details = {}
    for error in exc.errors():
        field = ".".join(map(str, error["loc"][1:]))
        error_details[field] = error["msg"]

    return generate_error_response(
        status.HTTP_422_UNPROCESSABLE_ENTITY, "Validation Error", error_details
    )


@app.exception_handler(HTTPException)
async def not_found_exception_handler(request, exc: HTTPException):
    if exc.status_code == 404:
        error_detail = exc.detail or "No further details available"
        return generate_error_response(
            status.HTTP_404_NOT_FOUND,
            "Resource not found",
            error={"detail": error_detail},
        )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.status_code,
            "message": exc.detail or "An error occurred",
            "error": {},
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=param_compile.host,
        port=param_compile.port,
        reload=param_compile.reload,
        workers=param_compile.workers,
        log_level=param_compile.log_level,
        limit_max_requests=param_compile.limit_max_requests,
        limit_concurrency=param_compile.limit_concurrency,
        backlog=param_compile.backlog,
        ssl_keyfile=param_compile.ssl_keyfile,
        ssl_certfile=param_compile.ssl_certfile,
    )
