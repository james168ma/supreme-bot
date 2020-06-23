from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config import keys, num_items
import time
import multiprocessing

def timeme(method):
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = method(*args, **kw)
        endTime = int(round(time.time() * 1000))
        print('order ran in:', (endTime - startTime)/1000, 's')
        return result
    return wrapper


@timeme
def order(index, driver):
    # ordering if you already have the specific url ready
    if keys[index]['specific_url'] != None:
        driver.get(keys[index]['specific_url'])
    # ordering from all with item number
    elif keys[index]['item_type'] == None:
        # get product url
        driver.get(keys[index]['url'])
        driver.find_element_by_xpath('//*[@id="container"]/li[{}]/div/a'.format(keys[index]['item_number'])).click()
        # for the css transition
        time.sleep(.5)
    # ordering from (item_type) page with item name
    else:
        # get product url
        url = keys[index]['url'] + keys[index]['item_type']
        driver.get(url)
        # get product of selected color
        products = driver.find_elements_by_link_text(keys[index]['item_name'])
        for item_type_link in products:
            try:
                item_type_link.parent.find_element_by_link_text(keys[index]['style']).click()
                # for the css transition
                time.sleep(.5)
                break
            except NoSuchElementException:
                continue

    # add to cart
    driver.find_element_by_name('commit').click()

    # wait for checkout button element to load
    time.sleep(.4)
    driver.find_element_by_class_name('button.checkout').click()

    # fill out checkout screen fields
    
    # name
    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(keys[index]['name'])
    # email
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(keys[index]['email'])
    # phone
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(keys[index]['phone'])
    # address
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(keys[index]['address'])
    # zip
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(keys[index]['zip'])
    # city
    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(keys[index]['city'])
    # state
    driver.find_element_by_xpath('//*[@id="order_billing_state"]/option[{}]'.format(keys[index]["state"])).click()
    # credit card number
    driver.find_element_by_id('rnsnckrn').send_keys(keys[index]['cc_number'])
    # credit card expiration month
    driver.find_element_by_xpath('//*[@id="credit_card_month"]/option[{}]'.format(keys[index]["exp_month"])).click()
    # cc expiration year
    driver.find_element_by_xpath('//*[@id="credit_card_year"]/option[{}]'.format(keys[index]["exp_year"])).click()
    # CCV
    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(keys[index]['cvv'])
    # terms and conditions
    driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p[2]/label/div/ins').click()

    # process payment
    driver.find_element_by_name('commit').click()
    

if __name__ == '__main__':
    # load chrome(s)
    drivers = [webdriver.Chrome('./chromedriver') for driver in range(num_items)]

    for index, driver in enumerate(drivers):
        # simultaneously make orders
        multiprocessing.Process(target=order, args=(index, driver, )).start() 

