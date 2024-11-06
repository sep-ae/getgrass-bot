Here’s the updated README with instructions to create a `user_id.txt` file for storing the user ID.

---

# BOT GRASS AUTO FARMING

This project is a modified bot script for automating actions on Grass, adapted from the original script by [Airdrop Family IDN](https://github.com/AirdropFamilyIDN-V2-0/grass).

## Installation Requirements

Clone the repository:
```bash
git clone https://github.com/sep-ae/getgrass-bot.git
```

Install necessary dependencies:
```bash
pip install requests
pip install loguru
pip install websockets==12.0
pip install fake_useragent
pip install websockets_proxy
```

Run the script:
```bash
python localgrassnode.py
python localgrasslite.py
```

## Setting Up Proxies

To use proxies with the bot, create a file named `local_proxies` in the project directory. Add each proxy in the following format:
```
http://user:pass@ip:port
http://user:pass@ip:port
http://user:pass@ip:port
http://user:pass@ip:port
http://user:pass@ip:port
```
Each line represents a single proxy. Replace `user`, `pass`, `ip`, and `port` with your proxy details.

## How to Retrieve and Save Your User ID on Grass

1. Log in to the Grass website.
2. Open Developer Tools (press F12 or right-click and select "Inspect").
3. Go to the **Console** tab.
4. Paste the following code to retrieve your `userId`:
   ```javascript
   localStorage.getItem('userId')
   ```
   > If pasting doesn’t work, type `allow pasting` and press Enter, then try again.

5. Copy the retrieved `userId` and save it in a file named `user_id.txt` in the project directory. The `user_id.txt` file should contain only the user ID, like this:
   ```
   your-user-id-here
   ```

---

