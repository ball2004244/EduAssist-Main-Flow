from llm import generate_answer
from store import PostgresDB, RedisDB
from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD
from rich.console import Console
from mock_data import MOCK_KEYWORDS
from datetime import datetime
import time

console = Console()
# This code will generate answers based on the questions in the redis queue
# Then push answers to the redis queue


def main() -> None:
    topic = "Philosophy"
    redis_db = RedisDB()  # question queue
    postgres_db = PostgresDB(host=POSTGRES_HOST, port=POSTGRES_PORT, dbname=POSTGRES_DB,
                             user=POSTGRES_USER, password=POSTGRES_PASSWORD)  # answer storage
    while True:
        # get first question from the queue
        question = redis_db.pop_queue("questions")
        if not question:
            continue

        console.print(f"[green]Generating answer...")
        console.print(f"[bold]Question: {question}")
        answer = generate_answer(topic, question)
        console.print(f"Generated Answer:")
        console.print(f"{answer}")

        # insert data to postgres
        # should be replaced with real keywords after call kw extraction model
        keywords = MOCK_KEYWORDS
        postgres_data = [answer, question, keywords, datetime.now()]
        postgres_db.insert_answer("answers", postgres_data)

        console.print(
            f"[green]Answer pushed to {topic} database, waiting 2s to generate new answer")
        time.sleep(2)


# wait 2s before generating new answer
if __name__ == "__main__":
    main()
