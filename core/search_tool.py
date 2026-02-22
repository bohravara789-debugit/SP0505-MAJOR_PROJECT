from ddgs import DDGS
import warnings

def search_web(query):
    # Suppress the RuntimeWarning about package renaming
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="duckduckgo_search")
    
    results_text = ""

    try:
        with DDGS() as ddgs:
            # Convert to list to ensure execution and handle empty results
            results = list(ddgs.text(query, max_results=5))

            if not results:
                return ""

            for r in results[:3]:
                results_text += f"""
Title: {r.get('title', 'No Title')}
Snippet: {r.get('body', 'No Snippet')}
URL: {r.get('href', '#')}

"""
    except Exception as e:
        print(f"⚠️ Search failed: {e}")
        return ""
        
    return results_text
