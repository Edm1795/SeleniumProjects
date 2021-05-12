from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
import time
import pickle
import os
from pathlib import Path

# Note: Dayforce just after loging in ask for a another click ('employee') which this program does not take into account
# Notes: the last section of code, the if block is not locating the file
# asked for and so it always returns false and therefore is not renaming the file
# the 'pp' path is not working, hard code does work however.

# Create Interface and get Credentials from user

try:
    # Check if file with credentials already exists. If so take data from file
    pickleRead = open('data.pickle','rb')
    data = pickle.load(pickleRead)
    pickleRead.close()
     
    
except:
   # If file does not exist, ask user to input credentials

    def getInfo():
        ''' 
        Inputs: none
        Outputs: none
        Gets credentials from user and also runs PickleIn --> writes creds to pickle file
        '''
        username = e1.get()
        PIN = e2.get()
        cred = (username, PIN)
        pickleWrite(cred)
        
        
    def pickleWrite(cred):
        '''
        Inputs: credentials from getInfo()--> a tuple with username and PIN
        Outputs: none
        writes creds to pickle file
        '''
        
        pickleHand = open('data.pickle', 'wb')
        pickle.dump(cred,pickleHand)
        pickleHand.close()    
    
    master = Tk()
    master.title('Last Login')
    master.geometry('400x150')
    
    # Gets the requested values of the height and width.
    windowWidth = master.winfo_reqwidth()
    windowHeight = master.winfo_reqheight()
    
     
    # Gets both half the screen width/height and window width/height
    positionRight = int(master.winfo_screenwidth()/2 - windowWidth/2)
    positionDown = int(master.winfo_screenheight()/2 - windowHeight/2)
    
    master.geometry("+{}+{}".format(positionRight, positionDown))
    
    
    Label(master, text="Username").grid(row=0)
    Label(master, text="Password").grid(row=1)
    
    e1 = Entry(master)
    e2 = Entry(master, show='*')
    
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    btSend = Button(master, text = 'ok', fg = 'red', command=lambda:[getInfo(),quit()]) # switch out quit() for master.destroy() -
    # does allow the program to continue on past the master.mainloop, -
    # however there will be a problem with the data.pickle file. Not sure what causes that.
    btSend.grid(row=2, column=2)
    
    master.mainloop()

def GetCurrentMonth(br):
    
    ''' Gets string for the month and year showing on screen (eg: 'July 2021') and returns the month only (eg:'July')
    Inputs: br --> the web browser driver
    Outputs: string of the current month (eg: 'July')
    '''
    
    currentMonthWebElement = br.find_element_by_id("UI_Form__CalendarDropDownMixin_0_label")
    currentMonthString = currentMonthWebElement.text # format eg: 'July 2021'
    currentMonthList = currentMonthString.split(" ") # Creates list from string: ['July','2021']
    
    return currentMonthList[0] # eg: ['July','2021'] --> returns month string: 'July'

def CalculateNextMonth(currentMonthString):
    
    '''Calculate what the next month should be based on the current month.
    Inputs: currentMonthString (eg: 'July')
    Outputs: String of next month: (eg: 'August')
    '''
    
    monthList = ['January','February','March','April','May','June','July','August']
    nextMonthIndex = monthList.index(currentMonthString) + 1
    nextMonthString = monthList[nextMonthIndex]
    
    return nextMonthString



print('   Program starting')
br = webdriver.Firefox() #Automatically waits for browser to load before moving on
print('   opening browser')
br.get('https://www.dayforcehcm.com') # Automatically waits for completion of load before moving to next line

#br.implicitly_wait(10) # waits maximum of 10 seconds for all elements to load -- not needed as function automatically waits

# find elements on login page
comp = br.find_element_by_id('txtCompanyName')
usrnam = br.find_element_by_id('txtUserName')
passw = br.find_element_by_id('txtUserPass')

# send login credentials
comp.send_keys('epl')
usrnam.send_keys(data[0]) # replace with data[0] and [1]day
passw.send_keys(data[1])
print('   login credentials entered')

# find and hit login button
logbtn = br.find_element_by_id('MainContent_loginUI_cmdLogin')
logbtn.click() 
  # This button waits but not for total completion, therefore the next search comes back empty. There is delay but not long enough 
  # upon researching here https://groups.google.com/g/webdriver/c/7K2QWGVNCYo this function will not 
  # wait as it does not know how, part of the halting problem. Best to test for presence of a certain
  # element at the bottom of the page or use a wait function.
  # =======  Try this solution: poll for the next item (Framework...) until it receives ====== . --> note: tested and works well
print('   logging in')

# Find 'Employee' radio button and click (Note: this should conditional if the choices indeed popup.)

# Try to seek "Framework_UI..." element, once found, stop loop and click button

SelAccountType = True

while SelAccountType:
    
    try:
        employeeButton = br.find_element_by_id('Framework_UI_Form_RadioButton_2')
        SelAccountType = False
    except:
        pass
    
employeeButton.click()

# Find and hit "Next" button
nextButton = br.find_element_by_id('Button_1_label')
nextButton.click()

# maximize browser for better screenshot, and open calendar. Note: 'br.fullscreen_window()' would give even larger image if desired'
br.maximize_window()
print('   window maximized')

# Find calendar button, check for it until finds
FindCal = True

