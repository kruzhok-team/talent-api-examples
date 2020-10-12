# Примеры работы с API платформы «Талант»

Это примеры на `python`, демонстрирующие механизмы авторизации и получения токена на различных flow. После получения токена вы сможете взаимодействовать с методами API.

Полный перчень методов API платформы и документацию по использованию вы можете найти по ссылке [https://talent.kruzhok.org/api/docs/](https://talent.kruzhok.org/api/docs/).

## Требования для работы примеров
* python 3.6
* poetry

В качестве клиента, используется библиотека [`Authlib`](https://authlib.org/).

## Содержимое репозитория
|Пример|Описание|
|--|--|
| `client_credential.py` | Client Credential Flow (используется для Server-to-Server авторизации)|
| `authorization_code_flow.py` | Authorization Code Flow, самый распространенный сценарий с подтверждением доступа от пользователя |
| `authorization_code_flow_with_pkce.py` | Authorization Code with PKCE, расширение ACF c дополнительной защитой, используется для авторизации SPA и мобильных приложений, в примере так же добавлен запрос `openid` скоупа |

## Установка
```bash
# Ставим poetry
pip install poetry

# Ставим зависимости
poetry install
```

Затем, вам необходимо создать приложение в [кабинете разработчика](http://talent.kruzhok.org/developer/) согласно [инструкции](https://talent.kruzhok.org/api/docs/). 

Для работы примеров, параметр «Метод аутентификации клиента» нужно поставить в значение `client_secret_post`.

Отредактируйте файл `.env` и укажите в качестве значений переменных `CLIENT_ID`,  `CLIENT_SECRET` данные, полученные из кабинета; в качестве `REDIRECT_URI` укажите значение, которое вы установили при создании приложения.

## Запуск
```bash
poetry run python ./examples/authorization_code_flow.py
```