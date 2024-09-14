import time
import os
from social_media import tiktok
from seleniumbase import Driver

# driver = Driver(headless=True)

# List of comments for a video
comments = [
    "Great video! Engaging and informative.",
    "Amazing content! Well-presented and insightful.",
    "Fantastic job! Your creativity shines through.",
    "Impressive video! Captivating from start to finish.",
    "Wonderful production! Keep up the excellent work.",
    "Bravo! Your storytelling is truly compelling.",
    "Exceptional video! It's both entertaining and educational.",
    "Outstanding work! Your talent is evident in every frame.",
    "Well done! Your video is a delight to watch.",
    "Kudos on a superb video! Your efforts are commendable.",
]

driver = Driver(uc=True)

driver.maximize_window()

def run_bot():
    """
    Main bot function that handles TikTok login, posting comments, following users, and uploading videos.
    """

    # Enter your Email and password 
    email = "youremail@example.com"
    password = "yourpassword"

    # Prompt for credentials if not provided
    if not email or not password:
        email = input("Please enter your email: ")
        password = input("Please enter your password: ")

    # Load cookies for login
    cookies = tiktok.load_cookies('tiktok_cookies.txt')

    tiktok.login(driver, email, password, cookies)

    tiktok.comment_user_video(driver, 'taylor', comments, 3)

    time.sleep(5)

    tiktok.follow(driver, 'amazon')

    time.sleep(2)

    # Upload a video
    file_path = os.path.join(os.path.dirname(__file__), "my_video.mp4")

    try:
        tiktok.upload(driver, file_path, 'Check out this cool video! #tiktok #viral')
    except Exception as e:
        print(f"Failed to upload video: {e}")

    # Final message
    print("Bot execution finished.")

    # Allow some time before closing
    time.sleep(10)

if __name__ == "__main__":
    run_bot()