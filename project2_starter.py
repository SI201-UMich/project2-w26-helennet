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
    with open(html_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f, 'html.parser')
 
    listings = soup.find_all('div', class_='PLACEHOLDER_CLASS_FOR_LISTING_CARD')
    
    for listing in listings:
        title_element = listing.find('div', class_='PLACEHOLDER_CLASS_FOR_TITLE') 
        title = title_element.text.strip() if title_element else "Unknown Title"
        
        link_element = listing.find('a', href=True)
        listing_id = ""
        if link_element:
            match = re.search(r'/rooms/(\d+)', link_element['href'])
            if match:
                listing_id = match.group(1)
                
        if title and listing_id:
            results.append((title, listing_id))
            
    return results
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
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    filepath = os.path.join("html_files", f"{listing_id}.html")
    
    details = {
        "policy_number": "Exempt", 
        "host_type": "regular",
        "host_name": "",
        "room_type": "Entire Room",
        "location_rating": 0.0
    }
    
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            soup = BeautifulSoup(f, 'html.parser')
            
            # Policy Number
            policy_text = soup.find(text=re.compile(r'license|policy|registration', re.I))
            if policy_text:
                if "pending" in policy_text.lower():
                    details["policy_number"] = "Pending"
                elif "exempt" in policy_text.lower():
                    details["policy_number"] = "Exempt"
                else:
                    details["policy_number"] = policy_text.strip()

            # Host Name
            host_header = soup.find('h2', text=re.compile(r'Hosted by', re.I))
            if host_header:
                host_string = host_header.text.strip()
                details["host_name"] = host_string.replace("Hosted by ", "").strip()
                
            # Host Type
            if soup.find(text=re.compile(r'Superhost', re.I)):
                details["host_type"] = "Superhost"

            subtitle_element = soup.find('h2', class_='PLACEHOLDER_CLASS_FOR_SUBTITLE')
            if subtitle_element:
                subtitle = subtitle_element.text.strip().lower()
                if "private" in subtitle:
                    details["room_type"] = "Private Room"
                elif "shared" in subtitle:
                    details["room_type"] = "Shared Room"
                else:
                    details["room_type"] = "Entire Room"

            rating_element = soup.find('span', class_='PLACEHOLDER_CLASS_FOR_LOCATION_RATING')
            if rating_element:
                try:
                    details["location_rating"] = float(re.search(r'\d+\.\d+', rating_element.text).group())
                except (ValueError, AttributeError):
                    details["location_rating"] = 0.0

    except FileNotFoundError:
        pass
        
    return {listing_id: details}
    pass
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


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
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

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

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