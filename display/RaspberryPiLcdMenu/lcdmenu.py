                                                                  #!/usr/bin/python
#
# Created by Alan Aufderheide, February 2013
#
# This provides a menu driven application using the LCD Plates
# from Adafruit Electronics.
## Edited by Forrest Fuqua [JRWR] for the modern LCD Plate Lib + Hatnas Oper Menu
import commands
import textwrap
import os
from string import split
from time import sleep, strftime, localtime, strptime
from datetime import datetime, timedelta
from xml.dom.minidom import *
import Adafruit_CharLCD as LCD
from ListSelector import ListSelector


import pyotp
import psutil

configfile = 'lcdmenu.xml'
# set DEBUG=1 for print debug statements
DEBUG = 1
DISPLAY_ROWS = 2
DISPLAY_COLS = 16

# set to 0 if you want the LCD to stay on, 1 to turn off and on auto
AUTO_OFF_LCD = 1

lcd = LCD.Adafruit_CharLCDPlate()
# commands
def DoQuit():
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            lcd.set_backlight(0)
            quit()
        sleep(0.25)

def DoShutdown():
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            lcd.set_backlight(0)
            lcd.message("Shutting Down")
            out = commands.getoutput("/sbin/shutdown -h now")
            lcd.message(out)
            sleep(10)
            quit()
        sleep(0.25)

def DoReboot():
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            lcd.set_backlight(0)
            lcd.message("Rebooting!")
            out = commands.getoutput("/sbin/shutdown -r now")
	    lcd.message(out)
	    sleep(10)
            quit()
        sleep(0.25)

def LcdOff():
	lcd.set_backlight(0)
def LcdOn():
	lcd.set_backlight(1)
def LcdRed():
	lcd.set_color(1.0, 0.0, 0.0)
def LcdGreen():
	lcd.set_color(0.0, 1.0, 0.0)
def LcdBlue():
	lcd.set_color(0.0, 0.0, 1.0)
def LcdYellow():
	lcd.set_color(1.0, 1.0, 0.0)
def LcdTeal():
	lcd.set_color(0.0, 1.0, 1.0)
def LcdViolet():
	lcd.set_color(1.0, 0.0, 1.0)
def ShowDateTime():
    if DEBUG:
        print('in ShowDateTime')
    lcd.clear()
    while not(lcd.is_pressed(LCD.LEFT)):
        sleep(0.25)
        lcd.home()
        lcd.message(strftime('%a %b %d %Y\n%I:%M:%S %p', localtime()))
    
def ValidateDateDigit(current, curval):
    # do validation/wrapping
    if current == 0: # Mm
        if curval < 1:
            curval = 12
        elif curval > 12:
            curval = 1
    elif current == 1: #Dd
        if curval < 1:
            curval = 31
        elif curval > 31:
            curval = 1
    elif current == 2: #Yy
        if curval < 1950:
            curval = 2050
        elif curval > 2050:
            curval = 1950
    elif current == 3: #Hh
        if curval < 0:
            curval = 23
        elif curval > 23:
            curval = 0
    elif current == 4: #Mm
        if curval < 0:
            curval = 59
        elif curval > 59:
            curval = 0
    elif current == 5: #Ss
        if curval < 0:
            curval = 59
        elif curval > 59:
            curval = 0
    return curval

def SetDateTime():
    if DEBUG:
        print('in SetDateTime')
    # M D Y H:M:S AM/PM
    curtime = localtime()
    month = curtime.tm_mon
    day = curtime.tm_mday
    year = curtime.tm_year
    hour = curtime.tm_hour
    minute = curtime.tm_min
    second = curtime.tm_sec
    ampm = 0
    if hour > 11:
        hour -= 12
        ampm = 1
    curr = [0,0,0,1,1,1]
    curc = [2,5,11,1,4,7]
    curvalues = [month, day, year, hour, minute, second]
    current = 0 # start with month, 0..14

    lcd.clear()
    lcd.message(strftime("%b %d, %Y  \n%I:%M:%S %p  ", curtime))
    lcd.blink()
    lcd.set_cursor(curc[current], curr[current])
    sleep(0.5)
    while 1:
        curval = curvalues[current]
        if lcd.is_pressed(LCD.UP):
            curval += 1
            curvalues[current] = ValidateDateDigit(current, curval)
            curtime = (curvalues[2], curvalues[0], curvalues[1], curvalues[3], curvalues[4], curvalues[5], 0, 0, 0)
            lcd.home()
            lcd.message(strftime("%b %d, %Y  \n%I:%M:%S %p  ", curtime))
            lcd.set_cursor(curc[current], curr[current])
        if lcd.is_pressed(LCD.DOWN):
            curval -= 1
            curvalues[current] = ValidateDateDigit(current, curval)
            curtime = (curvalues[2], curvalues[0], curvalues[1], curvalues[3], curvalues[4], curvalues[5], 0, 0, 0)
            lcd.home()
            lcd.message(strftime("%b %d, %Y  \n%I:%M:%S %p  ", curtime))
            lcd.set_cursor(curc[current], curr[current])
        if lcd.is_pressed(LCD.RIGHT):
            current += 1
            if current > 5:
                current = 5
            lcd.set_cursor(curc[current], curr[current])
        if lcd.is_pressed(LCD.LEFT):
            current -= 1
            if current < 0:
                lcd.blink(0)
                return
            lcd.set_cursor(curc[current], curr[current])
        if lcd.is_pressed(LCD.SELECT):
            # set the date time in the system
            lcd.blink(0)
            os.system(strftime('sudo date --set="%d %b %Y %H:%M:%S"', curtime))
            break
        sleep(0.25)

    lcd.blink(0)

