from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# ALGORITHM TO FOLLOW IN ORDER TO LOGIN TO TWITTER USING SELENIUM:
# 1. Alocate the blocks to insert our data and, the button for login.
# 2. Save our credentials in two variables and then, find the way to dump them in the respective block.
# 3. Click on the button to login to twitter.
# 4. We wait for the main articles to load and once they loaded, we scroll down a little. This way, we will get another couple of articles without losing the existent ones.
# 5. Now, it's time to retrieve every container where every article is.
# 6. We execute the algorithm to retrieve the data for every article and finally, we save all of them.

#**NOTE:** Twitter saves more-less 6 to 12 articles, which means, that whenever we scroll down the upper articles got deleted and we just keep the ones
#that get inside this range. That's why, making a big scrolling doesn't make much sense at all, since the previous articles won't appear more in the html_tree. 
#In other word, **TO AVOID SATURATING THE HTML TREE WITH DIVS PER EVERY ARTICLE THAT WE LOAD WHEN WE SCROLL DOWN IN THE PAGE, TWITTER RECYCLES THE DIVS**.

from selenium.webdriver.common.keys import Keys
import json
# Setting our webdriver:
main_url = "https://twitter.com/login?lang=es" # main/seed url.
opts = Options()
ua = "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/88.0.4324.96 Chrome/88.0.4324.96 Safari/537.36"
opts.add_argument(ua)
driver = webdriver.Chrome("./chromedriver.exe", options=opts)
driver.get(main_url)

# POINT NUMBER "1".
user_xpath = "//input[@name='session[username_or_email]']"
password_xpath = "//input[@name='session[password]']"
button_xpath = "//span[text()='Iniciar sesión']"

# POINT NUMBER "2".
user = "@DanielR96234308"
passwd = "guitarras5"

user_block = WebDriverWait(driver, 10).until( # We wait up to 10seconds for the user block to load. Whenever it loads, immediatly we retrieve it.
                    EC.presence_of_element_located((By.XPATH, user_xpath))
                )
user_block.send_keys(user) # We fill the user block with our user.

passwd_block = WebDriverWait(driver, 10).until(# We wait up to 10seconds for the passowd block to load. Whenever it loads, immediatly we retrieve it.
    EC.presence_of_element_located((By.XPATH, password_xpath))
)
passwd_block.send_keys(passwd) # We fill the password block with our password.

# POINT NUMBER "3".
button = WebDriverWait(driver, 10).until( # We wait up to 10seconds for the button to load. Whenever it loads, immediatly we retrieve it.
    EC.presence_of_element_located((By.XPATH, button_xpath))
)
button.click() # Once we have filled all the required data to login, we click on the button.

"""
# WE SHOULDN'T USE THESE, BECAUSE WE NEED FOR THE PAGE TO LOAD THE DATA. IN THIS CASE, THE BLOCKS AND THE BUTTON. OTHERWISE, THE MAJORITY OF THE TIME,
# WE WOULD END UP WITH AN ERROR, SINCE SOME OF THE ELEMENTS WE ARE LOOKING FOR, PROBABLY DOESN'T EXIST AT THE TIME THE INSTRUCTION GETS EXECUTED.

driver.find_element(By.XPATH, user_xpath).send_keys(user)
driver.find_element(By.XPATH, password_xpath).send_keys(passwd)
driver.find_element(By.XPATH, button_xpath).send_keys(Keys.ENTER)
"""
# POINT NUMBER "4".
def save_data(data):
    """This function saves the data in a json file."""
    try:
        with open(f"twitter_data.json", 'w') as json_outfile:
            json.dump(data, json_outfile, ensure_ascii=False) # ENSURE_ASCII = FALSE. This way WE MAKE READABLE THE JSON FILE FOR THE HUMANS.
        print("THE DATA WAS SUCCESSFULLY SAVED!")
    except Exception as e:
        print("SOMETHING WENT WRONG WHEN SAVING THE DATA. The error is the following:")
        print(e)

def smart_wait(driver, xpath, retrieve_data=False):
    """This function help us aesthetic, since we just declare a line instead of the whole expression below."""
    if retrieve_data:
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )
        return elements
    else:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath))
        )

smart_wait(driver, "//div[@aria-label='Timeline: Your Home Timeline']//article") # We wait up to the articles are ready in the page.
scrolling_js_code = "document.getElementsByTagName('html')[0].scroll(0, 2000)" # Defining the instruction for scrolling.
driver.execute_script(scrolling_js_code) # Scrolling just 1 time. We are just practicing man.
sleep(5) # We wait a little more for the page to refresh after the scrolling.

# POINT NUMBER "5".
containers = smart_wait(driver, "//div[@aria-label='Timeline: Your Home Timeline']//article", retrieve_data=True) # We retrieve the articles once
# they are ready.

# POINT NUMBER "6".
twitter_data = list()
for i,container in enumerate(containers, start=1):
    name = container.find_element(By.XPATH,".//div[@dir='auto' and not(@role)]//span/span[not(@dir) and not(@aria-hidden)]").text
    tweet = container.find_elements(By.XPATH,".//div[not(@role)][@dir='auto' and @lang]")
    # Since any "tweet" can contain "hashtags" and those are separated from the main tag where the "tweet" is, we decided to join them.
    # Nevertheless, if there's no "hashtag", there won't we any proble, since the "tweet" will just retrieve on element in the list:
    text_ = ''
    for sentence in tweet:
        text_ += sentence.text.replace('\n','').strip()
    
    twitter_data.append({"Name":name, "Tweet":text_}) # We append the data to store it once every tweet has been saved.
    
    print("User Number:",i)
    print("NAME:",name)
    print("TWEET:",text_)
    print('\r')
    
save_data(twitter_data) # FINALLY, WE SAVE THE DATA.
