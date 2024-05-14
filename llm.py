from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import GEMINI_API_KEY
from typing import List


def generate_questions(topic: str, questions: List[str], question_count: int = 5, verbose: bool = False) -> List[str]:
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", google_api_key=GEMINI_API_KEY)

    prompt = '''
    For each question given below, generate {question_count} more different questions based on this requirement. 
    These questions should be related to my current one in terms of topic, context, and field 
    but expressed differently. Your generated questions should be insightful, relevant, 
    and specific." 
    ANSWER NOTHING BUT THE {question_count} INSIGHT QUESTIONS. 
    Separate each question with only '\n'. 
    Here is your topic: {topic}
    Here are the questions I have so far, use these as the context for the new questions:
    {questions}
    '''
    quest_gen_prompt = PromptTemplate.from_template(prompt)
    chain = LLMChain(llm=llm, prompt=quest_gen_prompt, verbose=verbose)
    input_data = {"topic": topic, "questions": questions,
                  "question_count": question_count}
    res = chain.invoke(input=input_data)["text"]

    return res.split("\n")


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


if __name__ == "__main__":
    # questions = ["What is the meaning of life in terms of existentialism?", "What is the point of nietzsche's heaviest weight in the gay science", "What argument does the Watchmaker argument makes about existence of God", "Explain social contract theory in terms of Hobbes", "What is the difference between a priori and a posteriori knowledge?"]
    output = generate_questions("Philosophy", [], 5)
    # output = generate_questions(topic)
    # print(output)

    # print("=====================================")
    # answer = generate_answer(topic, init_question)
    # print(answer)
