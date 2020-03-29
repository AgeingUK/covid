import urllib
from matplotlib import pyplot as plt
import numpy as np
from datetime import date
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

pops={'United Kingdom':66000,'France':65000,'Germany':82000,'Italy':59000,'Spain':46000,
'NLD':17000, 'US':327000,'BEL':11400,'CHN':1380000,'Belgium':11400,
"Japan":127000, "Korea, South":52000}
Jan=31
Feb=29
yet=Jan+10
locks={"Italy":Jan+Feb+5-JHstart, "United Kingdom":Jan+Feb+23-JHstart, "US":yet,"France":Jan+Feb+18-JHstart,"German":yet,"Spain":Jan+Feb+14-JHstart,
"Belgium":Jan+Feb+18-JHstart, "Japan":yet}

def plot_country(country, symbol='ko'):
	global maxy
	key=5
	zero=0
	data= get_country(country)
	gbrx=[]
	gbry=[]
	off=False
	for i, val in enumerate(data):
		if val>=key:
			if off==False:
				zero=i
				print(str(country)+" starts day:"+str(i))
				off=True
			gbrx.append(i-zero)
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
		#gbry.append(1025/pops[country])
	plt.plot(gbrx,gbry,symbol)
	return [zero,gbry]

countries=['US','France',
'Italy',
'Japan',
#'Korea, South',
'Belgium',
'Germany',
'Spain',
'United Kingdom']

sym=['yD-','bD-','gs-','gD-','kD-','k^-','bo-','ro-'] #,'bo','ro']
for i,c in enumerate(countries):
	[zero,deaths]=plot_country(c, symbol=sym[i])
	#print(c)
	if c in ["Italy","Spain","Belgium"]:
		plt.scatter(locks[c]-zero,deaths[locks[c]-zero],s=100,facecolors="none",
		edgecolors='k')
		plt.vlines(locks[c]-zero,0,0.025)	
		#plt.hlines([422,463],0,30)
	if c in ["United Kingdom","France"]:
		plt.scatter(locks[c]-zero,deaths[locks[c]-zero],s=100,facecolors="none",
		edgecolors='k')
		plt.vlines(locks[c]-zero,0,0.022)
		
	
plt.legend(countries,loc='upper left')
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
plt.text(1,0.022, 'Lockdown points circled for \nBelgium,     Spain, Italy,  France\n                                           UK', fontsize=12,
rotation=0, rotation_mode='anchor', color='k')		
		
plt.xlabel('Day since 5th death testing positive')
plt.ylabel('Cumulative fatalities of people testing COVID +ve; per 1000 pop')
plt.title('Data from John Hopkins Date: '+ today)
plt.ylim([0,maxy+0.02])
plt.xlim(0,35)
filename='covidpop'+today+'.png'
plt.savefig(filename,dpi=300)
plt.show()
