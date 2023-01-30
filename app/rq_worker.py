from config import settings

REDIS_URL = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}'
QUEUES = [settings.REDIS_QUEUE]
