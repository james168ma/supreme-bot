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

start_time = time.time()

url_for_search = 'https://www.supremenewyork.com/mobile_stock.json'

categroy = 'Shirts'
keywords = ['H']
color_style = 'Black'
size = 'Any'

###### checkout #######
name = 'hasham ghuffary'
email = 'testboi@gmail.com'
phone_num = '2025550181'
address = 'street test'
apt_unit_etc = 'Apt 1'
zip_code = '90001'
city = 'Los Angeles'
state = 'CA'

crd_card_num = '4581 0983 4981 3942'
crd_card_month = '12'
crd_card_year = '2019'
crd_cvv = '999'





headers_mobile = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36', 'Content-type': 'application/x-www-form-urlencoded'}


def make_query():
    r = requests.get(url_for_search, headers=headers_mobile)
    url_webdriver = r.json()

    uper_dict = url_webdriver['products_and_categories']
    main_dict = uper_dict[categroy]    # print(len(main_dict))
    for i in main_dict:
        # print(i)
        name_of_prod = i['name']
        for _ in keywords:
            if_found = name_of_prod.find(_)

            if if_found > -1:
                return i['id']


def product_details(id):
    formated_url_product = 'https://www.supremenewyork.com/shop/{}.json'.format(id)
    r = requests.get(formated_url_product, headers=headers_mobile)
    got_json = r.json()
    styles_json = got_json['styles']

    style_id = False
    size_id = False

    for i in styles_json:
        if i['name'] == color_style:
            style_id = i['id']
            sizes_list = i['sizes']

            if size != 'Any':
                for _ in sizes_list:
                    if _['name'] == size:
                        size_id = _['id']

            elif size == 'Any':
                size_id = sizes_list[randint(0, (len(sizes_list)-1))]['id']

            print(size_id, style_id)

    return size_id, style_id


def add_to_cart_link(s, st, id_passed_ki):
    payload = {"s": s, "st": st, "qty": '1'}
    url_with_id = 'https://www.supremenewyork.com/shop/{}/add.json'.format(id_passed_ki)
    r = requests.post(url_with_id, params=payload)
    return dict(r.cookies)


class Browser:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)

    def close_browser(self):
        self.driver.close()

    def checkout(self):
        self.driver.get('https://www.supremenewyork.com/checkout')
        sleep(1)
        if 'SHIPPING / PAYMENT' not in self.driver.page_source :
            self.driver.get('https://www.supremenewyork.com/checkout')

        self.driver.implicitly_wait(5)

        self.driver.execute_script("document.getElementById('order_billing_name').setAttribute('value','{}');".format(name))
        self.driver.execute_script("document.getElementById('order_email').setAttribute('value','{}');".format(email))
        self.driver.execute_script("document.getElementById('order_tel').setAttribute('value','{}');".format(phone_num))
        self.driver.execute_script("document.getElementById('bo').setAttribute('value','{}');".format(address))
        self.driver.execute_script("document.getElementById('oba3').setAttribute('value','{}');".format(apt_unit_etc))
        self.driver.execute_script("document.getElementById('order_billing_zip').setAttribute('value','{}');".format(zip_code))
        self.driver.execute_script("document.getElementById('order_billing_city').setAttribute('value','{}');".format(city))
        self.driver.execute_script("document.getElementById('order_billing_state').setAttribute('value','{}');".format(state))

        self.driver.execute_script("document.getElementById('cnb').setAttribute('value','{}');".format(crd_card_num))
        self.driver.execute_script("document.getElementById('credit_card_month').setAttribute('value','{}');".format(crd_card_month))
        self.driver.execute_script("document.getElementById('credit_card_year').setAttribute('value','{}');".format(crd_card_year))
        self.driver.execute_script("document.getElementById('vval').setAttribute('value','{}');".format(crd_cvv))

        # Submit
        # self.driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p[2]/label/div/ins').click()
        # self.driver.find_element_by_xpath('//*[@id="pay"]/input').click()

    def captcha(self):
        captcha_entry = self.driver.execute_script("document.getElementById('g-recaptcha-response').setAttribute('value','{}');".format(input('enter captcha')))

    def add_cookies(self, cookies):
        self.driver.get('https://www.supremenewyork.com')
        for x, y in zip(list(cookies.keys()), list(cookies.values())):
            self.driver.add_cookie({'name': x, 'value': y})


def main():
    id_by_query = make_query()
    pass_s, pass_st = product_details(id_by_query)
    cookie = add_to_cart_link(pass_s, pass_st, id_by_query)
    print(cookie)

    bot = Browser()
    bot.add_cookies(cookie)
    bot.checkout()
    bot.captcha()

    # Just to measure time took Remove it in production
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(elapsed_time)
    sleep(520)

    # chreom.close()


if __name__ == '__main__':
    main()
