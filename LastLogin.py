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
    Label(master, text="PIN").grid(row=1)
    
    e1 = Entry(master)
    e2 = Entry(master, show='*')
    
    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    btSend = Button(master, text = 'ok', fg = 'red', command=lambda:[getInfo(),quit()])
    btSend.grid(row=2, column=2)
    
    master.mainloop()



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
  # =======  Try this solution: poll for the next item (Framework...) until it receives ====== .
print('   logging in')

# Find 'Employee' radio button and click (Note: this should conditional if the choices indeed popup.)
employeeButton = br.find_element_by_id('Framework_UI_Form_RadioButton_2') 
employeeButton.click()

# Find and hit "Next" button
nextButton = br.find_element_by_id('Button_1_label')
nextButton.click()

# maximize browser for better screenshot, and open calendar. Note: 'br.fullscreen_window()' would give even larger image if desired'
br.maximize_window()
print('   window maximized')
cal = br.find_element_by_xpath("//div[@class='FeatureIcon dfI_Nav_ESSMyCalendar']")
cal.click()


time.sleep(15)
br.save_screenshot('C:/Users/Baum/Desktop/sched.png')
print()
print('   screenshot saved to desktop')

# pull out data of month and add .png to file (ie: August 2019.png)
month = br.find_element_by_id('UI_Form__CalendarDropDownMixin_0_label')
month = month.text
monthp = month + '.png'
print('   current month:',month)

# get path of screenshot and rename the file with the current month from above (ie. August 2019.png)
x = Path('C:/Users/Baum/Desktop/sched.png')
# Note: include an extra directory (ie: '/documents') in the p = Path... because the next line (os.path...) will cut off the last directory of the path
p = Path("C:/Users/Baum/Desktop/Documents")
# join the path (C:/Users/Baum/Desktop/) with the file name (August 2019.png)
pp = os.path.join(os.path.dirname(p), monthp)
print('   path of current month:',pp)

# Note: create new name if file already exists
os.rename(x, pp)
print("    - current month ready")
print()

nexmonth = br.find_element_by_id('Button_36').click()
print('   move to next month')
time.sleep(5)
br.save_screenshot('C:/Users/Baum/Desktop/nexmonth.png')

month = br.find_element_by_id('UI_Form__CalendarDropDownMixin_0_label')
month = month.text
monthp = month + '.png'
print('   next month:',month)

x = Path('C:/Users/Baum/Desktop/nexmonth.png')

pp = os.path.join(os.path.dirname(p), monthp)

os.rename(x,pp)
print('    - next month file complete')




#if os.path.isfile('pp') == True :
#    month = month + ' 2' + '.png'
#    pp = os.path.join(os.path.dirname(p), month)
#    print('   new file name:', month)
#    print('   path of updated file:',pp)
