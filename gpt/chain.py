from langchain.schema.runnable import RunnablePassthrough, RunnableLambda

from gpt.prompt import ANSWER_PROMPT, CHOOSE_PROMPT

def create_chain(retriever, llm):
    return {"docs": retriever,
            "question":RunnablePassthrough(),
            } | RunnableLambda(
                lambda inputs: get_answer(inputs, llm)
                ) | RunnableLambda(
                    lambda inputs: chose_answer(inputs, llm)
                    )

def get_answer(inputs, llm):
    docs = inputs['docs']
    question = inputs['question']
    answerchain = ANSWER_PROMPT | llm
    return {
        "question": question,
        "answers": [
        {
            "answer": answerchain.invoke(
                {"context": doc, "question": question}
            ).content,
            "source": doc.metadata["source"],
            "date": doc.metadata["lastmod"],
        }
        for doc in docs
        ],
    }
    
def chose_answer(inputs, llm):
    answers = inputs["answers"]
    question = inputs["question"]
    choose_chain = CHOOSE_PROMPT | llm
    condensed = "\n\n".join(
        f"{answer['answer']}\nSource:{answer['source']}\nDate:{answer['date']}\n"
        for answer in answers
    )
    return choose_chain.invoke(
        {
            "question": question,
            "answers": condensed,
        }
    )