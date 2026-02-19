from duckduckgo_search import DDGS

def search_web(query):
    results_text = ""

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)

        for r in results:
            results_text += f"""
Title: {r['title']}
Snippet: {r['body']}
URL: {r['href']}

"""

    return results_text
