from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

class APIResponse(BaseModel):
    code: bool = Field("0000", example="0000")
    msg: str = Field("操作成功", example="操作成功")
    content: object = Field({}, example="{}")

def gen_response(res: APIResponse = None, httpCode: int = 200):
    if res is None:
        res = APIResponse(code="9999", msg="未知响应", content={})
    return JSONResponse(
        status_code=httpCode,
        content={
            "code": res.code,
            "msg": res.msg,
            "content": res.content
        }
    )


