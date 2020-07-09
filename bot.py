'''
MIT License

Copyright (c) 2020 James Ma

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from config import num_items, time_delay, supreme_url, google_creds, drop_timing, payment, items
from random import randint
import time
import datetime as dt
import multiprocessing
import sys

test_minute_1 = 50 # 50
test_minute_2 = 0 # 0
test_second = 0 # 0

def login(driver):
    sys.stdout.write(" logging into google...\n")
    driver.get('https://accounts.google.com')
    # username
    driver.find_element_by_xpath('//*[@id="identifierId"]').send_keys(google_creds["account"])
    driver.find_element_by_xpath('//*[@id="identifierNext"]/div/span/span').click()
    time.sleep(time_delay)
    # password
    driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input').send_keys(google_creds["password"])
    driver.find_element_by_xpath('//*[@id="passwordNext"]/div/span/span').click()
    sys.stdout.write(" finished logging into google.\n\n")


def watch_videos(driver):
    urls = [
            'https://www.youtube.com/watch?v=W9q1Q74CTg4',
            'https://www.youtube.com/watch?v=FuPc1lifeLQ',
            'https://www.youtube.com/watch?v=VD7iZ3x8ahw',
            'https://www.youtube.com/watch?v=vQBH-LhJuOc'
           ]
    sys.stdout.write(" watching random youtube video to lessen chance of captcha...\n do not close window\n")
    # random youtube vid
    driver.get(urls[randint(0,3)])
    time.sleep(2*time_delay)
    # login to youtube
    driver.find_element_by_xpath('//*[@id="buttons"]/ytd-button-renderer/a').click()
    try:
        driver.find_element_by_xpath('//*[@id="movie_player"]/div[4]/button').click()
    except:
        return


def order(driver):
    sys.stdout.write("\n preparing for order...\n")
    index = 0
    while index < num_items:
        try:
            if index == 0:
                driver.get(supreme_url)
                order_time = dt.datetime(
                    drop_timing['year'],
                    drop_timing['month'],
                    drop_timing['date'],
                    drop_timing['hour'] - 1,
                    test_minute_2,
                    test_second
                )

                delay = (order_time - dt.datetime.now()).total_seconds()

                if delay > 0:
                    time.sleep(delay)
                    sys.stdout.write(" ordering...\n")
                    start_time = int(round(time.time() * 1000))
                else:
                    time.sleep(1)
            else:
                time.sleep(1)

            # ordering if you already have the specific url ready
            if items[index]['specific_url'] != None:
                driver.get(items[index]['specific_url'])
            # ordering from all with item number
            elif items[index]['item_type'] == None:
                if index == 0:
                    # refresh the page
                    driver.find_element_by_link_text('all').click()
                else:
                    driver.get(supreme_url)

                time.sleep(time_delay)

                driver.find_element_by_xpath('//*[@id="container"]/li[{}]/div/a'.format(items[index]['item_number'])).click()
                # for the css transition
                time.sleep(time_delay)

            # ordering from (item_type) page with item name
            else:
                if index == 0:
                    driver.find_element_by_link_text(items[index]['item_type']).click()
                else:
                    driver.get(supreme_url + "/{}".format(items[index]['item_type']))
                time.sleep(time_delay)
                # get product of selected color
                products = driver.find_elements_by_link_text(items[index]['item_name'])
                for item_type_link in products:
                    try:
                        parent = item_type_link.find_element_by_xpath('../..')
                        parent.find_element_by_link_text(items[index]['style']).click()
                        # for the css transition
                        time.sleep(time_delay)
                        break
                    except NoSuchElementException:
                        continue

            # if sizing provided
            if items[index]['size']:
                # select sizing if available
                try:
                    driver.find_element_by_xpath('//*[text()="{}"]'.format(items[index]['size'])).click()
                except:
                    # sizing not available so default to available option
                    index = index # do nothing
            # add to cart
            driver.find_element_by_name('commit').click()
            index += 1
        except NoSuchElementException:
            # click didn't go through so redo
            continue

    # wait for checkout button element to load
    time.sleep(time_delay)
    driver.find_element_by_class_name('button.checkout').click()

    # fill out checkout screen fields

    # name
    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(payment['name'])
    # email
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(payment['email'])
    # phone
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(payment['phone'])
    # address
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(payment['address'])
    # zip
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(payment['zip'])
    # city
    driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(payment['city'])
    # state
    driver.find_element_by_xpath('//*[@id="order_billing_state"]/option[{}]'.format(payment["state"])).click()
    # credit card number
    driver.find_element_by_id('rnsnckrn').send_keys(payment['cc_number'])
    # credit card expiration month
    driver.find_element_by_xpath('//*[@id="credit_card_month"]/option[{}]'.format(payment["exp_month"])).click()
    # cc expiration year
    driver.find_element_by_xpath('//*[@id="credit_card_year"]/option[{}]'.format(payment["exp_year"])).click()
    # CCV
    driver.find_element_by_xpath('//*[@id="orcer"]').send_keys(payment['cvv'])
    # terms and conditions
    driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p[2]/label/div/ins').click()

    # process payment
    driver.find_element_by_name('commit').click()
    sys.stdout.write(" enter your captcha response...\n\n")

    end_time = int(round(time.time() * 1000))
    sys.stdout.write(' order ran in: {} s\n'.format((end_time - start_time)/1000))


if __name__ == '__main__':
    sys.stdout.write("""
 --------------------------------------------

    MIT License

    Copyright (c) 2020 James Ma

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

 --------------------------------------------
 supreme-bot v.1.0.0
 --------------------------------------------


""")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--mute-audio')
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('start-maximized')
    # chrome_options.add_argument('window-size="300,300"')

    # load chrome(s)
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    login = multiprocessing.Process(target=login, args=(driver, ))

    # login to google
    login.start()

    login.join()

    watcher = multiprocessing.Process(target=watch_videos, args=(driver, ))

    # watch youtube videos
    watcher.start()

    order = multiprocessing.Process(target=order, args=(driver, ))

    order_time = dt.datetime(
            drop_timing['year'],
            drop_timing['month'],
            drop_timing['date'],
            drop_timing['hour'] - 1,
            test_minute_1
    )

    delay = (order_time - dt.datetime.now()).total_seconds()
    time.sleep(delay)

    order.start()
