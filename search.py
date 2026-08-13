from ddgs import DDGS

def search_query(query):
    try:
        with DDGS() as ddgs:
            results = []
            for r in ddgs.text(query, max_results=3):
                results.append(f"🔹 {r['title']}\n   {r['body']}\n   {r['href']}")
            if results:
                return "🔍 Search results:\n" + "\n\n".join(results)
            else:
                return "No results found."
    except Exception as e:
        return f"Search error: {e}"