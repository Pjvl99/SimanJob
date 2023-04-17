import scrapy
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import bs4
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import os

localPath = '/home/pablo/scrapy/CotizadorTiendas/'
class StoreQuote(scrapy.Spider):
    name = 'siman'
    start_urls = ["https://gt.siman.com"]

    def parse(self, response):              
        chrome_options = Options()
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument("--disable-notifications")
        driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
        # action = webdriver.ActionChains(driver)
        driver.maximize_window()
        driver.get(response.url) 
        time.sleep(10)
        popupPosition = driver.find_elements(By.XPATH, '/html/body/div')
        for popup in popupPosition:
            try:
                popup.find_element(By.XPATH, './div/div/div/div/div/div/button').click()
                break
            except:
                pass
        time.sleep(2)
        driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[2]/div/div[1]/div/div/div/div/div[1]/div/div/div/div/div[2]/div/div/div').click() #Clickear menu de categorias
        time.sleep(5)
        if len(driver.find_elements(By.XPATH, '/html/body/div[8]/div/div[2]/nav/ul')) != 0:
            categoryList = driver.find_elements(By.XPATH, '/html/body/div[8]/div/div[2]/nav/ul')
        elif len(driver.find_elements(By.XPATH, '/html/body/div[9]/div/div[2]/nav/ul')) != 0:
            categoryList = driver.find_elements(By.XPATH, '/html/body/div[9]/div/div[2]/nav/ul')
        elif len(driver.find_elements(By.XPATH, '/html/body/div[7]/div/div[2]/nav/ul')) != 0:
            categoryList = driver.find_elements(By.XPATH, '/html/body/div[7]/div/div[2]/nav/ul')
        else:
            categoryList = driver.find_elements(By.XPATH, '/html/body/div[6]/div/div[2]/nav/ul')
        for categoryListButton in categoryList:
            htmlCategoryList = categoryListButton.find_elements(By.XPATH, './li') 
            for categoryA in htmlCategoryList:
                categoryNameHtml = categoryA.find_elements(By.XPATH, './div/a') 
                if len(test) != 0:
                    for categoryNameAttribute in categoryNameHtml:
                        categoryName = categoryNameAttribute.find_elementsget_attribute('title')
                        try:
                            os.mkdir(f'{localPath}{categoryName}')
                        except:
                            pass
                else:
                    test = categoryA.find_elements(By.XPATH, './div/span/div')
                    for categoryNameAttribute in categoryNameHtml:
                        categoryName = categoryNameAttribute.text
                        try:
                            os.mkdir(f'{localPath}{categoryName}')
                        except:
                            pass
                htmlSubCategoryList = categoryA.find_elements(By.XPATH, './div[2]/div/section/div[2]/div/div') 
                for htmlSubCategoryListDivDiv in htmlSubCategoryList:
                    titleInside = htmlSubCategoryListDivDiv.find_elements(By.XPATH, './div/div') 
                    for titleInsideUlLi in titleInside:
                        if(len(titleInsideUlLi.find_elements(By.XPATH, './nav/ul/li')) == 1):
                            title = titleInsideUlLi.find_elements(By.XPATH, './nav/ul/li/div/a')
                            if len(title) != 0:
                                for titleDiv in title:
                                    subCategoryName = titleDiv.find_element(By.XPATH, './div').find_elementsget_attribute("innerHTML")
                                    try:
                                        os.mkdir(f'{localPath}{categoryName}/{subCategoryName}')
                                    except:
                                        pass
                            elif len(titleInsideUlLi.find_elements(By.XPATH, './nav/ul/li/div/span')) != 0:
                                title = titleInsideUlLi.find_elements(By.XPATH, './nav/ul/li/div/span')
                                for titleDiv in title:
                                    subCategoryName = titleDiv.find_element(By.XPATH, './div').find_elementsget_attribute("innerHTML")
                                    try:
                                        os.mkdir(f'{localPath}{categoryName}/{subCategoryName}')
                                    except:
                                        pass
                            
                        elif(len(titleInsideUlLi.find_elements(By.XPATH, './nav/ul/li')) == 0):
                            title = titleInsideUlLi.find_elements(By.XPATH, './div/div/p') 
                            for titleA in title:
                                subCategoryName = titleA.find_element(By.XPATH, './a').find_elementsget_attribute("innerHTML")
                                try:
                                    os.mkdir(f'{localPath}{categoryName}/{subCategoryName}')
                                except:
                                    pass
                        elif(len(titleInsideUlLi.find_elements(By.XPATH, './nav/ul/li')) > 1):
                            elements = titleInsideUlLi.find_elements(By.XPATH, './nav/ul/li')
                            for childsDivA in elements:
                                subCategoryChild = childsDivA.find_elements(By.XPATH, './div/a')
                                meta = {
                                    'subCategoryName': subCategoryName,
                                    'categoryName': categoryName
                                }
                                if len(subCategoryChild) > 0:
                                    for subCategoryHref in subCategoryChild:
                                        if len(subCategoryHref.find_elementsget_attribute('href')) > 0:
                                            meta['subCategoryNameChild'] = subCategoryHref.find_elementsget_attribute('title')
                                            if len(meta['subCategoryNameChild']) == 0:
                                                meta['subCategoryNameChild'] = 'default'
                                            yield response.follow(subCategoryHref.find_elementsget_attribute('href'), callback=self.getSubCategoryData, meta=meta)

    def getSubCategoryData(self, response):
        try:
            print(f'Currently in: {localPath}{response.meta["categoryName"]}/{response.meta["subCategoryName"]}/{response.meta["subCategoryNameChild"]}.csv')
            chrome_options = Options()
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument("--disable-notifications")
            driver = webdriver.Chrome(executable_path='chromedriver', options=chrome_options)
            driver.maximize_window()
            driver.get(response.url)
            totalNumProducts = 1
            priceCounter = 0
            page = 2
            productList = []
            try:
                while(totalNumProducts != 0):
                    time.sleep(10)
                    isNumAssigned = False
                    appendProducts = False
                    productLink = ''
                    price1 = ''
                    price2 = ''
                    productBrand = ''
                    productImage = ''
                    productImage = ''
                    productName = ''
                    discountTag = ''
                    productNum = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div/div[5]/div/div/section/div[2]/div/div[5]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/span')
                    if len(productNum) > 0:
                        for total in productNum:
                            isNumAssigned = True
                            totalNumProducts = total.find_elementsget_attribute('innerHTML').split(' <')[0]
                    else:
                        productNum = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[1]/div/div/section/div[2]/div/div[5]/div/div[2]/div/div[1]/div/div/div[1]/div/div/div/span')
                        for total in productNum:
                            isNumAssigned = True
                            totalNumProducts = total.find_elementsget_attribute('innerHTML').split(' <')[0]
                    if(isNumAssigned):
                        totalNumProducts = int(totalNumProducts)
                    else:
                        break
                    if totalNumProducts > 0:
                        popupPosition = driver.find_elements(By.XPATH, '/html/body/div')
                        for popup in popupPosition:
                            try:
                                popup.find_element(By.XPATH, './div/div/div/div/div/div/button').click()
                                break
                            except:
                                pass
                        time.sleep(2)
                        productData = driver.find_elements(By.XPATH,'/html/body/div[2]/div/div[1]/div/div')
                        counter = 0
                        for productDataFirstSection in productData:
                            productDataList = productDataFirstSection.find_elements(By.XPATH,'./div/div/section/div[2]/div/div')
                            for productDataListSection2 in productDataList:
                                productList = productDataListSection2.find_elements(By.XPATH, './div/div[2]/div/div')
                                for productListDiv in productList:
                                    productListDiv2 = productListDiv.find_elements(By.XPATH, './div/div/div/div/div') 
                                    for productLocalization in productListDiv2:
                                        if(appendProducts):
                                            productName = productName.replace(",","")
                                            productList.append({'Name' : productName, 'Brand' : productBrand, 
                                                    'Image': productImage, 'Price 1' : price1, 'Price 2': price2, 
                                                    'Discount (%)' : discountTag, 'Link' : productLink})
                                            discountTag = ''
                                        hrefProduct = productLocalization.find_elements(By.XPATH, './section/a/article')
                                        aProduct = productLocalization.find_elements(By.XPATH, './section/a')
                                        if len(aProduct) > 0:
                                            for aProductName in aProduct:
                                                appendProducts = True
                                                productLink = aProductName.find_elementsget_attribute('href')
                                        else:
                                            hrefs = productLocalization.find_elements(By.XPATH, './section/div/div/div/div')
                                            for href in hrefs:
                                                links = href.find_elements(By.XPATH, './section/a')
                                                for link in links:
                                                    appendProducts = True
                                                    productLink = link.find_elementsget_attribute('href')
                                        for discount in hrefProduct:
                                            discountList = discount.find_elements(By.XPATH, './div[1]/div/div/div/div[2]/span/span') #OBTENER TAG DE DESCUENTO
                                            if len(discountList) > 0:
                                                for discountName in discountList:
                                                    discountTag = discountName.find_elementsget_attribute('innerHTML')
                                            else:
                                                discountList = discount.find_elements(By.XPATH, './div/div/div[1]/div/div/div/div/div/div/div[2]/span/span') #OBTENER TAG DE DESCUENTO PAGINA DE UN PRODUCTO
                                                for discountName in discountList:
                                                    discountTag = discountName.find_elementsget_attribute('innerHTML')
                                            discountList = discount.find_elements(By.XPATH, './div[5]/div/div[1]/div/div/div/span') #OBTENER MARCA DE PRODUCTO
                                            if len(discountList) > 0:
                                                for discountName in discountList:
                                                    productBrand = discountName.find_elementsget_attribute('innerHTML')
                                            else:
                                                discountList = discount.find_elements(By.XPATH, './div/div/div[2]/div/div[1]/div/div/div/div/div/div/span') #OBTENER MARCA DE PRODUCTO PAGINA DE UN PRODUCTO
                                                for discountName in discountList:
                                                    productBrand = discountName.find_elementsget_attribute('innerHTML')
                                            discountList = discount.find_elements(By.XPATH, './div[1]/div/div/div/div[1]/div/div/img')
                                            if len(discountList) > 0:
                                                for images in discountList:
                                                    productImage = images.find_elementsget_attribute('src')
                                                    productName = images.find_elementsget_attribute('alt')
                                                    break
                                            else:
                                                discountList = discount.find_elements(By.XPATH, './div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/img')
                                                for images in discountList:
                                                    productImage = images.find_elementsget_attribute('src')
                                                    productName = images.find_elementsget_attribute('alt')
                                                    break
                                            discountList = discount.find_elements(By.XPATH, './div')
                                            for semifinal in discountList:
                                                listOfPriceAndDiscount = semifinal.find_elements(By.XPATH, './div/div/div/div')
                                                if len(listOfPriceAndDiscount) > 0:
                                                    price1 = ''
                                                    price2 = ''
                                                    for semifinal2 in listOfPriceAndDiscount:
                                                        stringPrices = semifinal2.find_elements(By.XPATH, './span/span/span')
                                                        if len(stringPrices) > 0:
                                                            counter += 1
                                                            price = ''
                                                            for prices in stringPrices:
                                                                price += prices.find_elementsget_attribute('innerHTML')
                                                            if len(price1) == 0:
                                                                price1 = price
                                                            else:
                                                                price2 = price
                                                        else:
                                                            stringPrices = semifinal2.find_elements(By.XPATH, './span/span')
                                                            if len(stringPrices) > 0:
                                                                counter += 1
                                                                price = ''
                                                                for prices in stringPrices:
                                                                    price += prices.find_elementsget_attribute('innerHTML')
                                                                if len(price1) == 0:
                                                                    price1 = price
                                                                else:
                                                                    price2 = price
                                                else:
                                                    listOfPriceAndDiscount = semifinal.find_elements(By.XPATH, './div/div[3]/div/div[4]/div/div')
                                                    if len(listOfPriceAndDiscount) > 0:
                                                        price1 = ''
                                                        price2 = ''
                                                        for semifinal2 in listOfPriceAndDiscount:
                                                            stringPrices = semifinal2.find_elements(By.XPATH, './span/span/span')
                                                            if len(stringPrices) > 0:
                                                                counter += 1
                                                                price = ''
                                                                for prices in stringPrices:
                                                                    price += prices.find_elementsget_attribute('innerHTML')
                                                                if len(price1) == 0:
                                                                    price1 = price
                                                                else:
                                                                    price2 = price
                                                            else:
                                                                stringPrices = semifinal2.find_elements(By.XPATH, './span/span')
                                                                if len(stringPrices) > 0:
                                                                    counter += 1
                                                                    price = ''
                                                                    for prices in stringPrices:
                                                                        price += prices.find_elementsget_attribute('innerHTML')
                                                                    if len(price1) == 0:
                                                                        price1 = price
                                                                    else:
                                                                        price2 = price
                        if(appendProducts):
                            productName = productName.replace(",","")
                            productList.append({'Name' : productName, 'Brand' : productBrand, 
                                        'Image': productImage, 'Price 1' : price1, 'Price 2': price2, 
                                        'Discount (%)' : discountTag, 'Link' : productLink})
                        if counter == 0:
                            firstIteration = driver.find_elements(By.XPATH,'/html/body/div[2]/div/div[1]/div/div')
                            for zero in firstIteration:
                                firstListOfPrices = zero.find_elements(By.XPATH, './div/div/section/div[2]/div/div')
                                for second in firstListOfPrices:
                                    secondListOfPrices = second.find_elements(By.XPATH, './div/div[2]/div/div')
                                    for third in secondListOfPrices:
                                        thirdListOfPrices = third.find_elements(By.XPATH, './div/div/div/div/div')
                                        for fourth in thirdListOfPrices:
                                            price1 = ''
                                            price2 = ''
                                            finalList = fourth.find_elements(By.XPATH, './section/a/article/div/div/div[3]/div/div[4]/div/div')
                                            pricePositionCounter = 1
                                            increment = False
                                            for final in finalList:
                                                stringPrices = final.find_elements(By.XPATH, './span/span/span')
                                                if len(stringPrices) > 0:
                                                    increment = True
                                                    price = ''
                                                    for prices in stringPrices:
                                                        price += prices.find_elementsget_attribute('innerHTML')
                                                    price1 = price
                                                else:
                                                    stringPrices = fourth.find_elements(By.XPATH, './span/span')
                                                    if len(stringPrices) > 0:
                                                        increment = True
                                                        price = ''
                                                        for prices in stringPrices:
                                                            price += prices.find_elementsget_attribute('innerHTML')
                                                        price2 = price
                                                try:
                                                    if len(price1) > 0:
                                                        productList[priceCounter][f'Price {pricePositionCounter}'] = price1
                                                    if len(price2) > 0:
                                                        productList[priceCounter][f'Price {pricePositionCounter}'] = price2
                                                except:
                                                    pass
                                                pricePositionCounter += 1
                                            if increment:
                                                priceCounter += 1
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                        time.sleep(3)
                        clickPages = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[1]/div/div')
                        pageExist = False 
                        if len(clickPages) > 0: 
                            for clicks in clickPages:
                                click = clicks.find_elements(By.XPATH, './div/div/section/div[2]/div/div')
                                for f in click:
                                    semifinalClick = f.find_elements(By.XPATH, './div/div')
                                    for finalClick in semifinalClick:
                                        clickDivDiv = finalClick.find_elements(By.XPATH, './div/div')
                                        for clickDivDiv2 in clickDivDiv:
                                            pagesDiv = clickDivDiv2.find_elements(By.XPATH, './div/div')
                                            for page2 in pagesDiv:
                                                try:
                                                    finalPage = page2.find_elementsget_attribute('innerHTML')                                         
                                                    if str(page) == finalPage:
                                                        pageExist = True 
                                                        page += 1
                                                        page2.click()
                                                        time.sleep(5)
                                                        break
                                                except:
                                                    pass
                                            if pageExist:
                                                break
                                        if pageExist:
                                            break
                                    if pageExist:
                                        break
                                if pageExist:
                                    break
                            if pageExist == False:
                                break
                        else:
                            break

                        if pageExist == False:
                            break

                if len(productList) > 0:
                    df = pd.DataFrame(productList)
                    if os.path.isfile(f'{localPath}{response.meta["categoryName"]}/{response.meta["subCategoryName"]}/{response.meta["subCategoryNameChild"]}.csv'):
                        df.to_csv(f'{localPath}{response.meta["categoryName"]}/{response.meta["subCategoryName"]}/{response.meta["subCategoryNameChild"]}.csv', mode='a', index=False, header=False)
                    else:
                        df.to_csv(f'{localPath}{response.meta["categoryName"]}/{response.meta["subCategoryName"]}/{response.meta["subCategoryNameChild"]}.csv', index=False)
                    print('Product appended')
                print('\n\n\n')
            except ValueError as e:
                print(e)
                print('\n\n\n')
                pass
        except ValueError as e:
            print('Selenium except')
            print('\n\n\n')
            pass
