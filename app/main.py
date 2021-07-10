from app.core.config import get_settings
from app.fastapi import get_application

settings = get_settings()

app = get_application(settings)
