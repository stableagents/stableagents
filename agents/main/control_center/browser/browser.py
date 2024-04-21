import requests

class Browser:
    def __init__(self, computer):
        self.computer = computer 

    def search(self, query):
        """
        Searches the web for the specified query and returns the results
        """
        response = requests.get(
            f'{self.computer.api_base.strip("/")}/browser/search',
            params={"query": query},
        )
        return response.json()["result"]

    class Search:
        def __init__(self, browser, query):
            self.browser = browser
            self.query = query
            self.results = self.browser.search(query)

        def filter_by_keyword(self, keyword):
            """
            Filters the search results to only include items containing the specified keyword.
            """
            filtered_results = []
            for result in self.results:
                if keyword.lower() in result['title'].lower():
                    filtered_results.append(result)
            return filtered_results

# Example usage
if __name__ == "__main__":
    # Assuming `computer` is an object with an `api_base` attribute
    computer = type('Computer', (object,), {'api_base': 'https://example.com'})()
    browser = Browser(computer)
    search = Browser.Search(browser, "Python programming")
    filtered_results = search.filter_by_keyword("Python")
    print(filtered_results)
