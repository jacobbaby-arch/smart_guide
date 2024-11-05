import requests

def get_wikipedia_attractions(city_name):
    # Define the base URL for the Wikipedia API
    base_url = "https://en.wikipedia.org/w/api.php"
    
    # Make a search request to Wikipedia for tourist attractions related to the city
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": f"tourist attractions in {city_name}",
        "format": "json",
        "srlimit": 5  # Number of results to retrieve (adjust as needed)
    }
    
    # Send request to the Wikipedia API
    response = requests.get(base_url, params=search_params)
    data = response.json()
    
    # If the response contains results, process them
    if "query" in data and "search" in data["query"]:
        attractions = data["query"]["search"]
        print(f"Top tourist attractions in {city_name}:\n")
        
        # Iterate through the search results and fetch the extracts for each attraction
        for attraction in attractions:
            title = attraction["title"]
            print(f"Title: {title}")
            print(f"Snippet: {attraction['snippet']}\n")
            
            # Now get the extract for each attraction (detailed description)
            extract_params = {
                "action": "query",
                "titles": title,
                "prop": "extracts",
                "exintro": True,  # Get an introductory snippet
                "format": "json"
            }
            
            # Fetch the full extract for the attraction
            extract_response = requests.get(base_url, params=extract_params)
            extract_data = extract_response.json()
            
            # Extract the page ID and get the extract text
            page_id = list(extract_data["query"]["pages"].keys())[0]
            extract_text = extract_data["query"]["pages"][page_id].get("extract", "No additional information available.")
            
            # Print the detailed description of the attraction
            print(f"Description: {extract_text}\n")
    else:
        print(f"No tourist attractions found for {city_name}.")

# Example usage
city = "Paris"
get_wikipedia_attractions(city)
