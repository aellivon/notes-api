import tempfile
import os
from pathlib import Path

from .base import *  # noqa: F403

BASE_DIR = Path(__file__).resolve().parent.parent.parent


INSTALLED_APPS += (  # noqa: F405
    "naomi",
)

# To avoid sending data real clients in the future, do a naomi backend
EMAIL_BACKEND = "naomi.mail.backends.naomi.NaomiBackend"
EMAIL_FILE_PATH = tempfile.gettempdir()

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
