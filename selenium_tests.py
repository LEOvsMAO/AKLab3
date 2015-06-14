from selenium import webdriver


driver = webdriver.Firefox()

driver.get('http://127.0.0.1:5000/users')


def test_edit():
    user_link = driver.find_element_by_name('userLink')
    user_link.click()
    name_input = driver.find_element_by_id('name')
    prev_name = name_input.get_attribute("value")
    address_input = driver.find_element_by_id('address')
    prev_address = address_input.get_attribute("value")

    name_input.send_keys("newTestName")
    address_input.send_keys("newTestAddress")
    save_button = driver.find_element_by_id("save")
    save_button.click()
    name_input = driver.find_element_by_id('name')
    new_name = name_input.get_attribute("value")
    address_input = driver.find_element_by_id('address')
    new_address = address_input.get_attribute("value")
    assert new_name == prev_name + "newTestName" and new_address == prev_address + "newTestAddress"
    address_input.clear()
    address_input.send_keys(prev_address)
    name_input.clear()
    name_input.send_keys(prev_name)
    save_button = driver.find_element_by_id("save")
    save_button.click()


test_edit()

driver.close()
