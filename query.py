from makeEmbeddings import get_embedding_function
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.llms.ollama import Ollama
import argparse
import os


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Choose an appropriate recipe based on the above context when you are told {query} and output it as JSON. An example output is shown below: 
{{
  "title": "Italian Party Sub",
  "ingredients": [
    "1 14-inch loaf Italian bread",
      "1/2 pound sliced mortadella",
      "1/4 pound sliced capicola",
      "1/4 pound sliced Genoa salami or hot soppressata",
      "1/4 pound sliced prosciutto",
      "1/4 pound sliced aged provolone cheese",
      "2 1/3 cups giardiniera (Italian pickled vegetables), drained and chopped",
      "1 cup sliced pitted Cerignola olives (black and green)",
      "1/2 cup chopped jarred Peppadew peppers",
      "2 tablespoons extra-virgin olive oil",
      "2 cups chopped romaine lettuce"
  ],
  "instructions": [
    "Split the bread in half lengthwise.",
    "Top the bottom half with the mortadella, capicola, salami, prosciutto and provolone.",
    "Toss the giardiniera in a bowl with the olives, peppers and olive oil.",
    "Pack the lettuce into the center of the bread and top with the giardiniera mixture.",
    "Carefully put the two sandwich halves together, pressing to keep the filling inside.",
    "Secure with small skewers and cut into pieces."
  ]
}}
"""

def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)

def query_rag(query_text: str): 
    db = Chroma(persist_directory= 'chroma', embedding_function=get_embedding_function())
    results = db.similarity_search_with_score(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, query=query_text)
    model = Ollama(model="llama3.1")
    response_text = model.invoke(prompt)
    print(response_text)
    return response_text
    
if __name__ == "__main__":
    main()