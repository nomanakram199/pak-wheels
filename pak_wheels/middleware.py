import time
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class APIPerformanceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        if settings.DEBUG:
            logger.info(
                "Path: %s | Method: %s | Status: %s | Duration: %.4fs",
                request.path,
                request.method,
                response.status_code,
                duration,
            )
        return response
