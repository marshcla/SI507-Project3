from bs4 import BeautifulSoup
import unittest
import requests
import csv

#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way,
# and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones,
# think pretty seriously about all the different parts and their requirements,
# and what you need to understand.
# Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########

# Write your code for Part 0 here.
try:
    photo_data = open("photo_data_cache.html", "r")
except:
    photo_data = requests.get("http://newmantaylor.com/gallery.html").text
    f = open("photo_data_cache.html", "w")
    f.write(photo_data)
    f.close()

photo_soup = BeautifulSoup(photo_data, "html.parser")
photo_tags = photo_soup.find_all("img")
for pic in photo_tags:
    print(pic.get("alt", "No alternative text provided!"))

######### PART 1 #########

# Get the main page data...

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except,
# but if you prefer to build up the code to do this scraping and caching yourself, that is OK.

try:
    np_cache = open("nps_gov_data.html", "r").text
except:
    np_cache = requests.get("https://www.nps.gov/index.htm").text
    f = open("nps_gov_data.html", "w")
    f.write(np_cache)
    f.close()

# Get individual states' data...

# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.

# TRY:
# To open and read all 3 of the files

try:
    arkansas_data = open("arkansas_data.html", "r").read()
    california_data = open("california_data.html", "r").read()
    michigan_data = open("michigan_data.html", "r").read()
except:
    np_soup = BeautifulSoup(np_cache, "html.parser")
    dropdown = np_soup.find("div", {"class":"SearchBar-keywordSearch input-group input-group-lg"})
    state_links = [state["href"] for state in dropdown.find_all("a")]
    three_states = []
    for state in state_links:
        if "ar" in state:
            three_states.append(state)
        elif "ca" in state:
            three_states.append(state)
        elif "mi" in state:
            three_states.append(state)
        else:
            pass
    state_urls = []
    for state in three_states:
        state_urls.append("https://www.nps.gov" + state)
    ar_url = state_urls[0]
    ca_url = state_urls[1]
    mi_url = state_urls[2]
    arkansas_data = requests.get(ar_url).text
    f = open("arkansas_data.html", "w")
    f.write(arkansas_data)
    f.close()
    california_data = requests.get(ca_url).text
    g = open("california_data.html", "w")
    g.write(california_data)
    g.close()
    michigan_data = requests.get(mi_url).text
    i = open("michigan_data.html", "w")
    i.write(michigan_data)
    i.close()

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown

# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method

# Use a list comprehension or accumulation to get all of the
# 'href' attributes of the 'a' tag objects in each li, instead of the full li objects

# Filter the list of relative URLs you just got to
# include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements

# Create 3 URLs to access data from by appending those
# 3 href values to the main part of the NPS url. Save each URL in a variable.

# To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g.
# Maine parks URL is "http://www.nps.gov/state/me/index.htm",
# Michigan's is "http://www.nps.gov/state/mi/index.htm" --
# so if you compare that to the values in those href attributes
# you just got... how can you build the full URLs?

# Finally, get the HTML data from each of these URLs,
# and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause!
# Otherwise, all this code will run every time you run the program!)

# And then, write each set of data to a file so this won't have to run again.

######### PART 2 #########

## Before truly embarking on Part 2, we recommend you do a few things:

# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects.
# What data do you have about each state? How is it organized in HTML?

# HINT: remember the method .prettify() on a BeautifulSoup object --
# might be useful for your investigation! So, of course, might be .find or .find_all, etc...

# HINT: Remember that the data you saved is data that
# includes ALL of the parks/sites/etc in a certain state,
# but you want the class to represent just ONE park/site/monument/lakeshore.

# We have provided, in sample_html_of_park.html
# an HTML file that represents the HTML about 1 park.
# However, your code should rely upon HTML data about
# Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your
# class definition, you may want to open this file and
# create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have
# to be careful about listed in the instructions --
# e.g. if no type of park/site/monument is listed in input,
# one of your instance variables should have a None value...

## Define your class NationalSite here:

