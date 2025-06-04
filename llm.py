from store_index import retriever
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="models/gemini-1.5-pro",  
    temperature=0.4,
    max_output_tokens=500,
    google_api_key="AIzaSyCqFBewSsxZpL86SjiqYL25IZ9Y2_rqEdA"
)

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "You are an expert assistant for a question-answering task.\n"
    "Use the following pieces of retrived context to answer.\n"
    "If the answer is not explicitly in the context, respond strictly with: 'I don't know.'\n"
    "Do NOT explain what the document is about.\n"
    "Use four Sentences Maximum and keep the "
    "answer concise.\n\n"
    "Context:\n{context}"
)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain=create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

