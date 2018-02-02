from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
class todayFuelPrice:
    def getPrice(self, city="Hyderabad"):
        path = "chromedriver"
        driver = webdriver.Chrome(path)

        url = "http://www.sify.com/finance/today-petrol-price/"
        driver.get(url)

        rowCount = len(driver.find_elements_by_xpath("//*[@id='contentDiv']/table/tbody/tr"))
        colCount = len(driver.find_elements_by_xpath('//*[@id="contentDiv"]/table/tbody/tr[1]/td'))
        # print(rowCount, colCount)
        for rows in range(2, rowCount+1):
            price = None
            for cols in range(1, colCount+1):
                data = driver.find_element_by_xpath('//*[@id="contentDiv"]/table/tbody/tr['+str(rows)+']''/td['+str(cols)+']').text
                if city in data:
                    price = driver.find_element_by_xpath('//*[@id="contentDiv"]/table/tbody/tr['+str(rows)+']''/td['+str(cols+1)+']').text
                    break
            if price != None:
                break
        price = price.replace("Rs.","")
        # print(data+":"+str(price))

        driver.quit()
        return float(price)

if __name__ == '__main__':
    todayFuelPrice().getPrice()