class NationalSite(object):

    def __init__(self, park):
        self.location = park.find("h4").text
        self.name = park.find("h3").text
        try:
            self.type = park.find("h2").text
        except:
            self.type = None
        try:
            self.description = park.find("p").text
        except:
            self.description = ""
        self.list_of_urls = [url["href"] for url in park.find_all("a")]
        self.url = self.list_of_urls[2]

    def __str__(self):
        return "{} | {}".format(self.name, self.location)

    def get_mailing_address(self):
        file_name = self.name + ".html"
        try:
            html = open(file_name, "r").read()
        except:
            html = requests.get(self.url).text
            f = open(file_name, "w")
            f.write(html)
            f.close()
        get_address_page = BeautifulSoup(html, "html.parser")
        try:
            street_address = get_address_page.find("span", {"class" : "street-address"}).text.strip()
        except:
            street_address = get_address_page.find("p", {"class" : "adr"}).text.strip()
        try:
            region = get_address_page.find("span", {"class" : "region"}).text.strip()
        except:
            region = get_address_page.find("span", {"itemprop" : "addressLocality"}).text.strip()
        try:
            zip_code = get_address_page.find("span", {"class" : "postal-code"}).text.strip()
        except:
            zip_code = get_address_page.find("span", {"itemprop" : "postalCode"}).text.strip()
        return street_address + ", " + region + " " + zip_code

    def __contains__(self, word):
        if word in self.name:
            return True
        else:
            return False

# Recommendation: to test the class,
# at various points, uncomment the following code
# and invoke some of the methods / check out the instance
# variables of the test instance saved in the variable sample_inst:

#f = open("sample_html_of_park.html",'r')
#soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
#sample_inst = NationalSite(soup_park_inst)
#f.close()

#print(sample_inst.get_mailing_address())
#print(sample_inst.__contains__("Isle"))

######### PART 3 #########

# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.

california_natl_sites = []
ca_soup = BeautifulSoup(california_data, "html.parser")
parklistca = ca_soup.find_all("li", {"class": "clearfix"})
for park in parklistca:
    try:
        park_c = NationalSite(park)
        california_natl_sites.append(park_c)
    except:
        pass

arkansas_natl_sites = []
ak_soup = BeautifulSoup(arkansas_data, "html.parser")
parklistak = ak_soup.find_all("li", {"class": "clearfix"})
for park in parklistak:
    try:
        park_a = NationalSite(park)
        arkansas_natl_sites.append(park_a)
    except:
        pass

michigan_natl_sites = []
mi_soup = BeautifulSoup(michigan_data, "html.parser")
parklistmi = mi_soup.find_all("li", {"class": "clearfix"})
for park in parklistmi:
    try:
        park_m = NationalSite(park)
        michigan_natl_sites.append(park_m)
    except:
        pass

#print(len(california_natl_sites))
##Code to help you test these out:
#for p in california_natl_sites:
#	print(p)
#for a in arkansas_natl_sites:
# 	print(a)
# for m in michigan_natl_sites:
# 	print(m)

######### PART 4 #########

## Remember the hints /
# things you learned from Project 2 about writing CSV files from lists of objects!

## Note that running this step for ALL your
# data make take a minute or few to run --
# so it's a good idea to test any methods/functions
# you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that
# may occur, you might run into some problems and have to
# debug for where you need to put in some None value / error handling!

with open('arkansas.csv', 'w') as csvfile:
    fieldnames = ['Name', 'Location', 'Type', 'Address', 'Description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for a in arkansas_natl_sites:
        if a.type == "":
            writer.writerow({'Name': a.name, 'Location': a.location,
                         'Type': 'None', 'Address': a.get_mailing_address(),
                         'Description': a.description})
        else:
            writer.writerow({'Name': a.name, 'Location': a.location,
                         'Type': a.type, 'Address': a.get_mailing_address(),
                         'Description': a.description})

with open('california.csv', 'w') as csvfile:
    fieldnames = ['Name', 'Location', 'Type', 'Address', 'Description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for c in california_natl_sites:
        if c.type == "":
            writer.writerow({'Name': c.name, 'Location': c.location,
                         'Type': 'None', 'Address': c.get_mailing_address(),
                         'Description': c.description})
        else:
            writer.writerow({'Name': c.name, 'Location': c.location,
                         'Type': c.type, 'Address': c.get_mailing_address(),
                         'Description': c.description})

with open('michigan.csv', 'w') as csvfile:
    fieldnames = ['Name', 'Location', 'Type', 'Address', 'Description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for m in michigan_natl_sites:
        if m.type == "":
            writer.writerow({'Name': m.name, 'Location': m.location,
                         'Type': 'None', 'Address': m.get_mailing_address(),
                         'Description': m.description})
        else:
            writer.writerow({'Name': m.name, 'Location': m.location,
                          'Type': m.type, 'Address': m.get_mailing_address(),
                          'Description': m.description})
