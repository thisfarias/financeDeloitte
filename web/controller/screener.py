from selenium import webdriver 
import time
import json

def find_stock(region, driver='Chrome'):
    if driver == 'Chrome':
        from webdriver_manager.chrome import ChromeDriverManager
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif driver == 'Edge':
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        browser = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())
    elif driver == 'Explorer':
        from webdriver_manager.microsoft import IEDriverManager
        browser = webdriver.Ie(executable_path=IEDriverManager().install())
    elif driver == 'Firefox':
        from webdriver_manager.firefox import GeckoDriverManager
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif driver == 'Opera':
        from webdriver_manager.opera import OperaDriverManager
        browser = webdriver.Opera(executable_path=OperaDriverManager().install())

    browser.get('https://finance.yahoo.com/screener/new')

    button_stock = None
    while button_stock is None:
        try:
            button_stock = browser.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[3]/button[1]')
        except:
            pass


    delete_region = browser.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li[1]/button')
    delete_region.click()

    
    add_region = browser.find_element_by_xpath('//*[@id="screener-criteria"]/div[2]/div[1]/div[1]/div[1]/div/div[2]/ul/li/div')
    add_region.click()

    time.sleep(.5)
    input_filter = browser.find_element_by_xpath('//*[@id="dropdown-menu"]/div/div[1]/div/input')
    input_filter.send_keys(region)

    time.sleep(0.5)
    #all_region = browser.find_element_by_class_name('C($tertiaryColor) Mstart(12px) Cur(p) Va(m)')
    all_region = browser.find_element_by_xpath('//*[@id="dropdown-menu"]/div/div[2]/ul/li/label')
    for span in all_region.find_elements_by_tag_name('span'):
        span.click()

    while True:
        if button_stock.is_enabled() is True:
            button_stock.click()
            break


    data_json = {}
    while True:
        tbody = None
        while tbody is None:
            try:
                tbody = browser.find_element_by_xpath('//*[@id="scr-res-table"]/div[1]/table/tbody')
            except:
                pass
        
        
        for row in tbody.find_elements_by_tag_name('tr'):
            columns = row.find_elements_by_tag_name('td')
            symbol = columns[0].find_element_by_tag_name('a').text
            name = columns[1].text
            price = columns[2].find_element_by_tag_name('span').text
            data_json[symbol] ={
                'symbol':symbol,
                'name':name,
                'price':price
            }

        try:
            button_next = browser.find_element_by_xpath('//*[@id="scr-res-table"]/div[2]/button[3]')
            if button_next.is_enabled() is True:
                button_next.click()
                time.sleep(1)
            else:
                break
        except:
            break
    browser.quit()
    return data_json
