from decouple import config

# The python manage.py runserver --settings=core.settings.prod, should still work
settings_environment = config("DJANGO_ENVIRONMENT_SETTINGS", "dev")

if settings_environment == "dev":
    print(f"Detected with the settings of '{settings_environment}', running the development settings")
    from .dev import *  # noqa: F403 F401
elif settings_environment == "prod":
    from .prod import *  # noqa: F403 F401
    print(f"Detected with the settings of '{settings_environment}', running the production settings")
else:
    from .dev import *  # noqa: F403 F401
    print(f"Settings with a value of '{settings_environment}' is not defined, defaulting with development settings")
