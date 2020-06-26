# Bot for Supreme

A bot to cop Supreme items.
Inspired by [this](https://youtu.be/AGpKm0pdTMM) YouTube tutorial.

When you run the bot, it will login to Google for you and watch YouTube videos in order to get an easier reCaptcha.
Before the drop, it will switch to the Supreme website. Once the drop happens, be ready to do the reCaptcha quickly.

---
## Prerequisites
1. Make sure you have Python3 installed. [Here](https://realpython.com/installing-python/) is a guide.
2. Make sure you have virtualenv installed. [Here](https://virtualenv.pypa.io/en/stable/installation.html) is a guide.

---
## Setting up:

1. Open up terminal

2. Clone this repo: 
```
git clone https://github.com/james168ma/supreme-bot.git
```

3. Go into the repo: 
```
cd supreme-bot
```

4. Run these commands:
```
virtualenv venv --python=python3
source venv/bin/activate
pip install selenium
deactivate
```

5. Download your chromedriver for your OS and version from [here](http://chromedriver.chromium.org/downloads), move it into the current directory, and unzip it with: 
```
unzip <zip file>
```

6. (optional) run this command to lower the chance of a reCaptcha: 
```
perl -pi -e 's/cdc_/dog_/g' chromedriver
```

7. Create your `config.py` file:

```
num_items = <number of items you want>
time_delay = 1 # leave as is
supreme_url = "https://www.supremenewyork.com/shop/all/"

drop_timing = {
	"year": <year of drop>,
        "month": <month of drop>,
        "date": <date of drop>,
        "hour": <hour of drop>
}

# make sure to use a new-ish unimportant gmail account
google_creds = {
        "account": "<gmail user>",
        "password": "<gmail password>"
}

payment = {
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
}


items = [
	{
	    # specific_url only filled out if you have it; otherwise replace with None
            "specific_url": "<specific_item_link>" || None,

	    # the number of the item as seen in the layout on the shop/all page (second row starts at 8) 
            "item_number": <number>,

`	    # only fill out item_type if you have item type, name, and style/color wanted; otherwise replace with None
            "item_type": "<type>" || None,
            "item_name": "<name>",
            "style": "<style>",
	},
	{
	  <another item key here following the same format>
	},
	{
	  <create the same amount of item keys as num_items you specified above>
	}
]
```
An example `config.py` file for reference:
```
num_items = 3
time_delay = 1
supreme_url = "https://www.supremenewyork.com/shop/all/"

drop_timing = { 
        "year": 2020,
        "month": 6,
        "date": 25,
        "hour": 8
}

google_creds = {
        "account": "johndoesthrowaway@gmail.com",
        "password": "some_password"
}

payment = {
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "phone": 7648379182,
        "address": "1001 Somewhere St",
        "zip": 99999,
        "city": "Los Angeles",
        "state": 6, # California
        "cc_number": 1111111111111111,
        "exp_month": 1, # January
        "exp_year": 1, # 2020
        "cvv": 111
}

items = [
    {
        "specific_url": None,
        "item_number": None,
        "item_type": "shorts",
        "item_name": "Nylon Water Short",
        "style": "Teal Floral"
    },
    {
        "specific_url": None,
        "item_number": 8, # first item on second row of /shop/all page
        "item_type": None,
        "item_name": None,
        "style": None
    },
    {
        "specific_url": "https://www.supremenewyork.com/shop/bags/dsd01krb8/bm4bz35rx",
        "item_number": None,
        "item_type": None,
        "item_name": None,
        "style": None
    }
]
```

---
## Run it
```
source venv/bin/activate
python bot.py
```
After you are done, run:
```
deactivate
```

---
## Tips

1. Find out what items you want to cop ahead of time (through EU store)
2. Cop multiple, semi-popular items (sell out at ~60s)
3. Run the bot at least 40 minutes before the drop time
4. Minimize the YouTube video, but open it back up before the drop
