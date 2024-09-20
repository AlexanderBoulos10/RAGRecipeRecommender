from makeEmbeddings import get_embedding_function
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
import argparse
import os
from openai import OpenAI

client = OpenAI()


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Choose an appropriate recipe based on the above context when you are told {query} and only output the resulting JSON and nothing else. An example output is shown below: 
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
    response = client.chat.completions.create(
          model='gpt-4o-mini',
          messages=[
              {'role': 'system', 'content': f'Answer the question based only on the following context: {context_text} and only output one recipe as as a JSON object.(ignore the 3 dashes at the start and end)'},
              {'role': 'user', 'content': 'Sub Sandwich'},
              {'role': 'assistant', 'content': '''
                      {"title": "Italian Party Sub",
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
                        ]}'''},
              {'role': 'user', 'content': query_text}
          ],
          max_tokens=500,
      )
    return response.choices[0].message.content
    
if __name__ == "__main__":
    main()