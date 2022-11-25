from typing import Dict

class Kwargs:
    SEARCH:Dict = {"id":"count"}
    REDIRECT:Dict = {"id":"count"}
    CONTENT_REDIRECT: Dict = {'redirecciones':'sum'}
    ACTIVE_USERS:Dict = {'correo':'nunique'}
    REGISTERS: Dict = {'correo':'count'}
    SESSIONS: Dict = {'sesión','nunique'}
    CONTENT_CREATED: Dict = {'titulo':'count'}