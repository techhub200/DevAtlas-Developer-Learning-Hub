from fastapi import FastAPI
import fastapi.exceptions as status

from src.api.auth.routes import auth_router
from src.Users.routes import User_rotues
from src.api.technologies.routes import tech_router
from src.api.course.routes import course_router
from src.api.recommendations.routes import recommendations_router
from fastapi.responses import JSONResponse
from src.Error_Handling.errors import register_error_handlers
from src.Middleware.middleware import register_middleware

app = FastAPI(title="DevAtlas API")
register_error_handlers(app)
register_middleware(app)
app.include_router(auth_router, prefix="/app/auth", tags=["Authentication"])
app.include_router(User_rotues, prefix="/app/users", tags=["Users"])
app.include_router(tech_router, prefix="/app/tech", tags=["Technologies"])
app.include_router(course_router, prefix="/app/course", tags=["Courses"])
app.include_router(recommendations_router, prefix="/app/recommendations", tags=["Recommendations"])
