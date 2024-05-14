from typing import List
import redis
import time
import sys
import psycopg2

class RedisDB:
    def __init__(self, host: str = 'localhost', port: int = 2409, db: int = 0):
        self.driver = redis.Redis(host=host, port=port, db=db)

    def push_queue(self, key: str, value: str) -> str:
        self.driver.rpush(key, value)

    def pop_queue(self, key: str) -> str:
        return self.driver.lpop(key)

    def get_queue(self, key: str) -> List[str]:
        return self.driver.get(key)

    def get_queue_length(self, key: str) -> int:
        return self.driver.llen(key)

    def set_data(self, key: str, value: str) -> str:
        self.driver.set(key, value)

    def get_data(self, key: str) -> str:
        return self.driver.get(key)

    def delete_data(self, key: str) -> int:
        return self.driver.delete(key)

    def get_top_queue(self, key: str) -> str:
        return self.driver.lindex(key, 0)

    def get_all_queue(self, key: str) -> List[str]:
        return self.driver.lrange(key, 0, -1)

class PostgresDB:
    def __init__(self, host: str = 'localhost', port: int = 5432, dbname: str = 'test_db', user: str = 'postgres', password: str = 'mysecretpassword') -> None:
        for i in range(5):
            try:
                self.conn = psycopg2.connect(
                    host=host,
                    port=port,
                    user=user,
                    password=password
                )
                self.cur = self.conn.cursor()
                print("Connected to the Postgres database!")
                break
            except psycopg2.OperationalError as e:
                if i < 4:  # i is 0 indexed, so it goes up to 4.
                    print(f"Attempt {i+1} failed. Retrying in 5 seconds...")
                    print('Error:', e)
                    time.sleep(5)  # Wait for 5 seconds before retrying
                else:
                    print(f"Attempt {i+1} failed. Terminating program.")
                    sys.exit(1)
                    
            # after connecting to Postgres, create db
            self.create_db(dbname)
            self.create_answer_table()
            


    # abstracting for data insertion, deletion, and update
    def __execute_query(self, query: str, params: tuple = None) -> None:
        self.cur.execute(query, params)
        self.conn.commit()

    # abstracting for data lookup and getting all data
    def __fetch_query(self, query: str, params: tuple = None) -> List[tuple]:
        self.cur.execute(query, params)
        return self.cur.fetchall()

    # abstracting for getting one data
    def __fetch_one(self, query: str, params: tuple = None) -> tuple:
        self.cur.execute(query, params)
        return self.cur.fetchone()

    # abstracting for creating table
    def __create_table(self, table_name: str, columns: dict) -> None:
        column = ', '.join(
            [f'{key} {value}' for key, value in columns.items()])
        command = f'CREATE TABLE {table_name}({column})'
        self.__execute_query(command)
        self.conn.commit()

    def __close(self):
        if not self.conn or not self.cur:
            return

        self.cur.close()
        self.conn.close()

    def create_db(self, db_name: str) -> None:
        command = f'CREATE DATABASE {db_name}'
        self.__execute_query(command)
        self.conn.commit()

    def create_answer_table(self) -> None:
        cols = {
            'id': 'SERIAL PRIMARY KEY',
            'answer': 'TEXT',
            'question': 'TEXT',
            'keywords': 'TEXT[]',
            'updated_at': 'TIMESTAMP'
        }
        self.__create_table('answers', cols)

    def insert_answer(self, table_name: str, values: List[str]) -> None:
        placecholder = ', '.join(['%s' for _ in range(len(values))])
        command = f'INSERT INTO {table_name} (answer, question, keywords, updated_at) VALUES({placecholder})'

        self.__execute_query(command, tuple(values))
        self.conn.commit()

    def get_all_answer(self, table_name: str) -> any:
        command = f'SELECT * FROM {table_name}'
        res = self.__fetch_query(command)
        return res

    def delete_answer(self, table_name: str, id: int) -> None:
        command = f'DELETE FROM {table_name} WHERE id = %s'
        self.__execute_query(command, (id,))
        self.conn.commit()

    def update_answer(self, table_name: str, update: dict, param: dict) -> None:
        update_columns = ", ".join(f'{query} = %s' for query in update.keys())
        param_columns = " AND ".join(f'{query} = %s' for query in param.keys())

        values = list(param.values()) + list(update.values())

        command = f'UPDATE {table_name} SET {update_columns} WHERE {param_columns}'
        self.__execute_query(command, values)
        self.con.commit()

    def __del__(self) -> None:
        self.__close()


if __name__ == "__main__":
    from datetime import datetime
    from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD

    test = PostgresDB(host=POSTGRES_HOST, port=POSTGRES_PORT,
                      dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD)

    mock_data = ["this is an answer", "this is a question",
                 ["keyword1", "keyword2"], datetime.now()]
    table_name = "answers"
    # test.insert_answer(table_name, mock_data)

    print(test.get_all_answer(table_name))