import pandas as pd
import psycopg2 
from dataclasses import dataclass
from queries import Template,Query
import os


class NotFoundError(Exception):
    pass

class EmptyQuery(Exception):
    pass

class DbName:
   PROFILE = "msprofileproduction"
   CONTENT = "mscontentproduction"
   STATS = "msstats"
   PROXY='msstatsproxyprod'

class Host:
   LOCAL = "localhost"
   REMOTE = ""

@dataclass
class BkData:
    user:str=os.getenv('BK_DB_USER')
    password:str=os.getenv('BK_DB_PASS')
    host:Host=Host.LOCAL
    port:str = "5432"
    database:DbName=DbName.PROFILE
    query:Query=Query(Template.PROFILE,"'areandina'").compile_query
    
    
    @property
    def fetch_data(self)->pd.DataFrame:
        connection = psycopg2.connect(user= self.user,
                                          password= self.password,
                                          host= self.host,
                                          port= self.port,
                                          database= self.database)

        try:

            cursor = connection.cursor()
            query = self.query
            result= pd.read_sql(query, connection)
            if result is None:
                raise EmptyQuery('empty query')
            cursor.close()
            return result

        except (Exception, psycopg2.Error) as error :
            print (error)
            raise NotFoundError('unable to execute query')

        finally:
            print('closing DB')
            connection.close()