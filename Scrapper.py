import urllib2
import json
import re
import wikipedia
import codecs
import networkx as nx
import matplotlib.pyplot as plt
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.stdout=open("Output.txt","w")


link = wikipedia.page("Python (programming language)")
g = nx.Graph()
graphDict = {  }
total = []

def printDictionary(dict):

	for i in dict:
		print i, dict[i]


def CalcNodeWeight(dict, link):
	
	for item in dict:
		weight = 0
		if dict[0].lower() == link.lower():
			weight += 1

	dict.update({"Weight": weight})


def Scrapper(link):
	#sys.stdout=open("Output.txt","w")
	Categories = link.categories
	
	print link.title

	try:
		for i in range (0, len(Categories)):
			temp = i
			#print Categories[i]
			spaceReplace = Categories[i]
			spaceReplace = str('_'.join(re.findall('\"[^\"]*\"|\S+',spaceReplace)))
	
			subReq = urllib2.Request("https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtype=subcat&cmtitle=Category:" + spaceReplace + "&format=json&cmlimit=500")
			opener = urllib2.build_opener()
			f = opener.open(subReq)
			parsed_json = json.loads(f.read())
	

			PagesReq = urllib2.Request("https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:" + spaceReplace + "&format=json&cmlimit=500")
			PagesOpener = urllib2.build_opener()
			p = PagesOpener.open(PagesReq)
			Pages_Parsed_Json = json.loads(p.read())

			sum = 0
			
			for j in range(0,len(parsed_json['query']['categorymembers'])):
				str1 = parsed_json['query']['categorymembers'][j]['title']
				
				print str1.encode("utf-8")
				print " "
				#total.append(str1)
				graphDict.update({sum : str1})
				sum += 1
				
				for x in range(0, len(Pages_Parsed_Json['query']['categorymembers'])):
				 	str2 =Pages_Parsed_Json['query']['categorymembers'][x][('title')]
				 	
				 	print str2.encode("utf-8")
				 	g.add_edge(j,x)
				 	#total.append(str2)
				 	graphDict.update({sum : str2})
				 	sum +=1




	except IndexError:
		print "Empty subcategory"  

pos = nx.spring_layout(g,scale=10)
print nx.info(g)
nx.draw(g,pos)
#print g.edges()
#plt.show()

nx.write_gml(g,"wiki.gml")
Scrapper(link)
printDictionary(graphDict)
sys.stdout.close()
