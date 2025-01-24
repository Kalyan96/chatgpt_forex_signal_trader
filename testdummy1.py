import time

import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests

def get_session_token():
    browser = selenium.webdriver.Chrome()
    browser.get("https://beta.openai.com/")
    # username = browser.find_element(By.ID, "username")
    # password = browser.find_element(By.ID, "password")
    # username.send_keys("YOUR_USERNAME")
    # password.send_keys("YOUR_PASSWORD")
    # password.send_keys(Keys.ENTER)
    time.sleep(60)
    session_token = browser.execute_script("return window.session_token")
    return session_token

def get_completion(prompt):
    session_token = get_session_token()
    url = "https://beta.openai.com/v1/engines/davinci/completions"
    data = {"prompt": prompt, "session_token": session_token}
    response = requests.post(url, json=data)
    completion = response.json()["choices"][0]["text"]
    return completion

if __name__ == "__main__":
    prompt = "Write a poem about a cat."
    completion = get_completion(prompt)
    print(completion)
