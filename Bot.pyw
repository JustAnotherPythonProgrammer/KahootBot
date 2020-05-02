from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException


class Question:
    def __init__(self, q, a):
        self.q = q
        self.a = a



def getData(URL):
    print("\n")
    driver = Chrome()
    driver.get(URL)

    showAnswers = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(("css selector", "#layout > div.layout__body-wrapper > main > div.question-list-and-resource-credits > section > header > button")))
    showAnswers.click()

    WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(("class name", "question-list__item")))
    quests = driver.find_elements_by_class_name("question-list__item")

    arr = []
    for index, q in enumerate(quests):

        text = q.find_element_by_class_name("question-media__text-inner-wrapper")
        ans = q.find_elements_by_class_name("choices__choice")
        for a in ans:
            try:
                a.find_element_by_class_name("choices__choice--correct")
                element = a.find_element_by_tag_name("span")
                answer = a.text.split("\n")[0]
                answerShape = element.get_attribute("class").split("--")[1]
                arr.append(Question(text.text, answerShape))
                break
            except NoSuchElementException as e:
                pass


    print("Retrieved answers.")
    driver.close()
    return arr


def connectToLobby(pin):
    driver = Chrome()
    driver.get("https://kahoot.it/")
    pinBox = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(("css selector", "#game-input")))
    pinBox.send_keys(pin)
    confirm = driver.find_element_by_css_selector("#root > div > div > div > main > div > form > button")
    confirm.click()
    print("Connected to lobby.")
    return driver


def enterName(driver, name):
    nameBox = WebDriverWait(driver, 60).until(expected_conditions.presence_of_element_located(("css selector", "#nickname")))
    nameBox.send_keys(name)
    confirm = driver.find_element_by_css_selector("#root > div > div > div > main > div > form > button")
    confirm.click()
    print("Joined game.")


def playGame(driver, questions):

    selectors = {"triangle": "#root > div > main > div.question__PageMainContent-sc-12j7dwx-0.dhkrXm > div > button.card-button__CardButton-vbewcy-1.eRSCLD.flat-button__FlatButton-sc-6uljam-0.bbSHdR",
                 "diamond":  "#root > div > main > div.question__PageMainContent-sc-12j7dwx-0.dhkrXm > div > button.card-button__CardButton-vbewcy-1.fabXZJ.flat-button__FlatButton-sc-6uljam-0.bbSHdR",
                 "circle":   "#root > div > main > div.question__PageMainContent-sc-12j7dwx-0.dhkrXm > div > button.card-button__CardButton-vbewcy-1.eYFENK.flat-button__FlatButton-sc-6uljam-0.bbSHdR",
                 "square":   "#root > div > main > div.question__PageMainContent-sc-12j7dwx-0.dhkrXm > div > button.card-button__CardButton-vbewcy-1.bDfINc.flat-button__FlatButton-sc-6uljam-0.bbSHdR"}

    for num, q in enumerate(questions, start=1):
        button = WebDriverWait(driver, 600).until(expected_conditions.presence_of_element_located(("css selector", selectors[q.a])))
        button.click()
        print(f"Question {num} answered.")




def main():
    URL = input("URL: ")
    pin = input("PIN: ")
    name = input("NAME: ")
    questions = getData(URL)
    game = connectToLobby(pin)
    enterName(game, name)
    playGame(game, questions)

if __name__ == "__main__":
    main()
