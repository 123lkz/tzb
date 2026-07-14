class RetryMiddleware:
    def process_response(self, request, response, spider):
        # 重试逻辑实现
        return response 