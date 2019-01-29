import os
import re

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

XPATH_TO_SONNET = '//script[contains(.,"text")]'

if __name__ == '__main__':
    url = "http://www.fibitz.com/sonnets/sonnets.html"

    chrome = Chrome()
    chrome.get(url)

    WebDriverWait(chrome, 3).until(
        EC.presence_of_element_located((By.XPATH, XPATH_TO_SONNET)))
    scripts = chrome.find_elements_by_xpath(XPATH_TO_SONNET)

    lines = []
    for script in scripts:
        script = script.get_attribute("innerHTML")
        # print(script)
        all_text = re.findall('"(.+)"', script)
        lines.extend(all_text)

    with open("fibitz.txt", "w") as file:
        file.write(os.linesep.join(lines))

    chrome.close()
