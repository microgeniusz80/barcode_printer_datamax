import pyautogui
import time
import pandas as pd

# Replace 'your_file.xlsx' with your actual Excel file path
df = pd.read_excel("data.xlsx", dtype=str, engine="openpyxl")

# Show first 5 rows
# print(df.head())




def type_things(image, text):
    time.sleep(0.1)
    res = pyautogui.locateCenterOnScreen(image, confidence=0.9)
    pyautogui.click(res)  # Click on the found image location
    pyautogui.typewrite(text)  # Type the text
    
def click_things(image):
    time.sleep(0.1)
    
    for attempt in range(3):
        res = pyautogui.locateCenterOnScreen(image, confidence=0.9)
        if res:
            pyautogui.click(res)
            return 'ada'
            break
        time.sleep(1)
    
    return 'tak ada'

def check_things(image):
    time.sleep(0.1)
    
    for attempt in range(3):
        res = pyautogui.locateCenterOnScreen(image, confidence=0.9)
        if res:
            # pyautogui.click(res)
            return 'ada'
            break
        time.sleep(1)
    
    return 'tak ada'
        
def click_things_xy(image, xy):
    time.sleep(0.1)
    
    for attempt in range(3):
        res = pyautogui.locateOnScreen(image, confidence=0.9)
        if res:
            click_x = res[0] + xy[0]
            click_y = res[1] + xy[1]
            pyautogui.click(click_x, click_y)
            break
        time.sleep(1)

def fill_form(ic):
    type_things('ic1.png', ic)
    type_things('ic2.png', ic)
    click_things('submit1.png')
    # click_things_xy('wow.png', [9, 9])
    # click_things_xy('yes.png', [9, 9])
    # type_things('search.png', 'path')
    # click_things('patho.png')
    click_things('startscreen.png')
    click_things('next.png')
    status = check_things('present.png')
    print(status)
    if status == 'ada':
        click_things('close.png')
        return 'ada'
    else:
        return 'tak ada'
    # click_things('next.png')
    
# fill_form('860404435298')


name_list = df["NO. KP"].tolist()

# print(name_list)
result = [[ic] for ic in name_list]

# result[0].append("done")
for index, name in enumerate(result):
    feedback = fill_form(name[0])
    if feedback == 'ada':
        result[index].append("done")
    else:
        result[index].append("not done")
    print(index, name)

# print(result)