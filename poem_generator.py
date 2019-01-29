import random
import re
from itertools import combinations

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def fill_form(feeling, noun, aspect_choices, verb_choice, adjective_choice, month_choice):
    driver.get(url)
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//option[.="{}"]'.format(feeling))))

    driver.find_element_by_xpath('//option[.="{}"]'.format(feeling)).click()
    driver.find_element_by_xpath('//input[@name="noun"]').send_keys(noun)

    for i, x in enumerate(aspect_choices):
        driver.find_element_by_xpath('//input[@name="aspect{}"]'.format(i + 1)).send_keys(aspect_choices[i])

    for i, x in enumerate(verb_choice):
        driver.find_element_by_xpath('//input[@name="verb{}"]'.format(i + 1)).send_keys(verb_choice[i])

    for i, x in enumerate(adjective_choice):
        driver.find_element_by_xpath('//input[@name="adjective{}"]'.format(i + 1)).send_keys(adjective_choice[i])

    driver.find_element_by_xpath('//option[.="{}"]'.format(month_choice)).click()

    driver.find_element_by_xpath('//input[@value="Write me a sonnet"]').submit()

    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, '//div[@class="poem"]')))
    el = driver.find_element_by_xpath('//div[@class="poem"]')
    return el.text


if __name__ == '__main__':
    url = 'https://www.poem-generator.org.uk/sonnet/'
    driver = Chrome()
    driver.get(url)

    inputs = '//input[@type="button"][@value="Suggest"]'
    love_hate_options = '//option[..//select[@name="love_hate"]]'
    dates = '//option[..//select[@name="month"]]'
    javascript = '//script[@type="text/javascript"][3]'

    run = 0

    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located((By.XPATH, inputs)))

    saved_suggestions = {}
    if run == 0:
        suggestions = driver.find_element_by_xpath(javascript).get_attribute("innerHTML")
        suggestions = re.findall(r"suggestions\['(.+)'\] = new Array\((.+)\);", suggestions)
        for category in suggestions:
            title, data = category

            data = data.replace("'", "")
            saved_suggestions[title] = [x.strip() for x in data.split(",")]

    print(saved_suggestions)
    love_hate = ["love", "hate"]
    noun_sin = saved_suggestions["noun_sin"]
    aspects = saved_suggestions["aspects"]  # x3
    verbb = saved_suggestions["verbb"]  # x3
    adjective = saved_suggestions["adjective"]  # x8
    month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
             "November", "December"]

    aspects = list(combinations(aspects, 3))
    print(aspects)
    #
    verbb = list(combinations(verbb, 3))
    print(verbb)
    #
    adjective = list(adjective)
    random.shuffle(adjective)
    # print(adjective)

    print(month)

    group_length = 8
    total_number = len(love_hate) * len(noun_sin) * len(aspects) * len(verbb) * len(adjective) * len(month)
    current_Value = 1

    with open("documents.txt", 'w') as f:
        for feeling in love_hate:
            for noun in noun_sin:
                for aspect_choices in aspects:
                    for verb_choice in verbb:
                        for i in range(0, len(adjective) - group_length):
                            adjective_choice = adjective[i: i + group_length]

                            for month_choice in month:
                                result = fill_form(feeling, noun, aspect_choices, verb_choice, adjective_choice,
                                                   month_choice)
                                f.write(result)
                                f.write("\n-------------------------------------------------------\n")
                                f.flush()
                                i += 1
                                print("{} out of {}: {}%", i, total_number, i / total_number)
    driver.close()
