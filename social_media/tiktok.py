import time
import json
import random
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class tiktok_bot:
    def __init__(self, driver):
        self.driver = driver

    def click(self, path):
        try:
            element = self.driver.find_element(By.XPATH, path)
            element.click()
        except Exception as e:
            print(f"Error clicking element: {e}")

    def type_text(self, path, text):
        try:
            element = self.driver.find_element(By.XPATH, path)
            for char in text:
                element.send_keys(char)
                time.sleep(0.05)
        except Exception as e:
            print(f"Error typing text: {e}")
            
    def comment(self, path, text):
        try:
            element = self.driver.find_element(By.XPATH, path)
            for char in text:
                element.send_keys(char)
                time.sleep(0.05)
            element.send_keys(Keys.ENTER)
        except Exception as e:
            print(f"Error typing text: {e}")
    

def save_cookies(cookies, filename):
    with open(filename, 'w') as file:
        json.dump(cookies, file)

def load_cookies(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def login(driver, email, password, cookies):
    bot = tiktok_bot(driver)
    
    # Navigate to TikTok homepage
    driver.get("https://www.tiktok.com")

    # Check if cookies are available for login
    if cookies:
        # Load cookies into the browser
        for cookie in cookies:
            driver.add_cookie(cookie)

        print("Cookies loaded. Skipping login...")

        # Log the action to a report file
        with open("report.txt", "a") as file:
            file.write("Logged in using cookies.\n")

        return  # Exit the function after successful login via cookies

    # No cookies found, proceed with manual login
    driver.get('https://www.tiktok.com/login/phone-or-email/email')

    # Input email and password using the bot
    bot.type_text('//input[@type="text"]', email)
    time.sleep(1)
    bot.type_text('//input[@type="password"]', password)
    time.sleep(1)

    start_url = driver.current_url

    # Submit login form
    bot.click('//button[@type="submit"]')
    time.sleep(10)

    # Check if login failed by comparing URLs
    if driver.current_url == start_url:
        print("Automatic login failed. Please log in manually and then type 'ok' to continue.")
        confirm = input("Type 'ok' after you've manually logged in: ")

    # Get cookies after manual login
    cookies = driver.get_cookies()

    # Save cookies to a file
    save_cookies(cookies, 'tiktok_cookies.txt')
    
    print("Login successful. Credentials saved for future sessions.")


def comment_user_video(driver, user, comments, n):
    """
    Posts a number of comments on a user's latest TikTok video, accounting for pinned videos.
    
    :param driver: Selenium WebDriver instance controlling the browser.
    :param user: TikTok username whose video you want to comment on.
    :param comments: List of comments to randomly choose from.
    :param n: Number of comments to post.
    """

    # Navigate to the user's TikTok profile
    driver.get(f"https://www.tiktok.com/@{user}")

    # Count the number of pinned videos on the user's profile
    pinned_video_count = len(driver.find_elements(By.XPATH, '//div[@data-e2e="video-card-badge"]'))

    # Wait for the user profile to fully load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-e2e="user-post-item"]')))

    bot = tiktok_bot(driver)

    # Click on the user's first video
    bot.click('//div[@data-e2e="user-post-item"]')
    
    # If pinned videos exist, navigate through them
    if pinned_video_count > 0:
        for _ in range(pinned_video_count):
            bot.click('//button[@data-e2e="arrow-right"]')  # Click to skip pinned videos

    # Loop to post multiple comments
    for i in range(n):
        comment = random.choice(comments)

        # Wait for the comment input box to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]')))

        try:
            # Post the comment
            bot.comment('//div[@role="textbox"]', comment)

            print(f"Successfully posted comment on {user}'s latest video.")

        except Exception as e:
            print(f"Error while commenting...")

        # Wait for the 'Send' button to be clickable, then click to submit the comment
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@data-e2e="arrow-right"]')))
        bot.click('//button[@data-e2e="arrow-right"]')

    print(f"Successfully posted {n} comments on {user}'s video.")

def follow(driver, user):
    driver.get("https://www.tiktok.com/@" + user)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//button[@data-e2e="follow-button"]')))

    bot = tiktok_bot(driver)

    bot.click('//button[@data-e2e="follow-button"]')

    print(f"Successfully followed {user}.")



def upload(driver, path, titre):
    driver.get("https://www.tiktok.com/creator-center/upload")

    time.sleep(10)

    iframe = WebDriverWait(driver, 50).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))

    driver.switch_to.frame(iframe)
    
    upload_btn = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))

    upload_btn.send_keys(path)

    time.sleep(5)

    bot = tiktok_bot(driver)
    
    title_box = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, '//div[@role="combobox"]')))

    title_box.click()
    
    title_box.clear()
    
    bot.type_text('//div[@role="combobox"]', titre)

    time.sleep(5)

    driver.execute_script("arguments[0].scrollIntoView(true);", driver.find_element(By.XPATH, '//button[@class="css-y1m958"]'))
    
    WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '//button[@class="css-y1m958" and not(@disabled)]')))

    bot.click('//button[@class="css-y1m958"]')
               
    print(f"Video titled '{titre}' uploaded successfully from path: {path}")
