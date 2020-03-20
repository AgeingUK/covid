import csv
from matplotlib import pyplot as plt
header=True

data=[]
with open('20200319-deaths.csv') as in_file:
	for row in csv.reader(in_file):
		if header == True:
			head=', '.join(row)
			header=False
		else:
			data.append(row)

print(head)
one='ITA'
two='ESP'
#'DEU'
three='FRA'
#'FRA'
four='GBR'
sym1='bo'
sym2='gD'
sym3='ro'

pops={'GBR':66000,'FRA':65000,'DEU':82000,'ITA':59000,'ESP':46000,
'NLD':17000}
pops['GBR']


key=5
code=[]
for row in data:
	if row[1]==one:
		code.append(row)
gbrx=[]
gbry=[]
off=False
for i, row in enumerate(code):
	if int(row[3])>=key:
		if off==False:
			zero=int(row[2])
			off=True
		gbrx.append(int(row[2])-zero)
		gbry.append(int(row[3])/pops[one])
	
plt.plot(gbrx,gbry,'bo')

code=[]
for row in data:
	if row[1]==two:
		code.append(row)
gbrx=[]
gbry=[]
off=False
for i, row in enumerate(code):
	if int(row[3])>=key:
		if off==False:
			zero=int(row[2])
			off=True
		gbrx.append(int(row[2])-zero)
		gbry.append(int(row[3])/pops[two])
	
plt.plot(gbrx,gbry,'gD')

code=[]
for row in data:
	if row[1]==three:
		code.append(row)
gbrx=[]
gbry=[]
off=False
for i, row in enumerate(code):
	if int(row[3])>=key:
		if off==False:
			zero=int(row[2])
			off=True
		gbrx.append(int(row[2])-zero)
		gbry.append(int(row[3])/pops[three])
			
plt.plot(gbrx,gbry,'kD')
				
code=[]
for row in data:
	if row[1]==four:
		code.append(row)
gbrx=[]
gbry=[]
off=False
for i, row in enumerate(code):
	if int(row[3])>=key:
		if off==False:
			zero=int(row[2])
			off=True
		gbrx.append(int(row[2])-zero)
		gbry.append(int(row[3])/pops[four])

#temp!!
#gbrx.append(max(gbrx)+1)
#gbry.append(71)

gbrx.append(max(gbrx)+1)
gbry.append(144/pops['GBR'])
print (gbrx)								
plt.plot(gbrx,gbry,'ro')
plt.plot(gbrx,[10*(el+1)/365 for el in gbrx],'r-o')
plt.text(5,0.31, 'Usual (typical UK) death rate non-COVID', fontsize=16,
rotation=0, rotation_mode='anchor', color='red')
plt.text(5,0.031, 'Death rates COVID +ve', fontsize=16,
rotation=0, rotation_mode='anchor', color='red')
plt.legend([one,two,three,four],loc='upper left')				
plt.xlabel('Day since 5th death testing positive')
plt.ylabel('Cumulative +ve test for people that died per 1000 pop')
plt.title('Data from https://ourworldindata.org/coronavirus')	
plt.show()

