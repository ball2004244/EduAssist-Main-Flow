from mock_data import MOCK_QUESTIONS
from typing import List
import redis


class RedisDB:
    def __init__(self, host: str = 'localhost', port: int = 2409, db: int = 0):
        self.driver = redis.Redis(host = host, port = port, db = db)
        
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

 