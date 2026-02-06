from fastapi import Request, HTTPException

def require_admin(request: Request):
    admin = request.cookies.get("admin")
    if not admin:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return admin
