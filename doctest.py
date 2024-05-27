from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL pattern
base_url = "https://m.likumi.lv/doc.php?id={}"

# Iterate over the range of IDs
for i in range(1, 360000):
    try:
        # Construct URL with current ID
        url = base_url.format(i)
        driver.get(url)
        time.sleep(2)  # Wait for the page to load

        # Initialize variable to store the combined text
        combined_text = ""

        # Check for the presence of the 'neko-body' div
        neko_body_elements = driver.find_elements(By.CLASS_NAME, "neko-body")
        if not neko_body_elements:
            print(f"No 'neko-body' found for ID {i}, skipping...")
            continue

        # If 'neko-body' is present, then look for the status
        status_elements = driver.find_elements(By.CSS_SELECTOR, "div.doc-info.first span.ico")
        if status_elements:
            status_text = f"Statuss: {status_elements[0].text}\n"
            combined_text += status_text

        # Extract text from 'p' and 'h3' tags within 'neko-body'
        p_tags = neko_body_elements[0].find_elements(By.TAG_NAME, "p")
        h3_tags = neko_body_elements[0].find_elements(By.TAG_NAME, "h3")

        for tag in p_tags + h3_tags:
            combined_text += tag.text + "\n"

        # Save content to a text file if there is any text collected
        if combined_text.strip():  # Check if text is not just whitespace
            with open(f"doc_{i}.txt", "w", encoding="utf-8") as file:
                file.write(combined_text)
                print(f"Saved doc_{i}.txt")
        else:
            print(f"Found 'neko-body' but no text for ID {i}, skipping...")

    except Exception as e:
        print(f"Failed to process ID {i}: {str(e)}")

# Close the driver
driver.quit()
