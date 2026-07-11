from fastapi import APIRouter,HTTPException,status

User_rotues=APIRouter()

@User_rotues.get("/Profile")
async def Get_User_Profile():
    pass

@User_rotues.put("/Update_Profile")
async def Update_Profile():
    pass


@User_rotues.delete("/Delete_Profile")
async def Delete_Profile():
    pass


@User_rotues.put("/Update_Picture")
async def Get_User_Profile():
    pass

@User_rotues.get("/Profile/{user_id}")
async def Get_User_Profile_by_id():
    pass

