# Bot for Supreme

A bot to cop Supreme items.
Spun off of [this](https://youtu.be/AGpKm0pdTMM) YouTube tutorial.

---
# Setting up:

1. Open up terminal
2. Clone this repo
3. Go into the repo
4. Run these commands:
```
virtualenv venv --python=python3.7.3
source venv/bin/activate
pip install selenium
deactivate
```
5. Download your chromedriver for your OS and version from [here](http://chromedriver.chromium.org/downloads), move it into the current directory, and unzip it with: `unzip <zip file>`
6. Create your `config.py` file:

```
num_items = <number of items you want>
keys = [
	{
	    # specific_url only filled out if you have it; otherwise replace with None
            "specific_url": "<specific_item_link>" || None,

	    # Keep url the same
            "url": "https://www.supremenewyork.com/shop/all/",

	    # the number of the item as seen in the layout on the shop/all page (second row starts at 8) 
            "item_number": <number>,

`	    # only fill out item_type if you have item type, name, and style/color wanted; otherwise replace with None
            "item_type": "<type>" || None,
            "item_name": "<name>",
            "style": "<style>",

	    # fill these with your own
            "name": "<name>",
            "email": "<email>",
            "phone": <phone>,
            "address": "<address>",
            "zip": <zip>,
            "city": "<city>",
	
	    # State number in alphabetical order of state abbrevations; California (CA) is 6
            "state": <state_number>,
            "cc_number": <card_number>,
            "exp_month": <month_number>, # 1 is January, 12 is December
            "exp_year": <year_number>, # 1 is this year, 11 is this year + 10
            "cvv": <cvv_number>
	},
	{
	  <another key list here following the same format>
	},
	{
	  <create the same amount of key lists as num_items you specified above>
	}
```
An example `config.py` file for reference:
```
num_items = 2
keys = [
	{
            "specific_url": None,
            "url": "https://www.supremenewyork.com/shop/all/",
            "item_number": None,
            "item_type": "jackets",
            "item_name": "Raglan Court Jacket",
            "style": "Olive",
            "name": "John Doe",
            "email": "johndoesemail@johndoe.com",
            "phone": 1234567890,
            "address": "1010 John Doe Way",
            "zip": 11111,
            "city": "Los Angeles",
            "state": 6, # California
            "cc_number": 123456789,
            "exp_month": 1, # January
            "exp_year": 4, # 2023
            "cvv": 111
	},
	{
            "specific_url": None,
            "url": "https://www.supremenewyork.com/shop/all/",
            "item_number": 8, # 8th item on the /shop/all page
            "item_type": None,
            "item_name": None,
            "style": None,
            "name": "John Doe",
            "email": "johndoesemail@johndoe.com",
            "phone": 1234567890,
            "address": "1010 John Doe Way",
            "zip": 11111,
            "city": "Los Angeles",
            "state": 6, # California
            "cc_number": 123456789,
            "exp_month": 1, # January
            "exp_year": 4, # 2023
            "cvv": 111
	}
}

```

---
# Run it
```
source venv/bin/activate
python bot.py
```
After you are done, run:
```
deactivate
```