def ShowIPAddress():
    if DEBUG:
        print('in ShowIPAddress')
    lcd.clear()
    lcd.message(commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1][5:])
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        sleep(0.25)
#only use the following if you find useful
def Use10Network():
    "Allows you to switch to a different network for local connection"
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        if lcd.is_pressed(LCD.SELECT):
            # uncomment the following once you have a separate network defined
            #commands.getoutput("sudo cp /etc/network/interfaces.hub.10 /etc/network/interfaces")
            lcd.clear()
            lcd.message('Please reboot')
            sleep(1.5)
            break
        sleep(0.25)

#only use the following if you find useful
def UseDHCP():
    "Allows you to switch to a network config that uses DHCP"
    lcd.clear()
    lcd.message('Are you sure?\nPress Sel for Y')
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        if lcd.is_pressed(LCD.SELECT):
            # uncomment the following once you get an original copy in place
            #commands.getoutput("sudo cp /etc/network/interfaces.orig /etc/network/interfaces")
            lcd.clear()
            lcd.message('Please reboot')
            sleep(1.5)
            break
        sleep(0.25)

def ShowLatLon():
    if DEBUG:
        print('in ShowLatLon')

def SetLatLon():
    if DEBUG:
        print('in SetLatLon')
    
def SetLocation():
    if DEBUG:
        print('in SetLocation')
    global lcd
    list = []
    # coordinates usable by ephem library, lat, lon, elevation (m)
    list.append(['New York', '40.7143528', '-74.0059731', 9.775694])
    list.append(['Paris', '48.8566667', '2.3509871', 35.917042])
    selector = ListSelector(list, lcd)
    item = selector.Pick()
    # do something useful
    if (item >= 0):
        chosen = list[item]

def CompassGyroViewAcc():
    if DEBUG:
        print('in CompassGyroViewAcc')

def CompassGyroViewMag():
    if DEBUG:
        print('in CompassGyroViewMag')

def CompassGyroViewHeading():
    if DEBUG:
        print('in CompassGyroViewHeading')

def CompassGyroViewTemp():
    if DEBUG:
        print('in CompassGyroViewTemp')

def CompassGyroCalibrate():
    if DEBUG:
        print('in CompassGyroCalibrate')
    
def CompassGyroCalibrateClear():
    if DEBUG:
        print('in CompassGyroCalibrateClear')
    
def TempBaroView():
    if DEBUG:
        print('in TempBaroView')

def TempBaroCalibrate():
    if DEBUG:
        print('in TempBaroCalibrate')
    
def AstroViewAll():
    if DEBUG:
        print('in AstroViewAll')

def AstroViewAltAz():
    if DEBUG:
        print('in AstroViewAltAz')
    
def AstroViewRADecl():
    if DEBUG:
        print('in AstroViewRADecl')

def CameraDetect():
    if DEBUG:
        print('in CameraDetect')
    
def CameraTakePicture():
    if DEBUG:
        print('in CameraTakePicture')

def CameraTimeLapse():
    if DEBUG:
        print('in CameraTimeLapse')

def NASDelete():
    lcd.clear()
    lcd.message('DELETE MODE\n=ACTIVE=');
    sleep(2)
    word = GetWord()
    lcd.message('Sure? ' + word + '\nPress Sel for Y')
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            out = commands.getoutput("php /root/scripts/deletenum.php " + word)
	    lcd.message(''.join(textwrap.wrap(out, 16)))
	    sleep(5)
	    lcd.clear()
            break
        sleep(0.25)

