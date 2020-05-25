import environ

# Django environ settings
# https://django-environ.readthedocs.io/en/latest/
# there should be a file called local_settings_example with this template
#

env = environ.Env(
    DEBUG=(bool, True),
    SECRET_KEY=(str, "dg#0^cvrrb_c-%b@9k08*w6qgq&w0n+)eol=3er$!ax_1dh!9u"),
    ALLOWED_HOSTS=(str, "*"),
    CELERY_TIMEZONE=(str, "UTC"),
    POSTGRES_DB=(str, ""),
    POSTGRES_USER=(str, ""),
    POSTGRES_PASSWORD=(str, ""),
    POSTGRES_HOST=(str, ""),
    POSTGRES_PORT=(int, None),
    REDIS_HOST=(str, "redis"),
    REDIS_PORT=(int, 6379),
    REDIS_DB=(int, 1),
    AWS_SES_ACCESS_KEY_ID=(str, ""),
    AWS_SES_SECRET_ACCESS_KEY=(str, ""),
    AWS_SES_REGION=(str, ""),
    AWS_ACCESS_KEY_ID=(str, ""),
    AWS_SECRET_ACCESS_KEY=(str, ""),
    AWS_STORAGE_BUCKET_NAME=(str, ""),
    CDN_DOMAIN=(str, ""),
    SENTRY_DSN=(str, ""),
    SENTRY_ENVIRONMENT=(str, ""),
    MAIN_HOST=(str, ""),
)
