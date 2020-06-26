from config import num_items, time_delay, supreme_url, google_creds, drop_timing, payment, items 
import requests
from time import sleep
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from random import randint

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--headless")

headers_mobile = {
        'user-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded'
}

supreme_mobile_stock_url = 'https://www.supremenewyork.com/mobile_stock.json'
supreme_style_url = 'https://www.supremenewyork.com/shop/{}.json'
supreme_add_url = 'https://www.supremenewyork.com/shop/{}/add.json'
item_category = 'Shorts'
item_name = 'Nylon Water Short'
item_style = 'Black'
item_size = 'Small'


def find_item(category, name):
    req = requests.get(supreme_mobile_stock_url, headers=headers_mobile)
    mobile_stock = req.json()
    
    desired_category = mobile_stock['products_and_categories'][category]
    desired_item = None
    for item in desired_category:
        if item['name'].find(name) != -1:
            desired_item = item
            break
    return desired_item['id']

#    with urllib.request.urlopen(supreme_mobile_stock_url) as url:
#        mobile_stock = json.loads(url.read().decode())
#        new_category = mobile_stock['products_and_categories']['new']
#        desired_item = None
#        for item in new_category:
#            if item['name'].find(name) != -1:
#                desired_item = item
#                break
#        return desired_item

# add random functionality later and error checks (like none remaining)
def choose_style(id_code, style, size):
    req = requests.get(supreme_style_url.format(id_code), headers=headers_mobile)
    info = req.json()
    styles = info['styles']

    style_id = None
    size_id = None

    for st in styles:
        if st['name'] == style:
            style_id = st['id']
            sizes = st['sizes']

            if size != 'Any':
                for s in sizes:
                    if s['name'] == size:
                        size_id = s['id']
                        break
            elif size == 'Any':
                # opt for most stock
                best_size = sizes[0]
                for s in sizes:
                    if best_size['stock_level'] < s['stock_level']:
                        best_size = s
                print('Auto-chose:', best_size['name'], '\n')
                size_id = best_size['id']
            print('style:', style_id, 'size:', size_id, '\n')
            return { 'style_id': style_id, 'size_id': size_id }

                

#    with urllib.request.urlopen(supreme_style_url.format(id_code)) as url:
#        info = json.loads(url.read().decode())
#        styles = info["styles"]
#        desired_style = None
#        for st in styles:
#            if st['name'].find(style) != -1:
#                desired_style = st
#                break
#        desired_size = None
#        for si in desired_style['sizes']:
#            if si['name'].find(size) != -1:
#                desired_size = si
#                break
#        return { 'desired_style' : desired_style, 'desired_size' : desired_size }


def add_to_cart(style, size, id_code):
    payload = { "st" : style, "s" : size, "h" : 1 }
    req = requests.post(supreme_add_url.format(id_code), params=payload, headers=headers_mobile)
    print(req.content)
    return dict(req.cookies)


def get_captcha_token():
    req = requests.get('http://localhost:8080/fetch')
    if req.content != None:
        print(str(req.content))
        token_pot = req.json()
        if str(req.content) == "b'[]'":
            print("Waiting for captcha...")
            sleep(.5)
        else:
            print("Got captcha token...")
            captcha_token = token_pot[0]['token']
            return captcha_token
    elif req.content == None:
        print("Captcha bank not active.")



class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver', options=chrome_options)
        self.driver.get('https://www.supremenewyork.com/shop/all') 

    def close_browser(self):
        self.driver.close()

    def checkout(self):
        self.driver.get('https://www.supremenewyork.com/checkout')
        sleep(1)
        while 'SHIPPING / PAYMENT' not in self.driver.page_source :
            self.driver.get('https://www.supremenewyork.com/checkout')
            sleep(1)

        self.driver.implicitly_wait(5)

        self.driver.execute_script("document.getElementById('order_billing_name').setAttribute('value','{}');".format(payment['name']))
        self.driver.execute_script("document.getElementById('order_email').setAttribute('value','{}');".format(payment['email']))
        self.driver.execute_script("document.getElementById('order_tel').setAttribute('value','{}');".format(payment['phone']))
        self.driver.execute_script("document.getElementById('bo').setAttribute('value','{}');".format(payment['address']))
        self.driver.execute_script("document.getElementById('order_billing_zip').setAttribute('value','{}');".format(payment['zip']))
        self.driver.execute_script("document.getElementById('order_billing_city').setAttribute('value','{}');".format(payment['city']))
        # state
        self.driver.find_element_by_xpath('//*[@id="order_billing_state"]/option[{}]'.format(payment["state"])).click()

        self.driver.execute_script("document.getElementById('rnsnckrn').setAttribute('value','{}');".format(payment['cc_number']))

        # credit card expiration month
        self.driver.find_element_by_xpath('//*[@id="credit_card_month"]/option[{}]'.format(payment["exp_month"])).click()
        # cc expiration year
        self.driver.find_element_by_xpath('//*[@id="credit_card_year"]/option[{}]'.format(payment["exp_year"])).click()

        self.driver.execute_script("document.getElementById('orcer').setAttribute('value','{}');".format(payment['cvv']))

        # Submit
        self.driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p[2]/label/div/ins').click()
        self.driver.find_element_by_xpath('//*[@id="pay"]/input').click()

    def captcha(self, token):
        captcha_entry = self.driver.execute_script("document.getElementById('g-recaptcha-response').setAttribute('value','{}');".format(input('enter captcha')))

    def add_cookie(self, cookie):
        self.driver.get('https://www.supremenewyork.com')
        for x, y in zip(list(cookie.keys()), list(cookie.values())):
            self.driver.add_cookie({'name': x, 'value': y})

if __name__ == '__main__':
    #item_id = find_item(item_category, item_name)
    #print('item:', item_id, '\n')
    #info = choose_style(item_id, item_style, item_size)
    #print('info:', info, '\n')
    #cookie = add_to_cart(info['style_id'], info['size_id'], item_id)
    #print('cookie', cookie, '\n')
    token = get_captcha_token()
    print(token)

    bot = Browser()
    #bot.add_cookie(cookie)
    sleep(10)
    bot.checkout()
    bot.captcha(token)


