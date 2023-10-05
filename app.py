import streamlit as st
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

import requests
import shutil
import os

@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
opts = FirefoxOptions()
opts.add_argument("--headless")
browser = webdriver.Firefox(options=opts)


# options = Options()
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')

# @st.experimental_memo
# def get_driver():
#     return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


def extract_image_url(tag,num_images):

    image_url = []

    url = f'''https://in.pinterest.com/search/pins/?q={tag}'''

    
    # browser = get_driver()

    browser.get(url)

    for _ in range(1,5):
        browser.execute_script("window.scrollTo(0,10000)")
        sleep(2)

    soup = BeautifulSoup(browser.page_source,"html.parser")

    for link in soup.find_all("img"):
        image_url.append(link.get("src"))

    browser.quit()

    df = pd.DataFrame({"url":image_url[:num_images]})
    file_name = f"{tag}_csv_file.csv"

    return df,file_name

st.title("PINTEREST IMAGE EXTRACTOR")

tag = st.text_input("Enter the tag:")
num_of_images = int(st.number_input("Number of Images Required:",min_value=0,value=0))

if tag != "" and num_of_images!=0:
    extracted_url_csv,file_name = extract_image_url(tag,num_of_images)
    csv_file = extracted_url_csv.to_csv()
        
if st.button("Scrape Images"):
        image_urls = extracted_url_csv["url"].to_list()
        if image_urls:
            st.write("Images from the webpage:")
            
            # Create a container with custom CSS to arrange images side by side
            st.write(
                f"<div style='display: flex; flex-wrap: wrap; gap: 5px;'>",
                unsafe_allow_html=True
            )
            
            for img_url in image_urls:
                # Display images side by side with custom CSS
                st.write(
                    f"<div style='flex: 1 0 calc(33.33% - 10px);'>"
                    f"<img src='{img_url}' style='width: 30%;'>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            
            # Close the container
            st.write("</div>", unsafe_allow_html=True)
        else:
            st.warning("No image URLs found on the webpage.")

        # Download images
        for i, img_url in enumerate(image_urls):
            response = requests.get(img_url)
            if response.status_code == 200:
                img_extension = img_url.split(".")[-1]
                img_filename = os.path.join("downloaded_images", f"image_{i + 1}.{img_extension}")
                with open(img_filename, "wb") as img_file:
                    img_file.write(response.content)

        # Zip downloaded images
        shutil.make_archive("downloaded_images", "zip", "downloaded_images")

        # Provide a download link to the user
        st.success(f"Downloaded {len(image_urls)} images. [Download ZIP](downloaded_images.zip)")
                
        st.success(f"Downloaded {len(image_urls)} images.")






