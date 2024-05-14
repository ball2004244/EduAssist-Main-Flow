from llm import generate_questions
from store import RedisDB
from config import REDIS_DB, REDIS_HOST, REDIS_PORT
from rich.console import Console
from mock_data import MOCK_TOPICS
import time
console = Console()

# This code will generate questions based on the initial question and topic
# Then push questions to the redis queue
# If the queue limit is reached, it will wait for 30s for answer service to consume the questions


def main() -> None:
    question_limit = 100  # max size of the queue
    redis_db = RedisDB(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    topic = MOCK_TOPICS[0]

    redis_db.delete_data("questions")  # clear the queue
    while True:
        if redis_db.get_queue_length("questions") >= question_limit:
            console.print(f"[red]Queue limit reached. Retry in 30s")
            time.sleep(30)
            continue

        console.print(f"[green]Generating questions...")
        console.print(f"[bold]Topic: {topic}")

        questions = redis_db.get_all_queue("questions")
        new_questions = generate_questions(topic, questions)
        console.print(f"Generated Questions:")
        for q in new_questions:
            console.print(f"{q}")
            redis_db.push_queue("questions", q)
        console.print(
            f"[green]Questions pushed to the queue, waiting for 5s before generating new questions")
        time.sleep(5)  # wait for 5s before generating new questions


if __name__ == "__main__":
    main()
