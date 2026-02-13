class ShortnerBaseException(Exception):
    """
    Базовый класс для всех исключений в приложении сокращения ссылок.
    Наследуется от встроенного класса Exception.
    """

    pass


class NoLongUrlFoundError(ShortnerBaseException):
    """
    Исключение, возникающее при попытке найти оригинальный URL по несуществующему короткому идентификатору.
    Наследуется от ShortnerBaseException.
    """

    pass


class SlugAlreadyExistsError(ShortnerBaseException):
    """
    Исключение, возникающее при попытке создать короткий идентификатор, который уже существует в базе данных.
    Наследуется от ShortnerBaseException.
    """

    pass
