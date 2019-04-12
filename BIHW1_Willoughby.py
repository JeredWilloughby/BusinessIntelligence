#Homework Assignment #1 - B.I. ISQS 6339
#Jered Willoughby

#Import Libraries
import csv
import requests as r
from bs4 import BeautifulSoup

#Assign URL
url1 = 'http://drd.ba.ttu.edu/isqs6339/imbadproducts/'
#Get URL via request.get
res = r.get(url1)
#Make the soup
soup1 = BeautifulSoup(res.text, 'lxml')
#Establish filepaths
filepath1 = 'desktop\ProductReviews1.csv'
filepath2 = 'desktop\ProductReviews2.csv'

#Check for good link and get headers
print(res.status_code)
print (res.headers)

#Find all anchors on the page
search_results = soup1.find('div', attrs={'id' : 'searchresults'})
product_results = search_results.find_all('a')

#Set the productID, title, price, and description according to their attribute. Run to check correcting parsing.
for ref in product_results:
    url2 = url1 + ref.get('href')
    productId = ref.find('span', attrs={'class' : 'productid'}).text
    product_t = ref.find('span', attrs={'class' : 'producttitle'}).text
    product_p = ref.find('span', attrs={'class' : 'productprice'}).text
    product_d = ref.find('span', attrs={'class' : 'productdesc'}).text
    
    #Differentiate hyperlinks.
    res2 = r.get(url2)
    soup2 = BeautifulSoup(res2.text, 'lxml')
    
    #Separate reviews on each page.
    user_review = soup2.find('div', attrs={'id' : 'userreviews'})
    review_results = user_review.find_all('div')
    
    #Call associated data to verify scrape code works.
    for rev in review_results:
        print('\n*****Product*****\n')
        print ('Product ID: ' + productId)
        print ('Product Title: ' + product_t)
        print ('Product Price: ' + product_p)
        print('Product Description: ' + product_d)
        print ('\n*****Review*****\n')
        author = rev.find('span', attrs={'class' : 'rauthor'}).text
        print('Author: ' + author)
        stars = rev.find('span', attrs={'class' : 'rstars'}).text
        print('Stars: ' + stars)
        review_of_product = rev.find('span' , attrs={'class' : 'rtext'}).text
        print('Review: ' + review_of_product)
        review_length = len(review_of_product)
        print('Length of Review: ', review_length)
        print('----------------------------------')
        
      
#Filepath1 to CSV - to accomplish this, a loop needs to be set up scrape the subpages with specified attributes.
with open(filepath1, 'w+') as dataout:
    datawriter = csv.writer(dataout, delimiter= ',', quotechar= '"', quoting = csv.QUOTE_NONNUMERIC)
    headers = ['ProductId', 'ProductTitle', 'ProductPrice', 'Author', 'Stars', 'Length of Review']
    datawriter.writerow(headers)
#Set loop for the product classes        
    for ref in product_results:
        url2 = url1 + ref.get('href')
        productId = ref.find('span', attrs={'class' : 'productid'}).text
        product_t = ref.find('span', attrs={'class' : 'producttitle'}).text
        product_p = ref.find('span', attrs={'class' : 'productprice'}).text
        product_d = ref.find('span', attrs={'class' : 'productdesc'}).text
        search_results = soup1.find('div', attrs={'id' : 'searchresults'})
        product_results = search_results.find_all('a')
        res2 = r.get(url2)
        soup2 = BeautifulSoup(res2.text, 'lxml')
        user_review = soup2.find('div', attrs={'id' : 'userreviews'})
        review_results = user_review.find_all('div')
#Set loop for the review classes         
        for rev in review_results:    
            author = rev.find('span', attrs={'class' : 'rauthor'}).text
            stars = rev.find('span', attrs={'class' : 'rstars'}).text
            review_of_product = rev.find('span' , attrs={'class' : 'rtext'}).text
            datawriter.writerow([productId, product_t, product_p, author, stars, len(review_of_product)])
                
#Filepath2 to CSV - to accomplish this, a loop needs to be set up scrape the subpages with specified attributes.
with open(filepath2, 'w+') as dataout2:
    datawriter = csv.writer(dataout2, delimiter= ',', quotechar= '"', quoting = csv.QUOTE_NONNUMERIC)
    headers = ['Product Id', 'Author', 'Stars', 'Review Text']
    datawriter.writerow(headers)
#Set loop for the product classes         
    for ref in product_results:
        url2 = url1 + ref.get('href')
        productId = ref.find('span', attrs={'class' : 'productid'}).text
        product_t = ref.find('span', attrs={'class' : 'producttitle'}).text
        product_p = ref.find('span', attrs={'class' : 'productprice'}).text
        product_d = ref.find('span', attrs={'class' : 'productdesc'}).text
        res2 = r.get(url2)
        soup2 = BeautifulSoup(res2.text, 'lxml')
        user_review = soup2.find('div', attrs={'id' : 'userreviews'})
        review_results = user_review.find_all('div')
#Set loop for the review classes       
        for rev in review_results:    
            author = rev.find('span', attrs={'class' : 'rauthor'}).text
            stars = rev.find('span', attrs={'class' : 'rstars'}).text
            review_of_product = rev.find('span' , attrs={'class' : 'rtext'}).text
            datawriter.writerow([productId, author, stars, review_of_product])