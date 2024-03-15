# # from django.test import TestCase

# # from .models import Header
# from selenium import webdriver
# import time,json
# from selenium.webdriver.common.by import By

# driver=webdriver.Chrome()

# driver.get('https://www.amazon.in/')
# time.sleep(20)

# cards = driver.find_elements(By.XPATH, '//*[@id="hmenu-content"]/ul[1]/li/a')
# cards2 = driver.find_elements(By.XPATH, ' //*[@id="hmenu-content"]/ul[1]/ul[1]/li/a')
# result = {}

# for index, card in enumerate(cards2[0:]):  # Starting from index 3 as per your code
#     time.sleep(2)
#     try:
#         card_text = card.text
#         print(card_text)
#         card.click()
#         time.sleep(2)
#         data=f'//*[@id="hmenu-content"]/ul[{index+9}]/li/a'
#         # print(data)
#         sub_cards = driver.find_elements(By.XPATH, f'//*[@id="hmenu-content"]/ul[{index+9}]/li/a')
#         sub_card_list = []
#         for sub_card in sub_cards[1:]:
            
#             driver.execute_script("window.open(arguments[0]);", sub_card.get_attribute('href'))

#             # Switch to the new tab
#             driver.switch_to.window(driver.window_handles[1])
            
#             try:
#                 sub_sub_cat=driver.find_elements(By.XPATH,'.//li/span/a[@class="a-link-normal s-navigation-item"]')
#                 # Get the data you need from the new tab
#                 # For example, you can get the company name from the new tab
#                 for sub_cat in sub_sub_cat:
#                     sub_card_info = {
#                         sub_card.text: { sub_cat.text: sub_cat.get_attribute('href')}
#                     }

#                 # print(company_link)
            
#             # Close the new tab
#                 driver.close()

#                 # Switch back to the original tab
#                 driver.switch_to.window(driver.window_handles[0])
#                 sub_card_list.append(sub_card_info)
#             except Exception as e:
#                 # print(e)
#                 driver.close()

#                 # Switch back to the original tab
#                 driver.switch_to.window(driver.window_handles[0])
#                 pass
#         result[card_text] = sub_card_list

#         # Click the card again to collapse the options
#         sub_cards[0].click()
#     except:
#         pass
# # Convert the result dictionary to JSON
# json_data = json.dumps(result, indent=4)

# # Write JSON data to a file
# with open("D:/amazon app/amazon_scraper/amazon_app/menu_data2.json", "a") as json_file:
#     json_file.write(json_data)

# # Close the WebDriver
# driver.quit()
#     # for sub in sub_card[1:]:
#     #     name=sub.text
#     #     print(name)
#         # href=sub.find_element(By.XPATH,'//a').get_attribute('href')
#         # print(href)

#     # print(sub_card[1].text)
#     # sub_card[1].click()

# import os
# csv_filename = 'SKU_files/sku.xlsx'
# directory = os.path.dirname(csv_filename)

# # Create the directory if it doesn't exist
# os.makedirs(directory, exist_ok=True)
# directory = os.path.dirname(csv_filename)
