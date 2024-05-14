from config import POSTGRES_USER, POSTGRES_PASSWORD
from typing import List
import subprocess

# Install each Helm chart for each topic
def install_charts(release_name: str, chart_name: str, topics: List[str]) -> None:
    for topic in topics:
        command = [
            "helm", "install", f"{release_name}-{topic}", chart_name, 
            "--set", f"topic={topic}", 
            "--set", f"postgres.postgresqlUser={POSTGRES_USER}",
            "--set", f"postgres.existingSecret=postgres-secret"
        ]
        process = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            print(f"Error: {error}")
        else:
            print(f"Output: {output}")

# Usage
if __name__ == "__main__":
    install_charts("test-release", "topic-chart", ["maths", "physics", "chemistry"])