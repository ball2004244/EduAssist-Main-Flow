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
Phase 1: Data Gen - This will generate mock data to store in the database
1. Clone this repo
2. Run `pip install -r requirements.txt`
3. Copy '.env.example' to '.env' and fill the necessary information
4. Set up your desired topics in `mock_data.py`
5. Run `python question.py` to generate questions
6. At the same time, run `python answer.py` to generate answers
7. Check out the installed postgresql database for the generated data

Phase 2: Store Data - Store data distributedly in the database cluster with K8s, Helm, Docker and Postgresql
1. Create k8s secret from .env file
```bash
kubectl create secret generic postgres-secret --from-env-file=.env
```
2. Take a look at `cluster.py` and replace the necessary information.
3. Then run the following command to deploy the database cluster
```bash
python3 cluster.py
```
4. Check the status of the database cluster
```bash
kubectl get pods
```

## Interesting Finding
We use Gemini to create both questions and answers for our system. As you know, Google introduced several harmful categories that the model should avoid. However, we found that the model still recognizes its own generated texts as harmful. We are still investigating the reason behind this.
