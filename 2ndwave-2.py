import urllib
from matplotlib import pyplot as plt
import numpy as np
from datetime import date
#icloud>covidpy
plt.rcParams['axes.facecolor'] = 'white'
maxy=0
today = date.today().strftime("%d-%m-%Y")
JHstart=22
def add(a,b):
	if len(a)!=len(b):
		print ('add error')
		exit()
	return [x + y for x, y in zip(a, b)]
	
def multiadd(lists):
	return [sum(x) for x in zip(*lists)]
	
def grab_data():
	url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
	file = urllib.request.urlopen(url)
	lines=[]
	for line in file:
		decoded_line = line.decode("utf-8")
		lines.append(decoded_line.split(','))
	return lines
	
def get_country(country):
	data=[]
	for line in range(len(lines)):
		if (lines[line][0]=='' and lines[line][1]==country) or (lines[line][0]==country and lines[line][1]==country):
			#print(lines[line])
			for x in range(len(lines[line][4:-1])):
				data.append(int(lines[line][4+x]))
			data.append(int(lines[line][-1].rstrip()))
		
	return data
		
lines=grab_data()

pops={'United Kingdom':66,'France':65,'Germany':82,'Italy':59,'Spain':46,
'Netherlands':17, 'US':327,'BEL':11.400,'CHN':1380,'Belgium':11.400,
"Japan":127.000, "Korea, South":52.000,"Iceland":0.364,"Sweden":10.400,
"Austria":8.822, "Denmark":5.600, "England":56.000, "Poland": 38.000,
"Ireland":4.900,"Brazil":209.000,"Peru":33.000,"Hungary":9.600,"Czechia":10.600,"Slovakia":5.450,"Greece":10.5,"Wales":3.1,"Portugal":10.28,"Luxembourg":0.626,"Norway":5.3}
for key in pops:    
	pops[key] /= 1

Jan=31
Feb=29
yet=Jan+10
locks={"Italy":Jan+Feb+5-JHstart, "United Kingdom":Jan+Feb+23-JHstart, "US":yet,"France":Jan+Feb+18-JHstart,"German":yet,"Spain":Jan+Feb+14-JHstart,
"Belgium":Jan+Feb+18-JHstart, "Japan":yet}
#plt.figure(figsize=(4,4))
def plot_country(country, symbol='ko', fill='full'):
	global maxy
	maxrate=0
	key=5
	zero=0
	data= get_country(country)
	gbrx=[]
	gbry=[]
	off=False
	baseline=0
	for i, val in enumerate(data):
		if val>=key:
			if off==False:
				zero=i+200
				print(str(country)+" starts day:"+str(i))
				off=True
			#to get second wave, change i by 200
			if i==200:
				baseline=val
			val=val-baseline	
				
			gbrx.append(i-zero) #change here
			normalise=True
			if normalise == False:
				gbry.append(val)
			else:
				gbry.append(val/pops[country])
			if max(gbry)>maxy:
				maxy=max(gbry)
			print("cumulative="+str(round(max(gbry)*pops[country])))
	if country=="United Kingdom":
		a=1 #dummy
		#gbrx.append(max(gbrx)+1)
		#gbry.append(max(gbry)+(717)/pops[country])
	plt.plot(gbrx,gbry,symbol, fillstyle=fill)
	return [zero,gbry,maxrate]

all=True
if all==True:
	countries=['Germany','France',
	'Italy',
	'Czechia',
	#'Korea, South',
	'Belgium',
	'Netherlands',
	'Sweden',
	'Spain',
	'Poland',
	'Greece',
	'Portugal',
	'United Kingdom']
else:
	countries=['France',
	'Italy',
	'Belgium',
	'Brazil',
	'Sweden',
	'Spain',
	'United Kingdom']
sym=['yD-','bo-','ws-','mD-','gD-','k^-','c^-','bo-','k+','r--','y+-','ro-'] #,'bo','ro']
fills=['full','none','full','full','full','full','full','full','full','full','full','full']
for i,c in enumerate(countries):
	[zero,deaths,maxrate]=plot_country(c, symbol=sym[i],fill=fills[i])
	#print(c)
	lockdowns=False
	if lockdowns==True:
		if c in ["Italy","Spain","Belgium"]:
			plt.scatter(locks[c]-zero,deaths[locks[c]-zero],s=100,facecolors="none",
			edgecolors='k')
			plt.vlines(locks[c]-zero,0,0.2)	
			#plt.hlines([422,463],0,30)
		if c in ["United Kingdom","France"]:
			plt.scatter(locks[c]-zero,deaths[locks[c]-zero],s=100,facecolors="none",
			edgecolors='k')
			print(locks[c])
			plt.vlines(locks[c]-zero,0,0.15)

if all==False:
	newcountries=[]
	for country in countries:
		if country != 'Sweden':
			newcountries.append(country)
		else:
			newcountries.append("Sweden (No LockD)")
	plt.legend(newcountries,loc='upper left',framealpha=0.5)
else:
	plt.legend(countries,loc='upper left',framealpha=0.5)		
context=False 
if context==True:
	textstr = '\n'.join(['Usual (typical UK)',
	'death rate non-COVID','From UK Gov ONS'])
	plt.text(9,0.2, textstr, fontsize=16,
	rotation=0, rotation_mode='anchor', color='red')
	gbrx=range(len(deaths))
	plt.plot(gbrx,[10*(el+1)/365 for el in gbrx],'k',linewidth=5)
	plt.text(8,0.02, 'Death rates for \npeep testing COVID +ve', fontsize=15,
	rotation=40, rotation_mode='anchor', color='red')		
if lockdowns==True:
	plt.text(0.6,0.20, 'Lockdown points circled for \nBelgium, Spain,Italy, \n                       France/ UK', fontsize=10,
	rotation=0, rotation_mode='anchor', color='k')		
l=0
r=350
#plt.hlines(17260/pops['United Kingdom'],l,r,colors='r', linestyles='dashed')	
plt.hlines(26408/pops['England'],l,r,'r',linewidth=2)		
#plt.hlines(18768/pops['United Kingdom'],l,r,colors='r', linestyles='dashed')		
'''
Table 7
https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/839350/Surveillance_of_influenza_and_other_respiratory_viruses_in_the_UK_2018_to_2019-FINAL.pdf

oops normalised forUK NOT England! NOW CORRECTED!!
'''
flu='England flu associated deaths (ONS data) \nWinter of 2017/2018, see links'	
plt.text(50,26408/pops['England']+10,flu,color='r',fontweight='bold')														
plt.xlabel('Day since 5th death testing c19 positive -200 (to get 2nd wave)')
plt.ylabel('"2nd" WAVE COVID +ve fatalities per million pop')
plt.title('"2nd" WAVE Data from John Hopkins: '+ today)
plt.ylim([0,1600])
plt.xlim(0,150)
filename='covid2nd'+today+'.png'
plt.savefig(filename,dpi=300)
plt.show()
