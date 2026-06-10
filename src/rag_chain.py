from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

def build_rag_chain(retriever):
    llm = ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama-3.1-8b-instant",
        temperature=0.2
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a helpful assistant. 
        Answer the question using ONLY the context below.
        If the answer is not in the context, say "I could not find this in the document."

        Context:
        {context}

        Question: {question}

        Answer:"""
    )

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
    return chain

def ask(chain, question):
    result = chain.invoke({"query": question})
    return result["result"], result["source_documents"]