def GetGPSTime():
    lcd.clear()
    lcd.message("Grabbing Time")
    while not(lcd.is_pressed(LCD.LEFT)):
        sleep(0.25)
	out = commands.getoutput("/bin/bash /root/scripts/getgpstime.sh 2>/dev/null")
        lcd.home()
        lcd.message(strftime('%a %b %d %Y\n%I:%M:%S %p', strptime(out, "%Y-%m-%d %H:%M:%S")))

def SetGPSTime():
    lcd.clear()
    lcd.message("Syncing Time")
    out = commands.getoutput("/bin/bash /root/scripts/gpssynctime.sh")
    lcd.clear()
    ShowDateTime()

def KillGPSTime():
	lcd.clear()
	lcd.message("Killing GPSD")
	commands.getoutput("killall gpsd")
	lcd.clear()

def NASHide():
    lcd.clear()
    lcd.message('HIDE MODE\n=ACTIVE=');
    sleep(2)
    word = GetWord()
    lcd.message('Sure? ' + word + '\nPress Sel for Y')
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            out = commands.getoutput("php /root/scripts/deletenum.php " + word + " 1")
            lcd.message(''.join(textwrap.wrap(out, 16)))
            sleep(5)
            lcd.clear()
            break
        sleep(0.25)
def SoftReboot():
    lcd.clear()
    lcd.message('SOFT REBOOT!');
    sleep(2)
    word = GetWord()
    lcd.message('Soft Reboot?\nPress Sel for Y')
    while 1:
        if lcd.is_pressed(LCD.LEFT):
            break
        if lcd.is_pressed(LCD.SELECT):
            lcd.clear()
            out = commands.getoutput("bash /root/scripts/firewall.sh")
            lcd.message(''.join(textwrap.wrap(out, 16)))
            sleep(5)
            lcd.clear()
            break
        sleep(0.25)

def spinning_cursor():
    while True:
        for cursor in '<>':
            yield cursor

def HatNasLock():
    lock = 1
    spinner = spinning_cursor()
    lcd.message("[HATNAS] LOCKED")
    sleep(0.5)
    lcd.clear()
    oldclientnum = 0
    oldfilenum = 0
    while lock == 1 :
     if lock == 0:
        return None
     if lcd.is_pressed(LCD.UP):
                word = GetWord()
                lcd.clear()
                lcd.home()
                if word is not None:
                        totp = pyotp.TOTP('C2IUA4AWM5ILSBLR')
                        if totp.now()[:2] == word :
				lock = 0
                                lcdstart = datetime.now()
                                return None
			else:
				lcd.message('~BAD PASSWORD~')
         			lcd.set_backlight(1)
         			lcd.set_color(0.0, 1.0, 0.0)
         			sleep(0.1)
         			lcd.set_backlight(0)
         			sleep(1)
				lcd.clear()
     cpu = int(round(psutil.cpu_percent(interval=None)))
     lcd.set_cursor(0,0)
     spin = spinner.next()
     lcd.message('%'+str(cpu).zfill(2))
     lcd.set_cursor(4,0)
     lcd.message(''+spinner.next()+'HATNAS'+spinner.next())
     lcd.set_cursor(13,0)
     num_lines = len(commands.getoutput("arp -a").split('\n'))
     lcd.message(str(num_lines).zfill(3))
     cpt = sum([len(files) for r, d, files in os.walk("/mnt/usb/u")])
     mem = int(round(psutil.virtual_memory().percent))
     disk = int(round(psutil.disk_usage('/mnt/usb').percent))
     ldisk = int(round(psutil.disk_usage('/').percent))
     lcd.set_cursor(0,1)
     lcd.message('F'+str(cpt).zfill(3))
     lcd.set_cursor(5,1)
     lcd.message('M'+str(mem).zfill(2))
     lcd.set_cursor(9,1)
     lcd.message('D'+str(disk).zfill(2))
     lcd.set_cursor(13,1)
     lcd.message('L'+str(ldisk).zfill(2))

     for _ in range(3):
      if oldclientnum != num_lines:
   	 lcd.set_backlight(1)
	 lcd.set_color(0.0, 1.0, 0.0)
         sleep(1)
         lcd.set_backlight(0)
         sleep(0.2)
      if oldfilenum != cpt:
	 lcd.set_backlight(1)
         lcd.set_color(0.0, 0.0, 1.0)
         sleep(1)
         lcd.set_backlight(0)
         sleep(0.4)
     sleep(2)
     lcd.set_backlight(0)
     oldclientnum = num_lines
     oldfilenum = cpt


