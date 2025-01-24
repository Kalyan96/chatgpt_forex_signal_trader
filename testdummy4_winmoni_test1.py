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
# window_title = '*Untitled - Notepad'
window_title = '22601456: AdmiralMarkets-Demo - Demo Account - Admiral Markets Group AS - [EURUSD,M5]'

# Interval between screenshots (in seconds)
interval_seconds = 3600  #

# Initialize the Telegram Bot
bot = Bot(token=telegram_token)

# Offset in inches
inch_offset = 4

# Initialize the Telegram Bot
bot = Bot(token=telegram_token)

def inches_to_pixels(inches):
    # Calculate the number of pixels for the given inches
    return int(inches * 96)  # Assuming 96 DPI

def background_screenshot(hwnd, save_path):
    try:
        # Get the client area dimensions
        rect = win32gui.GetClientRect(hwnd)

        # Calculate the offset in pixels
        x_offset = inches_to_pixels(inch_offset)
        y_offset = inches_to_pixels(inch_offset)

        # Adjust the dimensions with the offset
        rect = (rect[0], rect[1], rect[2] + x_offset, rect[3] + y_offset)

        # Create a device context (DC) for the window
        wDC = win32gui.GetWindowDC(hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()

        # Create a bitmap compatible with the adjusted client area
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, rect[2], rect[3])
        cDC.SelectObject(dataBitMap)

        # BitBlt the content of the window's client area
        cDC.BitBlt((0, 0), (rect[2], rect[3]), dcObj, (0, 0), win32con.SRCCOPY)

        # Save the bitmap to a file
        dataBitMap.SaveBitmapFile(cDC, save_path)

        # Clean up
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        return True
    except Exception as e:
        print(f"Error capturing background screenshot: {e}")
        return False

def convert_to_png(bitmap_path, png_path):
    try:
        image = Image.open(bitmap_path)
        image.save(png_path, format="PNG")
        return True
    except Exception as e:
        print(f"Error converting to PNG: {e}")
        return False

def get_window_screenshot(title, save_path):
    try:
        hwnd = win32gui.FindWindow(None, title)
        if hwnd != 0:
            # Save the bitmap image to a file
            if background_screenshot(hwnd, save_path):
                # Convert the bitmap image to PNG
                png_path = save_path.replace('.bmp', '.png')
                if convert_to_png(save_path, png_path):
                    return png_path
                else:
                    print(f"Failed to convert to PNG.")
            else:
                print(f"Failed to capture background screenshot.")
            return None
        else:
            print(f"Window with title '{title}' not found.")
            return None
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
        return None

def send_screenshot_to_telegram(chat_id, image_path):
    try:
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=chat_id, photo=InputFile(photo))
        print(f"Screenshot sent to Telegram.")
    except Exception as e:
        print(f"Error sending screenshot to Telegram: {e}")

if __name__ == "__main__":
    while True:
        screenshot_path = 'screenshot.png'
        screenshot_png_path = get_window_screenshot(window_title, screenshot_path)
        if screenshot_png_path:
            send_screenshot_to_telegram(telegram_chat_id, screenshot_png_path)
        time.sleep(interval_seconds)
