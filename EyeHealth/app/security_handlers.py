from abc import ABC, abstractmethod

# Абстрактный класс и обработчики

class SecurityHandler(ABC):
    def __init__(self, next_handler=None):
        self.next_handler = next_handler

    @abstractmethod
    def handle_request(self, request):
        pass


class AuthenticationHandler(SecurityHandler):
    def handle_request(self, request):
        if 'token' not in request:
            print("Ошибка: Отсутствует токен аутентификации.")
            return
        print("Аутентификация прошла успешно.")
        if self.next_handler:
            self.next_handler.handle_request(request)


class AuthorizationHandler(SecurityHandler):
    def handle_request(self, request):
        if 'role' not in request or request['role'] != 'admin':
            print("Ошибка: У пользователя нет прав на доступ.")
            return
        print("Авторизация прошла успешно.")
        if self.next_handler:
            self.next_handler.handle_request(request)


class CSRFProtectionHandler(SecurityHandler):
    def handle_request(self, request):
        if 'csrf_token' not in request:
            print("Ошибка: Отсутствует CSRF токен.")
            return
        print("Защита от CSRF прошла успешно.")
        if self.next_handler:
            self.next_handler.handle_request(request)


class SQLInjectionProtectionHandler(SecurityHandler):
    def handle_request(self, request):
        if 'query' in request and "DROP" in request['query'].upper():
            print("Ошибка: Обнаружена попытка SQL-инъекции.")
            return
        print("Защита от SQL-инъекций прошла успешно.")
        if self.next_handler:
            self.next_handler.handle_request(request)
