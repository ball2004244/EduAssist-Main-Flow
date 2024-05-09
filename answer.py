from llm import generate_answer
from rich.console import Console
from store import RedisDB
import time

console = Console()
# This code will generate answers based on the questions in the redis queue
# Then push answers to the redis queue
def main() -> None:
    topic = "Philosophy"
    redis_db = RedisDB()
    redis_db.delete_data("answers")  # clear the queue
    while True:
        question = redis_db.pop_queue("questions")
        if not question:
            continue

        console.print(f"[green]Generating answer...")
        console.print(f"[bold]Question: {question}")
        answer = generate_answer(topic, question)
        console.print(f"Generated Answer:")
        console.print(f"{answer}")
        redis_db.push_queue("answers", answer)
        console.print(
            f"[green]Answer pushed to the queue, waiting for 2s before generating new answer")
        time.sleep(2)
# wait 2s before generating new answer
if __name__ == "__main__":
    main()