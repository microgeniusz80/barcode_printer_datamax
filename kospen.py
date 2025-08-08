import pyautogui
import time
import pandas as pd


medical_history_yes = [10, 32]
medical_history_no = [71, 322]

# family_diabetes = [437, 161]
# family_hypertension = [20, 161]
# family_heart = [20, 186]
# family_stroke = [437, 186]
# family_mental = [855, 210]
# family_cancer = [20, 210]
# family_other = [20, 233]
# family_ckd = [855, 186]

family_illness_yes = [10, 30]
family_illness_no = [62, 32]

family_diabetes = [429, 108]
family_hypertension = [11, 107]
family_heart = [11, 131]
family_stroke = [427, 131]
family_mental = [850, 155]
family_cancer = [11, 155]
family_other = [10, 180]
family_ckd = [850, 131]

family_other_text = [13, 212]

# client_hypertension = [20, 400]
# client_diabetes = [438, 400]
# client_cholesterol = [855, 400]
# client_other = [20, 520]

client_hypertension = [10, 107]
client_diabetes = [320, 107]
client_cholesterol = [630, 107]
client_other = [10, 228]
client_other_enter = [14, 256]

mental_yes = [11, 91]
mental_no = [61, 91]

whooley_1_yes = [22, 140]
whooley_1_no = [73, 140]
whooley_2_yes = [22, 207]
whooley_2_no = [73, 207]

gad_1_a = [22, 370]
gad_1_b = [22, 393]
gad_1_c = [22, 418]
gad_1_d = [22, 443]

gad_2_a = [22, 511]
gad_2_b = [22, 536]
gad_2_c = [22, 559]
gad_2_d = [22, 583]

alcohol_no = [106, 152]

def type_things(image, text):
    time.sleep(1)
    res = pyautogui.locateCenterOnScreen(image, confidence=0.9)
    pyautogui.click(res)  # Click on the found image location
    pyautogui.typewrite(text)  # Type the text
    
def click_things(image):
    time.sleep(1)
    
    for attempt in range(3):
        res = pyautogui.locateCenterOnScreen(image, confidence=0.9)
        if res:
            pyautogui.click(res)
            break
        time.sleep(1)
        
def click_things_xy(image, xy):
    time.sleep(1)
    
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
    
    # click_things_xy('anchor.png', client_hypertension)
    
    # pyautogui.press('end')
    
    # click_things('continue.png')
    
fill_form('920809075026')


def test():
    click_things_xy('family_anchor.png', family_illness_yes)


    click_things_xy('family_anchor.png', family_hypertension)
    click_things_xy('family_anchor.png', family_diabetes)
    click_things_xy('family_anchor.png', family_heart)
    click_things_xy('family_anchor.png', family_stroke)
    click_things_xy('family_anchor.png', family_ckd)
    click_things_xy('family_anchor.png', family_mental)
    click_things_xy('family_anchor.png', family_cancer)
    click_things_xy('family_anchor.png', family_other)
    click_things_xy('family_anchor.png', family_other_text)


    click_things_xy('client_anchor.png', medical_history_yes)
    click_things_xy('client_anchor.png', client_cholesterol)
    click_things_xy('client_anchor.png', client_diabetes)
    click_things_xy('client_anchor.png', client_hypertension)
    click_things_xy('client_anchor.png', client_other)
    click_things_xy('client_anchor.png', client_other_enter)