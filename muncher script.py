import time
import requests
import sys
import csv
fileName = 'muncher.txt'
URL="https://tgrcode.com/mm2/level_info/"
URLPlayed="https://tgrcode.com/mm2/level_played/"
checkCleared= True
PARAMS={}
line2=""
file1=open(fileName, 'r', errors="replace")


class Jamper:
   def __init__(self, name):
      self.name=name
   totalPts=0
   totalClears=0

   
jamperList=[]

def jamperIndex(name):
   for i in range(len(jamperList)):
      if jamperList[i].name==name:
         return i;
   user=Jamper(name)
   jamperList.append(user)
   return len(jamperList)-1

def getclearers(input):
   splitted=input.split()
   line=splitted[0]
   points=getPoints(splitted[1])
   r=requests.get(url=URLPlayed+line,params=PARAMS)
   data=r.json()
   for i in range(len(data['players'])):
      for j in range(len(data['cleared'])):
         if data['players'][i]['pid']==data['cleared'][j]:
            index=jamperIndex(data['players'][i]['name'])
            jamperList[index].totalClears+=1
            jamperList[index].totalPts+=points
               
#returns points granted at a specific difficulty
def getPoints(difficulty):
   if float(difficulty)<1.4:
      return float(difficulty)
   pts=round(float(difficulty)**1.3,1)
   return pts
   
#main loop   
while True:
   line = file1.readline().strip()
   if line=="" or line2==line:
      break
   try:
      getclearers(line)
   except:
         try:
            getclearers(line)
            continue
         except:
            try:
               getclearers(line)
               continue
            except:
               print("three failures wtf for clearers on " + line)
               continue

   line2=line
   
with open('muncheroutput.csv','w', encoding ='UTF8',newline='') as f:
   writer=csv.writer(f)
   writer.writerow(['name','points','clears'])
   for x in jamperList:
      #printMe=x.name+ " has " + str(x.totalClears) + " clears and " +  str(x.totalPts) + " points\n"
      #encoded=printMe.encode('utf8')
      #sys.stdout.buffer.write (encoded)
      writer.writerow([x.name,x.totalPts,x.totalClears])