while FindCal:

    try:
        cal = br.find_element_by_xpath("//div[@class='FeatureIcon dfI_Nav_ESSMyCalendar']")
        FindCal = False
    except:
        pass

cal.click()

# First screen shot here:
# Poll for an element of the webpage to determine when page has loaded (polls for '01' text string in the calendar using xpath search
WaitForScreen = True

while WaitForScreen:

    try:
        Fragment = br.find_element_by_xpath("//div[contains(text(),\'01')]")
        WaitForScreen = False
    except:
        pass


# Grab name of month showing (for use later in program, when grabbing next month's screenshot)

currentMonthString = GetCurrentMonth(br) # used for argument for CalculateNextMonth()

print(' ============= testing GetCurrentMonth() Function: ',currentMonthString)

#time.sleep(15) # Consider removing this delay and instead search the page until it find the element of the first day of the week (01). Or search
# for class DayLabel
br.save_screenshot('C:/Users/j/Desktop/sched.png') #switched: "...Users/Baum/...", for "...Users/j/..."
print()
print('   screenshot saved to desktop')

# pull out data of month and add .png to file (ie: August 2019.png)
month = br.find_element_by_id('UI_Form__CalendarDropDownMixin_0_label')
month = month.text
monthp = month + '.png'
print('   current month:',month)

# get path of screenshot and rename the file with the current month from above (ie. August 2019.png)
x = Path('C:/Users/j/Desktop/sched.png')               #switched: "...Users/Baum/...", for "...Users/j/..."
# Note: include an extra directory (ie: '/documents') in the p = Path... because the next line (os.path...) will cut off the last directory of the path
p = Path("C:/Users/j/Desktop/Documents")               #switched: "...Users/Baum/...", for "...Users/j/..."
# join the path (C:/Users/j/Desktop/) with the file name (August 2019.png)
pp = os.path.join(os.path.dirname(p), monthp)
print('   path of current month:',pp)


# check if file already exists, if so rename file with (1)

rename = True
while rename:
    try:
        os.rename(x, pp)
        rename = False
    except:
        month = month + '(1)'
        monthp = month + '.png'
        pp = os.path.join(os.path.dirname(p), monthp)
        
    
print("    - current month ready")
print()

#time.sleep(5) Remove this delay and replace with search loop seeking element from page

# Poll for an element of the webpage to determine when page has loaded (polls for '01' text string in the calendar using xpath search
# Note:the second month tends to come out partly blank; the screen shot is taken slightly before the full page loads. 
# Try this solution: I think that the 
# variable receiving the element should be given a new name (other than Fragment) because it carries the previous value from the first month. -->
# This did not work (using SecondFragment = br.find....)
# I think it is finding the "01" from the original page.
# Try this: the only element properly changing is the name of the month (June to July...) The original month is fine, but then have it search for
# the next month after that. Build a function that grabs the original month and then goes up one month from there and searches for that string.

# Xpath ID for element containing month and year with a space (eg. June 2021): //*[@id="UI_Form__CalendarDropDownMixin_0_label"]

nexmonth = br.find_element_by_id('Button_36').click()
print('   move to next month')

# Setting up for second screen shot:
nextMonth = CalculateNextMonth(currentMonthString)
WaitForScreen = True

print()
print('============== Testing Get Current Month Function =============:', nextMonth)
print()
# This below works code wise however the month name is loaded ahead of the calendar therefore the
# screenshot still comes out without the calendar. Solution: after determining the month has moved, then 
# poll for the 01!
while WaitForScreen:
    
    print('Checking if screen has loaded title for new month:',GetCurrentMonth(br), nextMonth)
    print()
    if GetCurrentMonth(br) == nextMonth:
        print('post if statement',GetCurrentMonth(br), nextMonth)
        
        WaitForScreen = False
    else:
        continue

# Now that the month is determined to have moved, now you can poll for the 01 and know it is 
# for a new month.
print()
c = 1
WaitForScreen = True # set back to true since the previous block set it to False
while WaitForScreen:

    try:
        print(str(c) + ' searching for calendar element 28')
        c += 1
        SecondFragment = br.find_element_by_xpath("//div[contains(text(),\'28')]")
        WaitForScreen = False
    except:
        pass


br.save_screenshot('C:/Users/j/Desktop/nexmonth.png') #switched: "...Users/Baum/...", for "...Users/j/..."

month = br.find_element_by_id('UI_Form__CalendarDropDownMixin_0_label')
month = month.text
monthp = month + '.png'
print('   next month:',month)

x = Path('C:/Users/j/Desktop/nexmonth.png') #switched: "...Users/Baum/...", for "...Users/j/..."

pp = os.path.join(os.path.dirname(p), monthp)

# check if file already exists if so rename file with (1)
rename = True
while rename:
    try:
        os.rename(x, pp)
        rename = False
    except:
        month = month + '(1)'
        monthp = month + '.png'
        pp = os.path.join(os.path.dirname(p), monthp)


print('    - next month file complete')
print()
print('Both months saved to Desktop;')
print()
print("Job Completed")




#if os.path.isfile('pp') == True :
#    month = month + ' 2' + '.png'
#    pp = os.path.join(os.path.dirname(p), month)
#    print('   new file name:', month)
#    print('   path of updated file:',pp)
