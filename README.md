# Bot for Supreme

A bot to cop Supreme items.
Spun off of [this](https://youtu.be/AGpKm0pdTMM) YouTube tutorial.

---
# Setting up:

1. Open up terminal
2. Clone this repo
3. Go into the repo
4. Run: `pip install selenium`
5. Download your chromedriver from [here](http://chromedriver.chromium.org/downloads)
6. Create your `config.py` file:

```
keys = {
	# specific_url only filled out if you have it; otherwise replace with None
        "specific_url": "<specific_item_link>" || None,

	# Keep url the same
        "url": "https://www.supremenewyork.com/shop/all/",

	# the number of the item as seen in the layout on the shop/all page (second row starts at 8) 
        "item_number": <number>,

`	# only fill out item_type if you have item type, name, and style/color wanted; otherwise replace with None
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
        "exp_year": <year_number>, # 1 is this year, 10 is this year + 10
        "cvv": <cvv_number>
}
```
---
# Run it
```
python3 bot.py
```

