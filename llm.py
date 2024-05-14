from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import GEMINI_API_KEY
from typing import List
import time


def generate_questions(topic: str, questions: List[str], question_count: int = 5, verbose: bool = False) -> List[str]:
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", google_api_key=GEMINI_API_KEY)

    prompt = '''
    You are an expert in field {topic}. Your task is to come up with {question_count} indepth questions follow-up my current questions. 
    These questions should be in same field but not too related to my current one in terms of topic, context, and field. 
    Your generated questions should be insightful, relevant, and specific to the original one.
    ANSWER NOTHING BUT THE {question_count} INSIGHT QUESTIONS. 
    Dont be too shallow, but deeply insightful instead.
    Separate each question with only '\\n'. 
    Here is your topic: {topic}
    Here are the questions I have so far:
    {questions}
    '''

    quest_gen_prompt = PromptTemplate.from_template(prompt)
    chain = LLMChain(llm=llm, prompt=quest_gen_prompt, verbose=verbose)
    input_data = {"topic": topic, "questions": questions,
                  "question_count": question_count}
    res = chain.invoke(input=input_data)["text"]

    # Return only non-empty questions
    return list(filter(None, res.split("\n")))


def generate_answer(topic: str, question: str, verbose: bool = False) -> str:
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", google_api_key=GEMINI_API_KEY)

    prompt = '''
    You are an expert in field {topic}. You are asked to answer the following question: "{question}".
    Please provide a detailed and insightful answer to the question.
    Answer in a way that is informative, relevant, and specific to the question.
    Also answer from 400-600 words.
    '''
    answer_gen_prompt = PromptTemplate.from_template(prompt)
    chain = LLMChain(llm=llm, prompt=answer_gen_prompt, verbose=verbose)

    input_data = {"topic": topic, "question": question}
    res = chain.invoke(input=input_data)["text"]
    return res


def generate_topics(topic: str, sub_topics: int, max_call: int = 3) -> List[str]:
    if max_call == 0:
        return []

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", google_api_key=GEMINI_API_KEY)

    prompt = '''
    You are an expert in this {topic} field. Your task is to give {sub_topics} possible subtopics that is relevant to the {topic}. 
    Answer only with the subtopics provided and nothing else. Make sure your subtopics are relevant and specific to the {topic} topic and expand it in some way.
    Separate each subtopic with only '\\n'. 
    '''
    topic_gen_prompt = PromptTemplate.from_template(prompt)
    chain = LLMChain(llm=llm, prompt=topic_gen_prompt, verbose=False)
    input_data = {"topic": topic, "sub_topics": sub_topics}

    output_topics = chain.invoke(input=input_data)["text"].split("\n")
    out = output_topics.copy()
    for topic in output_topics:
        time.sleep(1)
        new_topics = generate_topics(topic, sub_topics, max_call - 1)
        if (len(new_topics) > 0):
            out.extend(new_topics)

    # remove empty topics
    return list(filter(None, out))


if __name__ == "__main__":
    topic = "Philosophy"
    sub_topics = 5
    questions = ["What is the meaning of life?"]
    output = generate_questions(topic, questions, question_count=5, verbose=True)
    print(output)

