from duckduckgo_search import DDGS


def web_search(query):

    with DDGS() as ddgs:

        results = list(
            ddgs.text(
                query,
                max_results=3
            )
        )

    return results