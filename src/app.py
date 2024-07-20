from typing import Dict, Any
try:
    from fastapi import FastAPI
    from pydantic import BaseModel, Field
except Exception as e:
    print(f"Error! Some modules are missing: {e}")


app = FastAPI()

class PayloadBody(BaseModel):
    object: dict
    # ... is a special Pydantic syntax that means "no default value"
    max_depth: int = Field(..., gt=0, description="Must be a positive integer")

# during deployment, the load balancer can use this endpoint to check if service is up and running
@app.get("/")
async def helthcheck():
    return {"status": "OK"}

def _validate_object(obj: dict, max_depth: int) -> bool:
    """
    Validate each value in the object recursively - examples in test_validate.py
    Return False if any value has depth more than max_depth
    """
    # already exceeded max_depth - no need to call this function again
    if max_depth < 1:
        return False
    for value in obj.values():
        # if value is a dictionary and not empty - case for another depth level
        if isinstance(value, dict) and value:
            if not _validate_object(value, max_depth - 1):
                return False
    return True

@app.post('/validate/')
async def validate_object(payload: PayloadBody) -> bool:
    """
    Endpoint to validate if object depth exceeds max_depth
    """
    # empty object has 0 depth and it is valid: no depth in it more than minimal depth=1
    if not payload.object:
        return True
    return _validate_object(payload.object, payload.max_depth)

def _truncate_object(obj: Any, max_depth: int) -> Any:
    """
    Truncate object to max_depth recursively - examples in test_truncate.py
    Return the object with all values truncated to max_depth
    """
    if max_depth < 1 or not isinstance(obj, dict):
        return {}
    truncated = {}
    for key, value in obj.items():
        if isinstance(value, dict):
            truncated[key] = _truncate_object(value, max_depth - 1)
        # keep the value as is for other types (not dict)
        else:
            truncated[key] = value
    return truncated

@app.post('/truncate/')
async def truncate_object(payload: PayloadBody) -> Dict[str, Any]:
    """
    Endpoint to truncate object to max_depth
    """
    truncated_object = _truncate_object(payload.object, payload.max_depth)
    return truncated_object