# Get a word from the UI, a character at a time.
# Click select to complete input, or back out to the left to quit.
# Return the entered word, or None if they back out.
def GetWord():
    lcd.clear()
    lcd.blink(1)
    sleep(0.75)
    curword = list("5")
    curposition = 0
    while 1:
        if lcd.is_pressed(LCD.UP):
            if (ord(curword[curposition]) < 127):
                curword[curposition] = chr(ord(curword[curposition])+1)
            else:
                curword[curposition] = chr(32)
        if lcd.is_pressed(LCD.DOWN):
            if (ord(curword[curposition]) > 32):
                curword[curposition] = chr(ord(curword[curposition])-1)
            else:
                curword[curposition] = chr(127)
        if lcd.is_pressed(LCD.RIGHT):
            if curposition < DISPLAY_COLS - 1:
                curword.append('5')
                curposition += 1
                lcd.set_cursor(curposition, 0)
            sleep(0.75)
        if lcd.is_pressed(LCD.LEFT):
            curposition -= 1
            if curposition <  0:
                lcd.blink(0)
                return
            lcd.set_cursor(curposition, 0)
        if lcd.is_pressed(LCD.SELECT):
            # return the word
            sleep(0.75)
            return ''.join(curword)
        lcd.home()
        lcd.message(''.join(curword))
        lcd.set_cursor(curposition, 0)
        sleep(0.25)

    lcd.blink(0)

# An example of how to get a word input from the UI, and then
# do something with it
def EnterWord():
    if DEBUG:
        print('in EnterWord')
    word = GetWord()
    lcd.clear()
    lcd.home()
    if word is not None:
        lcd.message('>'+word+'<')
        sleep(5)

class CommandToRun:
    def __init__(self, myName, theCommand):
        self.text = myName
        self.commandToRun = theCommand
    def Run(self):
        self.clist = split(commands.getoutput(self.commandToRun), '\n')
        if len(self.clist) > 0:
            lcd.clear()
            lcd.message(self.clist[0])
            for i in range(1, len(self.clist)):
                while 1:
                    if lcd.is_pressed(LCD.DOWN):
                        break
                    sleep(0.25)
                lcd.clear()
                lcd.message(self.clist[i-1]+'\n'+self.clist[i])          
                sleep(0.5)
        while 1:
            if lcd.is_pressed(LCD.LEFT):
                break

class Widget:
    def __init__(self, myName, myFunction):
        self.text = myName
        self.function = myFunction
        
class Folder:
    def __init__(self, myName, myParent):
        self.text = myName
        self.items = []
        self.parent = myParent

def HandleSettings(node):
    global lcd
    if node.getAttribute('lcdColor').lower() == 'red':
        LcdRed()
    elif node.getAttribute('lcdColor').lower() == 'green':
        LcdGreen()
    elif node.getAttribute('lcdColor').lower() == 'blue':
        LcdBlue()
    elif node.getAttribute('lcdColor').lower() == 'yellow':
        LcdYellow()
    elif node.getAttribute('lcdColor').lower() == 'teal':
        LcdTeal()
    elif node.getAttribute('lcdColor').lower() == 'violet':
        LcdViolet()
    elif node.getAttribute('lcdColor').lower() == 'white':
        LcdOn()
    if node.getAttribute('lcdBacklight').lower() == 'on':
        LcdOn()
    elif node.getAttribute('lcdBacklight').lower() == 'off':
        LcdOff()

def ProcessNode(currentNode, currentItem):
    children = currentNode.childNodes

    for child in children:
        if isinstance(child, xml.dom.minidom.Element):
            if child.tagName == 'settings':
                HandleSettings(child)
            elif child.tagName == 'folder':
                thisFolder = Folder(child.getAttribute('text'), currentItem)
                currentItem.items.append(thisFolder)
                ProcessNode(child, thisFolder)
            elif child.tagName == 'widget':
                thisWidget = Widget(child.getAttribute('text'), child.getAttribute('function'))
                currentItem.items.append(thisWidget)
            elif child.tagName == 'run':
                thisCommand = CommandToRun(child.getAttribute('text'), child.firstChild.data)
                currentItem.items.append(thisCommand)

