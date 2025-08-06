import pyautogui
import cv2
import numpy as np
import time

ASSETS_FOLDER="assets/4k"
FIRST_ITEM_BUTTON_IMAGE_PATH = f"{ASSETS_FOLDER}/first_item_button.png"
ITEM_BUTTON_IMAGE_PATH = f"{ASSETS_FOLDER}/item_button.png"
SCROLL_BUTTON_IMAGE_PATH = f"{ASSETS_FOLDER}/scroll_button.png"
ENTRY_BUTTON_IMAGE_PATH = f"{ASSETS_FOLDER}/entry_button.png"
TITLE_BUTTON_IMAGE_PATH = f"{ASSETS_FOLDER}/title_button.png"
MODIFICATION_BUTTON_IMAGE_PATH = f"{ASSETS_FOLDER}/modification_button.png"

# Because we need to click the down of scroll button to move the page
SCROLL_CLICK_OFFSET = 50
FIRST_ITEM_HORIZONTAL_OFFSET = 30
MODIFICATION_CLICK_OFFSET = 10

WAITING_SEC = 0.005

MEETING_TITLE = "Phison MoE Sync Meeting"
DAYS = ["8/11 (mon)", "8/12 (tue)", "8/13 (wed)", "8/14 (thu)", "8/15 (fri)"]

def locate_button(image_path, confidence=0.8):
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(image_path, 0)
    result = cv2.matchTemplate(cv2.cvtColor(
        screenshot, cv2.COLOR_BGR2GRAY), template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= confidence:
        return max_loc
    else:
        return None


def add_vote_option(option, button_image_path, item_offset):
    button_location = locate_button(button_image_path)
    if button_location:
        pyautogui.doubleClick(
            button_location[0] + 10 + item_offset, button_location[1] + 10)
        time.sleep(WAITING_SEC)
        pyautogui.typewrite(option)
        time.sleep(WAITING_SEC)
        return True
    else:
        print(f"Could not locate the '輸入選項' button for option: {option}")
        return False


def scroll_page(scroll_image_path, offset):
    # locate and click the button of scroll button
    click_time = 3
    for _ in range(click_time):
        scroll_button = locate_button(scroll_image_path)
        if scroll_button:
            # Click near the center of the button
            pyautogui.click(scroll_button[0] + 10, scroll_button[1] + offset)
            time.sleep(WAITING_SEC)  # Wait for page moving
        else:
            print(f"Could not locate the 'scroll' button")
            return False
    return True


def click_entry_button(button_image_path):
    button_location = locate_button(button_image_path)
    if button_location:
        pyautogui.doubleClick(button_location[0], button_location[1])
        time.sleep(WAITING_SEC)
        return True
    else:
        print(f"Could not locate the entry button")
        return False


def add_vote_option_retry_once(option, item_button_image, item_offset, scroll_button_image, scroll_offset):
    if add_vote_option(option, item_button_image, item_offset):
        return True
    if scroll_page(scroll_button_image, scroll_offset):
        print(f"Scroll Success!")
        if add_vote_option(option, item_button_image, 0):
            return True
    return False


def set_title(option, item_button_image, item_offset):
    if add_vote_option(option, item_button_image, item_offset):
        return True
    return False


def click_modification_button(item_button_image, item_offset):
    button_location = locate_button(item_button_image)
    if button_location:
        # Click near the center of the button
        pyautogui.click(button_location[0] + 10 +
                        item_offset, button_location[1] + 10)
        time.sleep(WAITING_SEC)  # Wait for page to update
        return True
    else:
        print(f"Could not locate the modification button")
        return False


def generate_time_slot_options(days, time_ranges):
    options = []
    for day in days:
        for start_time, end_time in time_ranges:
            options.append(f"{day} {start_time} - {end_time}")

    return options


def main():
    days = DAYS
    time_ranges = [
        ("9:00", "10:30"),
        ("10:30", "12:00"),
        ("13:00", "14:30"),
        ("14:30", "16:00"),
        ("16:00", "17:30")
    ]
    options = generate_time_slot_options(days, time_ranges)

    print("Switch to the voting application window in 5 seconds...")
    time.sleep(2)

    # Click entry button
    click_entry_button(ENTRY_BUTTON_IMAGE_PATH)

    # set title
    set_title(MEETING_TITLE, TITLE_BUTTON_IMAGE_PATH, 0)

    # click
    click_modification_button(
        MODIFICATION_BUTTON_IMAGE_PATH, MODIFICATION_CLICK_OFFSET)

    # Add each option
    for index, option in enumerate(options):
        if index == 0:
            add_vote_option_retry_once(option, FIRST_ITEM_BUTTON_IMAGE_PATH,
                                       FIRST_ITEM_HORIZONTAL_OFFSET, SCROLL_BUTTON_IMAGE_PATH, SCROLL_CLICK_OFFSET)
        else:
            add_vote_option_retry_once(
                option, ITEM_BUTTON_IMAGE_PATH, 0, SCROLL_BUTTON_IMAGE_PATH, SCROLL_CLICK_OFFSET)


if __name__ == "__main__":
    main()
