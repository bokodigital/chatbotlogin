from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

SBR_WEBDRIVER = 'https://brd-customer-hl_e2661980-zone-scrapingdata:t7vcaj25vcn4@brd.superproxy.io:9515'

def scrape_website(url):
    print("Launching from browser..")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(url)
        print("Waiting captcha to solve...")
        # solve_res = driver.execute('executeCdpCommand', {
        #     'cmd': 'Captcha.waitForSolve',
        #     'params': {'detectTimeOut':100},
        # })
        # print("Captch Solve Status", solve_res['value']['status'])

        # Python Selenium - manually solving CAPTCHA after navigation  
        driver.execute('executeCdpCommand', {  
            'cmd': 'Captcha.setAutoSolve',  
            'params': {'autoSolve': False},  
        })  
        driver.get(url)  
        solve_result = driver.execute('executeCdpCommand', {  
            'cmd': 'Captcha.solve',  
            'params': {'detectTimeout': 30000},
        })  
        print('Captcha solve status:', solve_result['value']['status'])

        print("Navigatin! scrapping Content")
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(html_content):
    soup = BeautifulSoup(html_content,"html.parser")
    
    for script_or_style in soup(["script"],["style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator = "\n")
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip())

    return cleaned_content

def split_dom_content (dom_content, max_lenght = 6000):
    return[
        dom_content[i : 1 + max_lenght] for i in range(0, len(dom_content), max_lenght)
    ]


# import selenium.webdriver as webdriver
# from selenium.webdriver.chrome.service import Service
# import time

# def scrape_website(website):
#     print("Launching from browser..")

#     chrome_driver_path = "./chromedriver.exe"
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

#     try:
#         driver.get(website)
#         print("page loaded...")
#         html = driver.page_source
#         time.sleep(10)
#         return html
#     finally:
#         driver.quit()