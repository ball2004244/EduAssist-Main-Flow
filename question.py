from llm import generate_questions
from store import RedisDB
from rich.console import Console
import time

console = Console()

# This code will generate questions based on the initial question and topic
# Then push questions to the redis queue
# If the queue limit is reached, it will wait for 30s for answer service to consume the questions


def main() -> None:
    question_limit = 100  # max size of the queue
    redis_db = RedisDB()
    # init_question = input("Enter the initial question for the AI system: ")
    # topic = input("Enter the topic for the AI system: ")
    init_question = "What is the meaning of life in terms of existentialism?"
    topic = "Philosophy"

    redis_db.delete_data("questions")  # clear the queue
    # push the initial question
    redis_db.push_queue("questions", init_question)
    while True:
        if redis_db.get_queue_length("questions") >= question_limit:
            console.print(f"[red]Queue limit reached. Retry in 30s")
            time.sleep(30)
            continue

        console.print(f"[green]Generating questions...")
        console.print(f"[bold]Topic: {topic}")
        console.print(f"[bold]Initial Question: {init_question}")

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
