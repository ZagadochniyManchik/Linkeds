import pymysql
from CONFIG.database_config import *


class Database:
    """
    Class Database with standard requests to mysql using python
    Such as - SELECT; INSERT; DELETE; UPDATE; CREATE
    """

    def __init__(self):
        try:
            self._connection = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset=DB_CHARSET,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.is_alive = True
            self._connection.close()
            self._connection = None
        except Exception as error:
            self.is_alive = False
            raise ConnectionError(str(error))

    def __del__(self):
        try:
            self._connection.close()
        except Exception as error:
            self.error_report = error
            return

    def connect(self) -> str:
        """
        Connecting to DB, raise Error if database is not alive
        If connect successful - returns DB config
        """
        try:
            self._connection = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME,
                charset=DB_CHARSET,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.is_alive = True

            return f'Connected to {DB_NAME} | HOST: {DB_HOST} | PORT: {DB_PORT} |'

        except Exception as error_data:
            raise ConnectionError(str(error_data))

    def connection_proc(self, process) -> None:
        """
        Executing function results into mysql
        """
        try:
            with self._connection.cursor() as self.cursor:
                conn_process = process
                self.cursor.execute(conn_process)
        except Exception as error_data:
            raise ValueError('(RequestError): ' + str(error_data))

    def select(self, table_name: str = 'None', id: str = 'None', subject: str = '*', criterion: str = 'id') -> str:
        """
        Returns selected data from selected Table
        """
        if table_name == 'None':
            raise ValueError(f'Table not specified in module "{self}.select"')

        if id == 'None':
            self.connection_proc(f"SELECT {subject} FROM `{table_name}`")
            return self.cursor.fetchall()

        self.connection_proc(f"SELECT {subject} FROM `{table_name}` WHERE {criterion} = '{id}'")
        return self.cursor.fetchall()

    def update(self, table_name: str = 'user', id: str = 'None', subject: str = None, subject_value=None,
               criterion: str = 'id') -> str:
        """
        Rewrite old data to new
        """
        if table_name == 'None':
            raise ValueError(f'Table not specified in module "{self}.update"')

        if subject_value is None or subject is None:
            raise ValueError(f'Update func doesnt get any type of data to update in module "{self}.update"')

        if table_name == 'images':
            if id == 'None':
                raise ValueError(f'ID is required to make UPDATE in images table')
            with self._connection.cursor() as self.cursor:
                conn_process = f"UPDATE `{table_name}` SET {subject} = %s WHERE `{criterion}` = '{id}'"
                arguments = (subject_value,)
                self.cursor.execute(conn_process, arguments)
            self._connection.commit()
            return f'Updated data in `{table_name}`["{subject}" = "image"] for {criterion}[{id}]'

        if id == 'None':
            self.connection_proc(f"UPDATE `{table_name}` SET {subject} = '{subject_value}'")
            self._connection.commit()
            return f'Updated data in `{table_name}`["{subject}" = "{subject_value}"] for all IDs'

        self.connection_proc(f"UPDATE `{table_name}` SET `{subject}` = '{subject_value}' WHERE `{criterion}` = '{id}'")
        self._connection.commit()
        return f'Updated data in `{table_name}`["{subject}" = "{subject_value}"] for {criterion}[{id}]'

    def create(self, status: str = 'table', name: str = 'example', table_args: set[str] = None) -> str:
        """
        Create table or Database
        """
        if table_args is None:
            table_args = ('Row1 INT', 'Row2 VARCHAR(59)')  # standard values to create

        if status == 'database':
            self.connection_proc(f"CREATE {status.upper()} `{name}`")
            self._connection.commit()
            return f'Created {status.upper()} with name[{name}]'

        elif status == 'table':
            self.connection_proc(f"CREATE {status.upper()} `{name}` ({', '.join(table_args)})")
            self._connection.commit()
            return (f'Created {status.upper()} with name[{name}]\n'
                    f'Args: [{", ".join(table_args)}]')

        else:
            raise ValueError('Incorrect type of status, must be ("table", "database")')

    def insert(self, name: str = 'user', subject_values=None) -> str:
        """
        Insert row of data in table
        """

        table_elements = db_table_elements.get(name)
        try:
            if name == 'user':
                table_elements.remove('id')
        except ValueError:
            pass

        if subject_values is None:
            raise ValueError("Subject values must be dict, not NoneType object")

        if len(subject_values) != len(table_elements):
            raise ValueError("Not enough values to make INSERT func")

        request = map(lambda x: "'" + str(x) + "'", subject_values.values())
        self.connection_proc(f"INSERT INTO `{name}` ({', '.join(table_elements)}) "
                             f"VALUES ({', '.join(list(request))});")
        self._connection.commit()
        return f"Inserted data in table {name}"

    def delete(self, table_name: str = None, id: str = None, criterion: str = 'id') -> str:
        """
        Delete Data from specified table
        """
        if table_name is None or id is None:
            raise ValueError(f"Not enough data for module {self}.delete")

        self.connection_proc(f"DELETE FROM `{table_name}` WHERE id = '{id}'")
        self._connection.commit()
        return f"Deleted data from table:`{table_name}` where {criterion}:'{id}'"
