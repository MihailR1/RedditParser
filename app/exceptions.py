from fastapi import HTTPException, status


class BaseExcep(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class ConnectionProblemToReddit(BaseExcep):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Ошибка подключения к апи"


class WrongSubbredditName(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Имя сабреддита не существует"
