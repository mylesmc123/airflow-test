from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os

def fetch_nws_tabular_gage(gage_id):
    # Set up Chrome options to run in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")  # Enable debugging

    # Set the download directory to the current working directory
    download_dir = os.getcwd()  # Get the current working directory

    # Specify the download directory in Chrome options
    prefs = {
        "download.default_directory": download_dir,  # Set download directory
        "download.prompt_for_download": False,       # Do not prompt for download
        "directory_upgrade": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # chrome_options.add_argument(f"--download.default_directory={download_dir}")

    # Specify the path for the Chrome binary in WSL
    chrome_options.binary_location = "/usr/bin/chromium-browser"

    # Initialize the webdriver with the specified options
    service = Service(ChromeDriverManager().install())
    # # Initialize the webdriver with the specified options and specify the desired ChromeDriver version
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="135.0.7049.114").install()), options=chrome_options)


    # Navigate to the page
    url = f'https://water.noaa.gov/gauges/{gage_id}/tabular'
    driver.get(url)

    # Wait for the page to load (you may need to adjust the time)
    time.sleep(10)

    # Wait until the observed download button is clickable
    observed_download_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, 'buildTableCSV') and contains(text(), 'Download CSV')]"))
    )

    # Locate the "Download Forecasted CSV" button using its onclick attribute
    forecasted_download_button = driver.find_element(By.XPATH, "//button[contains(@onclick, 'buildTableCSV') and contains(@onclick, 'forecast')]")

    # Uncomment one of these depending on which data you want to download:

    # Click the "Download Observed CSV" button
    observed_download_button.click()
    # wait for the download to complete
    time.sleep(5)  # Adjust the sleep time as needed

    # Or click the "Download Forecasted CSV" button
    forecasted_download_button.click()#it for the forecasted data
    # wait for the download to complete
    time.sleep(5)  # Adjust the sleep time as needed

    # Print a message confirming the download action
    print(f"CSV file should be downloaded to {download_dir}")
    driver.quit()

    # copy the downloaded file to the current working directory
    # The downloaded file will be in the default download directory of the browser
    # Check if the file exists in the download directory
    downloaded_observed_file = os.path.join('/home/mmc/snap/chromium/3117/Downloads'  , "WLTO2_HGIRG_observed.csv")
    downloaded_forecast_file = os.path.join('/home/mmc/snap/chromium/3117/Downloads'  , "WLTO2_HGIFF_forecast.csv")
    if os.path.exists(downloaded_observed_file):
        # Move the file to the current working directory
        os.rename(downloaded_observed_file, "WLTO2_HGIRG_observed.csv")
        print(f"Moved observed file to {os.getcwd()}")
    else:
        print(f"Observed file not found in {download_dir}")
    if os.path.exists(downloaded_forecast_file):
        # Move the file to the current working directory
        os.rename(downloaded_forecast_file, "WLTO2_HGIFF_forecast.csv")
        print(f"Moved forecast file to {os.getcwd()}")
    else:
        print(f"Forecast file not found in {download_dir}")

if __name__ == "__main__":
    gage_id = 'WLTO2'  # Replace with the desired gage ID
    fetch_nws_tabular_gage(gage_id)