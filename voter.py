import random

from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def find_option_selectors(driver, gender, timeout):
    xpath = '//div[..//..//..//..//div[@class="question-title-box"]//div//div//span[contains(text(), ' \
            '"{}")]][@class="select-placeholder"]'.format(gender)

    print(xpath)

    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return driver.find_elements_by_xpath(xpath)


def get_important_person(option_list, order):
    options = option_list.find_elements_by_xpath("./li/div/span")

    def ordering(x):
        x = x.text
        if x in order:
            return order[x]
        return 0

    results = list(map(ordering, options))

    v = set(map(lambda x: x.text.title(), options))
    if any(results):
        return max(options, key=ordering), v
    return options[random.randint(0, len(options) - 1)], v


def go_though_options(driver, question_option_list, timeout, order):
    p = set()

    for element in question_option_list:
        element.click()

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'select-option-menu-container')))
        option_list = driver.find_element_by_class_name("select-option-menu-container")

        option, people = get_important_person(option_list, order)
        p.update(people)
        option.click()

    return p


def fill_in_other(driver, order, gender):
    inputs = driver.find_elements_by_xpath(
        '//input[../../..//div//div//span[.="Other"]][../..//..//..//..//div['
        '@class="question-title-box"]//div//div//span[contains(text(), "{}")]]'.format(gender))

    preferred_input = max(order.keys(), key=lambda x: order[x])

    for textfield in inputs:
        textfield.send_keys(preferred_input)


def submit(driver):
    submit_button = driver.find_element_by_class_name("button-content")
    submit_button.click()


def resubmit(driver, timeout):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, '//a[.="Submit another response"]')))
    driver.find_element_by_xpath('//a[.="Submit another response"]').click()


def go_though_gender_selection(browser, delay, gender, priority_order):
    selections = find_option_selectors(browser, gender, delay)
    people = go_though_options(browser, selections, delay, priority_order)

    if len(priority_order) > 0:
        people_options = priority_order.copy()
    else:
        people_options = {key: random.random() for key in people}

    if "Other" in people_options:
        del people_options["Other"]
    print(people_options)
    fill_in_other(browser, people_options, gender)


if __name__ == '__main__':
    priority_order = {
        "Male": {
            "W. Hubbard": 3, "Other": 2, "Vernon": 1
        },
        "Female": {

        }
    }
    browser = Chrome()
    number_of_submits = 500
    delay = 10
    url = "http://tinyurl.com/votehubbard"

    browser.get(url)

    for i in range(number_of_submits):
        for gender in priority_order:
            go_though_gender_selection(browser, delay, gender, priority_order[gender])

        submit(browser)

        print("Number of submits:", i)

        if number_of_submits > 1:
            resubmit(browser, delay)
    browser.close()
