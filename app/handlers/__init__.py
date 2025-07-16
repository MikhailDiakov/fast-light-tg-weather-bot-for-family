from aiogram import Router

from .admin import router as admin_router
from .birthdays import router as birthday_router
from .city import router as city_router
from .settings import router as settings_router
from .start_and_menu import router as start_and_menu_router
from .weather import router as weather_router

router = Router()

router.include_router(start_and_menu_router)
router.include_router(weather_router)
router.include_router(city_router)
router.include_router(admin_router)
router.include_router(birthday_router)
router.include_router(settings_router)
