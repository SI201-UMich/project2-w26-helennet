# SI 201 HW4 (Library Checkout System)
# Your name: Xinyi Peng & Shiyu Xiong
# Your student id: xinyip & 
# Your email: xinyip@umich.edu &
# Who or what you worked with on this homework (including generative AI like ChatGPT): Xinyi Peng & Shiyu Xiong
# If you worked with generative AI also add a statement for how you used it.
# e.g.: We use GenAI to help us check our codes.
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""

# Linnet Function 1
def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    results = []
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    title_divs = soup.find_all('div', id=re.compile(r'^title_'))
    if title_divs:
        for div in title_divs:
            listing_id = div['id'].replace('title_', '')
            title = div.get_text(strip=True)
            if (title, listing_id) not in results:
                results.append((title, listing_id))
    else:
        for a_tag in soup.find_all('a', target=re.compile(r'^listing_')):
            listing_id = a_tag['target'].replace('listing_', '')
            title_div = a_tag.find('div', class_='t1jojoys')
            if title_div:
                title = title_div.get_text(strip=True)
                if (title, listing_id) not in results:
                    results.append((title, listing_id))

    return results[:18]
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Linnet Function 2
def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    import os
    import re
    from bs4 import BeautifulSoup

    details = {
        "policy_number": "Exempt", 
        "host_type": "regular",
        "host_name": "",
        "room_type": "Entire Room",
        "location_rating": 0.0
    }

    clean_id = str(listing_id).strip()
    filepath = os.path.join("html_files", f"listing_{clean_id}.html")
    
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()
    except FileNotFoundError:
        return {listing_id: details}

    soup = BeautifulSoup(html, 'html.parser')
    
    full_text = soup.get_text(separator=" ", strip=True).replace("\xa0", " ")

    str_match = re.search(r'(STR\s*-\s*\d+)', full_text, re.IGNORECASE)
    if str_match:
        details["policy_number"] = str_match.group(1).replace(" ", "").upper()
    elif "pending" in full_text.lower():
        details["policy_number"] = "Pending"

    if "superhost" in full_text.lower():
        details["host_type"] = "Superhost"

    for h in soup.find_all(['h1', 'h2', 'h3']):
        h_text = h.get_text(strip=True).replace("\xa0", " ")
        if "hosted by" in h_text.lower():
            if "private" in h_text.lower():
                details["room_type"] = "Private Room"
            elif "shared" in h_text.lower():
                details["room_type"] = "Shared Room"
            else:
                details["room_type"] = "Entire Room"
            
            name_match = re.search(r'hosted by\s+([A-Za-z]+)', h_text, re.IGNORECASE)
            if name_match:
                details["host_name"] = name_match.group(1).strip()
            break 

    loc_match = re.search(r'Location[^\d]{0,30}?([0-5]\.\d+)', full_text, re.IGNORECASE)
    if loc_match:
        details["location_rating"] = float(loc_match.group(1))

    return {listing_id: details}
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Linnet Function 3
def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    database = []
    listings = load_listing_results(html_path)
    
    for title, listing_id in listings:
        details_dict = get_listing_details(listing_id)
        info = details_dict.get(listing_id, {})
        
        listing_tuple = (
            title,
            listing_id,
            info.get("policy_number", "Exempt"),
            info.get("host_type", "regular"),
            info.get("host_name", "Unknown"),
            info.get("room_type", "Entire Room"),
            info.get("location_rating", 0.0)
        )
        database.append(listing_tuple)
        
    return database
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Helen Funtion 1
def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Helen Function 2
def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Helen Function 3
def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Arg
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================

# Linnet Function 4
# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = f"https://scholar.google.com/scholar?q={requests.utils.quote(query)}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    titles = []
    for item in soup.find_all('h3', class_='gs_rt'):
        title_text = item.text
        title_text = re.sub(r'^\[.*?\]\s*', '', title_text)
        titles.append(title_text)
        
    return titles
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

# Linnet Test Function 1
    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        self.assertEqual(len(self.listings), 18)
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))
        pass

# Linnet Test Function 2
    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        results = [get_listing_details(l_id) for l_id in html_list]

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        self.assertEqual(results[0]["467507"]["policy_number"], "STR-0005349")
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        self.assertEqual(results[2]["1944564"]["host_type"], "Superhost")
        self.assertEqual(results[2]["1944564"]["room_type"], "Entire Room")
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(results[2]["1944564"]["location_rating"], 4.9)
        pass

# Linnet Test Funtion 3
    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for item in self.detailed_data:
            self.assertEqual(len(item), 7)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(
            self.detailed_data[-1], 
            ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        )
        pass

# Helen Test Function 1
    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)
# Helen Test Function 2
    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

# Helen Test Function
    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)