class Display:
    def __init__(self, folder):
        self.curFolder = folder
        self.curTopItem = 0
        self.curSelectedItem = 0
	lcd.create_char(1, [8,12,30,31,30,12,8,0])
    def display(self):
        if self.curTopItem > len(self.curFolder.items) - DISPLAY_ROWS:
            self.curTopItem = len(self.curFolder.items) - DISPLAY_ROWS
        if self.curTopItem < 0:
            self.curTopItem = 0
        if DEBUG:
            print('------------------')
        str = ''
        for row in range(self.curTopItem, self.curTopItem+DISPLAY_ROWS):
            if row > self.curTopItem:
                str += '\n'
            if row < len(self.curFolder.items):
                if row == self.curSelectedItem:
                    cmd = '\x01'+self.curFolder.items[row].text
                    if len(cmd) < 16:
                        for row in range(len(cmd), 16):
                            cmd += ' '
                    if DEBUG:
                        print('|'+cmd+'|')
                    str += cmd
                else:
                    cmd = ' '+self.curFolder.items[row].text
                    if len(cmd) < 16:
                        for row in range(len(cmd), 16):
                            cmd += ' '
                    if DEBUG:
                        print('|'+cmd+'|')
                    str += cmd
        if DEBUG:
            print('------------------')
        lcd.home()
        lcd.message(str)

    def update(self, command):
        global currentLcd
        global lcdstart
        lcd.set_backlight(currentLcd)
        lcdstart = datetime.now()
        if DEBUG:
            print('do',command)
        if command == 'u':
            self.up()
        elif command == 'd':
            self.down()
        elif command == 'r':
            self.right()
        elif command == 'l':
            self.left()
        elif command == 's':
            self.select()
    def up(self):
        if self.curSelectedItem == 0:
            return
        elif self.curSelectedItem > self.curTopItem:
            self.curSelectedItem -= 1
        else:
            self.curTopItem -= 1
            self.curSelectedItem -= 1
    def down(self):
        if self.curSelectedItem+1 == len(self.curFolder.items):
            return
        elif self.curSelectedItem < self.curTopItem+DISPLAY_ROWS-1:
            self.curSelectedItem += 1
        else:
            self.curTopItem += 1
            self.curSelectedItem += 1
    def left(self):
        if isinstance(self.curFolder.parent, Folder):
            # find the current in the parent
            itemno = 0
            index = 0
            for item in self.curFolder.parent.items:
                if self.curFolder == item:
                    if DEBUG:
                        print('foundit')
                    index = itemno
                else:
                    itemno += 1
            if index < len(self.curFolder.parent.items):
                self.curFolder = self.curFolder.parent
                self.curTopItem = index
                self.curSelectedItem = index
            else:
                self.curFolder = self.curFolder.parent
                self.curTopItem = 0
                self.curSelectedItem = 0
    def right(self):
        if isinstance(self.curFolder.items[self.curSelectedItem], Folder):
            self.curFolder = self.curFolder.items[self.curSelectedItem]
            self.curTopItem = 0
            self.curSelectedItem = 0
        elif isinstance(self.curFolder.items[self.curSelectedItem], Widget):
            if DEBUG:
                print('eval', self.curFolder.items[self.curSelectedItem].function)
            eval(self.curFolder.items[self.curSelectedItem].function+'()')
        elif isinstance(self.curFolder.items[self.curSelectedItem], CommandToRun):
            self.curFolder.items[self.curSelectedItem].Run()

    def select(self):
        if DEBUG:
            print('check widget')
        if isinstance(self.curFolder.items[self.curSelectedItem], Widget):
            if DEBUG:
                print('eval', self.curFolder.items[self.curSelectedItem].function)
            eval(self.curFolder.items[self.curSelectedItem].function+'()')

# now start things up
uiItems = Folder('root','')

dom = parse(configfile) # parse an XML file by name

top = dom.documentElement

currentLcd = 0
LcdOff()
ProcessNode(top, uiItems)

display = Display(uiItems)
display.display()

if DEBUG:
    print('start while')

lcdstart = datetime.now()
while 1:
    if (lcd.is_pressed(LCD.LEFT)):
       	display.update('l')
	lcdstart = datetime.now()
        display.display()
        sleep(0.25)

    if (lcd.is_pressed(LCD.UP)):
        display.update('u')
	lcdstart = datetime.now()
        display.display()
        sleep(0.25)

    if (lcd.is_pressed(LCD.DOWN)):
        display.update('d')
	lcdstart = datetime.now()
        display.display()
        sleep(0.25)

    if (lcd.is_pressed(LCD.RIGHT)):
        display.update('r')
	lcdstart = datetime.now()
        display.display()
        sleep(0.25)

    if (lcd.is_pressed(LCD.SELECT)):
        display.update('s')
	lcdstart = datetime.now()
        display.display()
        sleep(0.25)

    if AUTO_OFF_LCD:
        lcdtmp = lcdstart + timedelta(seconds=45)
        if (datetime.now() > lcdtmp):
            HatNasLock()
            lcdstart = datetime.now()

