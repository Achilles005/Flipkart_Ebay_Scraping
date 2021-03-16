#Web Scrapping Task:- Without Using BeautifulSoup, Selenium or Srcapy
#This Scripts requires user to input the product name and Choose the site.
#Currently Supports only Flipkart and Ebay.
#The output of this file is a json file with the name flipkart.json or ebay.json depending upon the site choosed by the user.
#Have used sleep function and which takes a random number from 15 to 40 and for that many seconds pauses the operations to give a human touch.
#@Author:- Aditya Shukla

#importing required Libraries
from datetime import datetime as dt
from time import sleep as sleep
from random import randint
from urllib.request import urlopen
import re
import json

#Class function to process Flipkart site request.
class flipkart:
    def __init__(self,product,url='https://www.flipkart.com/search?q='):
        self.product=product
        self.url=url
    
    def connect(self,pageNum):
        final_url=self.url+self.product+'&page='+str(pageNum)
        try:
            response=urlopen(final_url).read().decode('utf-8')
        except:
            print('Connection Refused')
        return response
    
    def extract(self):
        product=[]
        links=[]
        response=self.connect(1)
        content=re.findall('<div class="_1YokD2 _3Mn1Gg" style=.*?>.*?<div class="_1AtVbE col-12-12" style=.*?>',response)
        pages=re.findall('<span>Page .*?</span>',response)
        page_clean=re.compile('<span>|</span>|,')
        for i in pages:
            temp=re.sub(page_clean,'',i)
            last=int(temp.split(" ")[-1])
        for i in range(1,last):
            sleep(randint(15,30))
            response=self.connect(i)
            content=re.findall('<div class="_1YokD2 _3Mn1Gg" style=.*?>.*?<div class="_1AtVbE col-12-12" style=.*?>',response)
            print('Page Number '+str(i)+' Finished')
            if len(content)>0:
                href=re.findall('target="_blank" rel="noopener noreferrer" href="/.*?">',content[0])
                clean=re.compile('target="_blank" rel="noopener noreferrer" href=')
                clean2=re.compile('>|"')
                for h in href:
                    temp=re.sub(clean, '', h)
                    temp=re.sub(clean2,'',temp)
                    prod_url='https://www.flipkart.com'+temp
                    links.append(prod_url)
            else:
                print('Complete')
                break
        print('Scarping Complete')
        link=list(set(links))
        clean_prod=re.compile('com/|/')
        for i in link:
            prod=re.findall('com/.*?/',i)
            prod=re.sub(clean_prod,'',prod[0])
            product.append(prod)
        return product,link
    
    def get_urls(self):
        product,link=self.extract()
        result = {product[i]: link[i] for i in range(len(product))} 
        with open("flipkart.json", "w") as outfile:  
            json.dump(result, outfile)


#Class Function for ebay site request.
class ebay:
    def __init__(self,product,url='https://www.ebay.com/sch/i.html?_nkw='):
        self.product=product
        self.url=url

    def connect(self,pageNum):
        final_url=self.url+self.product+'&_pgn='+str(pageNum)
        try:
            response=urlopen(final_url).read().decode('utf-8')
        except:
            print('Connection Refused')
        return response
    
    def extract(self):
        product=[]
        links=[]
        last=20000
        for i in range(1,last):
            sleep(randint(15,30))
            response=self.connect(1)
            content=re.findall(r'<li class="s-item     ".*?>.*?</li>',response)
            print('Page Number '+str(i)+' Finished')
            if len(content)>0:
                clean_href=re.compile('href=|class|>|<div')
                clean_prod=re.compile('itm/|/')
                for i in content:
                    link=re.findall('href=https://.*?class',i)[0]
                    link=re.sub(clean_href,'',link)
                    prod=re.findall('itm/.*?/',link)
                    prod=re.sub(clean_prod,'',prod[0])
                    product.append(prod)
                    links.append(link)
            else:
                print('Complete')
                break
        print('Scarping Complete')
        
        return product,links
    
    def get_urls(self):
        product,link=self.extract()
        result = {product[i]: link[i] for i in range(len(product))} 
        with open("ebay.json", "w") as outfile:  
            json.dump(result, outfile)
			

if __name__ == "__main__":
	product=input('Enter Product Name:- ')
	temp=product.split(" ")
	product="+".join(temp)
	site=int(input("Choose Site\nPress 1 for Flipkart\nPress 2 for Ebay\n"))
	if site not in [1,2]:
		print('Invalid Response')
	else:
		if site==1:
			flip=flipkart(product)
			flip.get_urls()
		elif site==2:
			eb=ebay(product)
			eb.get_urls()