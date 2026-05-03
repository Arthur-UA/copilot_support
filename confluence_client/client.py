import os
from typing import Dict, List, Any

import requests
from dotenv import load_dotenv

load_dotenv(override=True)
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Basic {os.environ['CONFLUENCE_ENCODED_STRING']}'
}
BASE_URL = os.environ['CONFLUENCE_BASE_URL']


def make_cql_query(query: str) -> List[Dict[str, Any]]:
    '''Make a CQL query to the Confluence API and return the results.
    Args:
        query (str): The CQL query string.
    Returns:
        List[Dict[str, Any]]: A list of results from the Confluence API.'''

    response = requests.get(BASE_URL, headers=HEADERS, params={'cql': query})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Confluence API. Status code: {response.status_code}, Response: {response.text}")
    return response.json().get('results', [])

def get_page_content_by_word(word: str) -> List[Dict[str, Any]]:
    '''Get the content of a Confluence page by searching for a specific word.
    Args:
        word (str): The word to search for.
    Returns:
        List[Dict[str, Any]]: A list of page contents matching the search term.'''

    cql_query = f'type=page AND text~"{word}"'
    responses = make_cql_query(cql_query)

    pages = []
    for i, res in enumerate(responses):
        page_content = res.get('content', {})
        page_plain_text = f'Page №{i+1}: ' + page_content.get('title', '')
        page_plain_text += '\n\n' + res.get('excerpt', '')

        pages.append(page_plain_text)
    return pages


if __name__ == "__main__":
    print(get_page_content_by_word("Deploy"))
