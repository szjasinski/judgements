

# driver = webdriver.Chrome(executable_path="/Users/szymon/PycharmProjects/Judgements/chromedriver")
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()


from selenium.webdriver import Chrome, ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys







def browser_function():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_experimental_option("detach", True)

    driver = Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://orzeczenia.nsa.gov.pl/cbo/query"
    driver.get(url)

    # window_before = driver.window_handles[0]

    elem = driver.find_element(By.ID, "hasla")

    x = "Podatek od czynności cywilnoprawnych!"
    elem.send_keys(x)

    # szukaj = driver.find_element(By.XPATH, "//option[@value='Szukaj']")

    szukaj = driver.find_element(By.XPATH, "//input[@type='submit']")
    szukaj.click()

    # window_after = driver.window_handles[1]

    info_lists = driver.find_elements(By.CLASS_NAME, "info-list-value")
    wyroki = [info_lists[i] for i in range(0, len(info_lists), 2)]
    linki = [wyroki[i].find_element(By.PARTIAL_LINK_TEXT, 'Wyrok') for i in range(len(wyroki))]

    # for i in linki:
    #     print(i.text)

    linki[0].click()

    elem = driver.find_element(By.CLASS_NAME, "war_header")
    print(elem.text)

    z = "lista-label"
    w = "info-list-value"




    # driver.switch_to.window(window_after)


    # driver.quit()

browser_function()
