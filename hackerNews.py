#!/usr/bin/python
import urllib , json ,smtplib
import sys ,  ConfigParser, time , sched , os.path

s = sched.scheduler(time.time, time.sleep)	

def gerPeriod():
	try :
		config = ConfigParser.ConfigParser()
		config.readfp(open(r'config'))
		return  int(config.get('update', 'period'))			
	except : 
		writeLog("error reading period")
		sys.exit()

def checkPreConditions() :
	if not os.path.isfile("HackerNewsLog.txt") :
		fo = open("HackerNewsLog.txt","w");
		fo.close()
		
	if not os.path.isfile("lastID.txt") :
		writeLog("lastID.txt file created")
		fo = open("lastID.txt","w");
		fo.close()
		
	if not os.path.isfile("config") :
		writeLog("config file not found")
		sys.exit()	

def writeLog(str):
	fo = open("HackerNewsLog.txt","a")
	fo.write(str+"\t\t"+time.strftime("%H:%M:%S")+"\t"+ time.strftime("%d/%m/%Y")+'\n')		
	fo.close()

def getMailCredentials():
	try :
		config = ConfigParser.ConfigParser()
		config.readfp(open(r'config'))
		return ( config.get('credentials', 'email'), \
			config.get('credentials', 'password') )
	except : 
		writeLog("error accessing configuration file")
		sys.exit()
		
def sendMail():
	fromaddr = 'tharindunishada@gmail.com'
	toaddrs  = 'lnishada@gmail.com'
	msg = 'Top article of the hacker news is changed'
	username , password = getMailCredentials()
	
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.ehlo()
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
	
def getCurrentNewsID():
	url = "https://hacker-news.firebaseio.com/v0/topstories.json"
	response = urllib.urlopen(url);
	jsondata = json.loads(response.read())	 
	return str(jsondata[0])
	
def getPreviousNewsID():
	try :
		fo = open("lastID.txt","r");
		previousTopNewsId= fo.read();
		fo.close();
		return previousTopNewsId
	except :
		writeLog("error accessing lastID.txt file")
		sys.exit()
		
def saveCurrentID(id):
	fo = open("lastID.txt","w")
	fo.write( str(id) )
	fo.close()	
	
def beginExecution():		
	s.enter( gerPeriod(), 1, beginExecution, ())		
	checkPreConditions()
	currentID = getCurrentNewsID()
	
	if not getPreviousNewsID() == currentID :			
		saveCurrentID(currentID)		
		sendMail()
		writeLog("email sent")	

def scheduleExecution():
	s.enter( gerPeriod() , 1, beginExecution, ())	
	s.run()
	
scheduleExecution()
#beginExecution()

