# api/wiki_api.py
import requests
import json

def search_wikipedia(query, limit=1, language="en"):
    """
    Search Wikipedia for information on a given query
    
    Args:
        query (str): Search query
        limit (int): Maximum number of results to return
        language (str): Language code for Wikipedia edition
        
    Returns:
        str: Wikipedia extract or empty string if no results
    """
    try:
        # Build the API URL
        url = f"https://{language}.wikipedia.org/w/api.php"
        
        # Set up the request parameters
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "redirects": 1,
            "titles": query,
        }
        
        # Make the request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract the page content
            pages = data.get("query", {}).get("pages", {})
            
            # Wikipedia API returns a dict with page IDs as keys
            # We just need the content of the first valid page
            content = ""
            for page_id, page_data in pages.items():
                if page_id != "-1":  # -1 means no results
                    content = page_data.get("extract", "")
                    break
            
            return content
        else:
            print(f"Wikipedia API request failed with status {response.status_code}")
            return ""
    
    except Exception as e:
        print(f"Error in Wikipedia API request: {str(e)}")
        return ""

def get_wikipedia_summary(title, language="en"):
    """
    Get the summary of a Wikipedia article
    
    Args:
        title (str): Exact Wikipedia article title
        language (str): Language code for Wikipedia edition
        
    Returns:
        str: Article summary or empty string if not found
    """
    try:
        # Build the API URL
        url = f"https://{language}.wikipedia.org/w/api.php"
        
        # Set up the request parameters
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts",
            "exintro": True,
            "explaintext": True,
            "titles": title,
        }
        
        # Make the request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract the page content
            pages = data.get("query", {}).get("pages", {})
            
            # Get the first page content
            for page_id, page_data in pages.items():
                return page_data.get("extract", "")
            
            return ""
        else:
            print(f"Wikipedia API request failed with status {response.status_code}")
            return ""
    
    except Exception as e:
        print(f"Error in Wikipedia API request: {str(e)}")
        return ""

def search_wikipedia_with_suggestions(query, limit=3, language="en"):
    """
    Search Wikipedia with query suggestions
    
    Args:
        query (str): Search query
        limit (int): Maximum number of results to return
        language (str): Language code for Wikipedia edition
        
    Returns:
        list: List of results with titles and extracts
    """
    try:
        # First, get search suggestions
        url = f"https://{language}.wikipedia.org/w/api.php"
        
        params = {
            "action": "opensearch",
            "format": "json",
            "search": query,
            "limit": limit,
            "namespace": 0,
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code != 200:
            print(f"Wikipedia API request failed with status {response.status_code}")
            return []
        
        data = response.json()
        
        # Extract titles from the response
        titles = data[1]
        
        # For each title, get the summary
        results = []
        for title in titles:
            summary = get_wikipedia_summary(title, language)
            if summary:
                results.append({
                    "title": title,
                    "extract": summary
                })
        
        return results
    
    except Exception as e:
        print(f"Error in Wikipedia API request: {str(e)}")
        return []