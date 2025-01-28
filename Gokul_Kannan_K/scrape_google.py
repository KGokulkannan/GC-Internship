from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def setup_driver():
    """Initialize and return a Chrome WebDriver instance."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Open browser in maximized mode
    driver = webdriver.Chrome(options=options)  # Ensure ChromeDriver is installed
    return driver

def google_search(driver, query):
    """Perform a Google search and return the list of result titles."""
    try:
        # Open Google
        driver.get("https://www.google.com")

        # Wait for the search box to appear
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        # Find the search box and enter the query
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h3"))
        )

        # Scrape the titles of search results
        results = driver.find_elements(By.CSS_SELECTOR, "h3")
        return [result.text for result in results if result.text.strip()]

    except TimeoutException:
        print("Timed out waiting for page elements to load.")
        return []

    except NoSuchElementException:
        print("Unable to locate an element on the page.")
        return []

def main():
    """Main function to perform Google search and display results."""
    driver = setup_driver()
    try:
        # Get search query from user
        search_query = input("Enter your search term: ")

        # Perform Google search and get results
        search_results = google_search(driver, search_query)

        # Display the results
        if search_results:
            print("\nSearch Results:")
            for index, title in enumerate(search_results, 1):
                print(f"{index}: {title}")
        else:
            print("No results found or an error occurred.")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    main()
