import requests
from bs4 import BeautifulSoup
import pandas
# To load other pages, use request for other pages' url
# find pattern of url so can put in for loop
base_url="http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
# in html, indicates the last page
page_nr=soup.find_all("a",{"class":"Page PagerCurrentPage"})[-1] # gets last element in list
for page in range(0,int(page_nr.text)*10,10): # (start=0, iterate step =10, end=20)
    # print(base_url+str(page)+".html")
    r=requests.get(base_url+str(page)+".html")
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"propertyRow"})
    # create dataframe from lists of dictionaries (8 pair in dictionaries)
    l=[]
    for item in all:
        d={}
        d["Price"]=item.find("h4",{"class":"propPrice"}).text.replace("\n","").replace(" ","") # gets the price
        address=item.find_all("span",{"class":"propAddressCollapse"}) # grabs address, use find_all because have two elements
        d["Address"]=address[0].text
        try:
            d["Locality"]=address[1].text
        except:
            d["Locality"]=None
        try:
            d["Beds"]=item.find("span",{"class": "infoBed"}).find("b").text
        except:
           d["Beds"]= None
        try:
            d["Area"]=item.find("span",{"class": "infoSqFt"}).find("b").text #area
        except:
            d["Area"]=None
        try:
            d["Full Baths"]=item.find("span",{"class": "infoValueFullBath"}).find("b").text
        except:
           d["Full Baths"]=None
        try:
            d["Half Baths"]=item.find("span",{"class": "infoValuHalfBath"}).find("b").text
        except:
            d["Half Baths"]=None
        #get lot size, but it is in multiple divisions
        for column_group in item.find_all("div",{"class":"columnGroup"}):
            for feature_group,feature_name in zip(column_group.find_all("span",{"class":"featureGroup"}),column_group.find_all("span",{"class":"featureName"})):
                if "Lot Size" in feature_group.text:
                    d["Lot Size"]=feature_name.text
        l.append(d)
        df =pandas.DataFrame(l)
        df.to_csv("Output2.csv")
