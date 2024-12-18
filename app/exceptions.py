from fastapi import HTTPException, status


class BookingException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class IncorrectEmailOrPasswordException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверная почта или пароль"


class TokenExpiredException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Срок действия токена истек"


class TokenAbsentException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(BookingException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"

class UserIsNotPresentException(BookingException):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Пользователь не существует"

class PoolFullyBookedException(BookingException):
    status_code=status.HTTP_409_CONFLICT
    detail="Не осталось свободных бассейнов"

class PoolCannotBeBookedException(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось записаться ввиду неизвестной ошибки"

class TimeFromCannotBeAfterTimeToException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Время начала не может быть позже времени окончания"

class CannotBookSpaceForLongPeriodException(BookingException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Невозможно забронировать бассейн сроком более суток"

class CannotAddDataToDatabaseException(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось добавить запись"

class CannotProcessCSVException(BookingException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Не удалось обработать CSV файл"

class IncorrectUserRoleException(BookingException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав для данного действ"
