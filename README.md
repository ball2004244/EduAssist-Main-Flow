# LogosDB - Data Gen

This repo contains the data generator for LogosDB, which equips small Language Model with Knowledge and Accuracy of LLM.

LogosDB:

- Blazingly Fast
- Super Liteweight
- Simple Setup
- Working fully offline

## Minimal Requirements

- Working machine with GPU Nvidia 1080Ti or better
- Capable of running Small Language Model like Mixtral 8x7B, LLama3 7B, etc.
- 2GB of free space for the database
- 16GB of RAM

## Installation

1. Clone this repo
2. Run `pip install -r requirements.txt`
3. Copy '.env.example' to '.env' and fill the necessary information
4. Set up your desired topics in `mock_data.py`
5. Run `python question.py` to generate questions
6. At the same time, run `python answer.py` to generate answers
7. Check out the installed postgresql database for the generated data
