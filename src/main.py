from fastapi import FastAPI
from src.api.auth.routes import auth_router
from src.Users.routes import User_rotues
from src.api.technologies.routes import tech_router
from src.api.course.routes import course_router


app = FastAPI(title="DevAtlas API")

app.include_router(auth_router, prefix="/app/auth", tags=["Authentication"])
app.include_router(User_rotues, prefix="/app/users", tags=["Users"])
app.include_router(tech_router, prefix="/app/tech", tags=["Technologies"])
app.include_router(course_router, prefix="/app/course", tags=["Courses"])
