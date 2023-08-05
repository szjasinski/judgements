from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def get_wyrok_dict(driver):
    tytuł = driver.find_element(By.CLASS_NAME, "war_header").text
    orzeczenie = {"nazwa": tytuł}

    keys = driver.find_elements(By.CLASS_NAME, "lista-label")
    keys = [i.text for i in keys]

    values = driver.find_elements(By.CLASS_NAME, "info-list-value")
    values = [i.text for i in values]

    reszta = driver.find_elements(By.CLASS_NAME, "info-list-value-uzasadnienie")
    sentencja_value = reszta[0].text
    if 'UZASADNIENIE' in keys:
        uzasadnienie_value = reszta[1].text

    for key, value in zip(keys, values):
        orzeczenie[key] = value

    orzeczenie['SENTENCJA'] = sentencja_value
    orzeczenie['UZASADNIENIE'] = uzasadnienie_value

    print(orzeczenie)
    return orzeczenie


def get_wyrok_links_list(driver):

    info_lists = driver.find_elements(By.CLASS_NAME, "info-list-value")
    wyroki = [info_lists[i] for i in range(0, len(info_lists), 2)]
    linki = [wyroki[i].find_element(By.PARTIAL_LINK_TEXT, 'Wyrok') for i in range(len(wyroki))]

    return linki


def go_to_wyroks_page(driver):
    elem = driver.find_element(By.ID, "hasla")

    x = "Podatek od czynności cywilnoprawnych!"
    elem.send_keys(x)

    # szukaj = driver.find_element(By.XPATH, "//option[@value='Szukaj']")

    szukaj = driver.find_element(By.XPATH, "//input[@type='submit']")
    szukaj.click()

def browser_function():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://orzeczenia.nsa.gov.pl/cbo/query"
    driver.get(url)

    # database is a list of dictionaries, each containing data of a single judgement
    database = []

    go_to_wyroks_page(driver)
    links = get_wyrok_links_list(driver)
    for link in links:
        link.click()
        judgement_data = get_wyrok_dict(driver)
        database.append(judgement_data)
        driver.back()


    # driver.quit()


if __name__ == "__main__":
    browser_function()
