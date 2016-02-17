'''
Testing some functions in PyAutoGui
Please instal pyautogui before running this script
'''
import pyautogui

# Fail-safe mode (prevent from ou of control)
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1.0 # pause each pyautogui function 1. sec

# testing screen shot
s = pyautogui.screenshot()
s.save('screenshot1.jpg')

print 'The resolution of your screen: ', pyautogui.size()

print 'Current position of mouse: ', pyautogui.position()

# Drag mouse to control some object on screen (such as googlemap at webpage)
distance = 100.
while distance > 0:
    pyautogui.dragRel(distance, 0, duration=2 , button='left')    # move right
    distance -= 25
    pyautogui.dragRel(0, distance, duration=2 , button='left')    # move down
    distance -= 25
    pyautogui.dragRel(-distance, 0, duration=2 , button='left')    # move right
    distance -= 25
    pyautogui.dragRel(0, -distance, duration=2 , button='left')    # move down
    distance -= 25

# scroll mouse wheel (zoon in and zoom out googlemap)
pyautogui.scroll(10, pause=1.)
pyautogui.scroll(-10, pause=1)

pyautogui.scroll(10, pause=1.)
pyautogui.scroll(-10, pause=1)

# message box
pyautogui.alert(text='pyautogui testing over, click ok to end', title='Alert', button='OK')



