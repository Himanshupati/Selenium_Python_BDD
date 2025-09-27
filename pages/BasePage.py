from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime
import os

driver = None

def set_driver(browser):
    global driver
    driver = browser

# IMP
def accept_alert():
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()

def get_xpath_index(config_browser):
    '''
    It provides index number for xpath to be flexible according to the os/screen*.
    '''
    if any(cb in config_browser for cb in ['sauce_android', 'sauce_android_tunnel', 'sauce_iphone', 'sauce_ipad']):
        xpath_index = 2
    else:
        xpath_index = 1
    return xpath_index

def get_locator_type_and_value(element_name, locator_dict):
    BY_LOCATOR_MAPPING = {
        'XPATH' : By.XPATH,
        'CSS_SELECTOR' : By.CSS_SELECTOR,
        'ID' : By.ID,
        'NAME' : By.NAME,
        'CLASS_NAME' : By.CLASS_NAME,
        'TAG_NAME' : By.TAG_NAME,
        'LINK_TEXT' : By.LINK_TEXT,
        'PARTIAL_LINK_TEXT' : By.PARTIAL_LINK_TEXT
    }
    for locator_type, elements in locator_dict.items():
        if element_name in elements:
            locator_value = elements[element_name]
            # by_type = getattr(By, locator_type.upper(), None)
            by_type = BY_LOCATOR_MAPPING.get(locator_type, None)
            by_type_raw = locator_type
            if by_type:
                print(f" '{element_name}' is found using the locator type '{by_type_raw}' and the value is '{locator_value}'")
                return by_type, locator_value
    raise ValueError(f"Element '{element_name}' not found in locator storage.")

# TODO
# def find_element_using_dynamic_locator(driver: WebDriver, element_name: str, locator_dict: dict):

def dismiss_alert():
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.dismiss()

def enter_text(locator, text):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    element.clear()
    element.send_keys(text)

def get_element_text(locator):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    return element.text

def get_element_attribute(locator, attribute_name):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    return element.get_attribute(attribute_name)

def force_click(element):
    driver.execute_script("arguments[0].click();", element)

def get_alert_text():
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    return alert.text

def highlight_element(locator):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    driver.execute_script("arguments[0].style.border='3px solid red'", element)

def unhighlight_element(locator):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    driver.execute_script("arguments[0].style.border=''", element)

def highlight_element_advance(locator, duration=2000):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    script = """
        var element = arguments[0];
        var originalStyle = element.style.border;
        var colors = ['red', 'blue', 'green', 'yellow', 'purple'];
        var index = 0
        var interval = setInterval(function() {
            element.style.border = '3px solid ' + colors[index % colors.length];
            index++;
        }, 200);
        setTimeout(function() {
            clearInterval(interval);
            element.style.border = originalStyle;
        }, arguments[1]);
    """
    driver.execute_script(script, element, duration)

def hit_enter_for(element):
    element.send_keys(Keys.ENTER)

# TODO
def hover_mouse_over(element):
    '''
    Hover over an element,
    The parameter can be either a WebElement or the locator*
    Webelement | locator -> (By, locator)
    Hint: to get the locator use method: get_locator_type_and_value or page specific method for this
    '''
    a = ActionChains(driver)
    # if isinstance(element_or_locator, WebElement):
    #     element = element_or_locator
    # elif isinstance(element_or_locator, tuple) and len(element_or_locator) == 2:
    #     element = driver.find_element(element_or_locator)
    # else:
    #     raise ValueError("The parameter must be a webelement or a locator*")
    a.move_to_element(element)
    time.sleep(2)

def sync_browser():
    WebDriverWait(driver, 50).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

def scroll_into_view(webelement):
    sync_browser()
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center',inline: 'center'});", webelement)
    sync_browser()

def scroll_top_to_bottom():
    driver.execute_script("window.scrollTo(0, 0);")
    print(f'scrolling started... {time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())}')

    def is_bottom():
        driver.execute_script("""window.isReachedBottom = function() {
            return (window.innerHeight +window.scrollY) >= document.body.offsetHeight;
        }""")
        is_reached_bottom = driver.execute_script("return window.isReachedBottom();")
        return is_reached_bottom
        # return browser.execute_script("return (window.innerHeight +window.scrollY) >= document.body.offsetHeight;")

    timeout = 40
    driver.execute_script("""
        function smoothScroll() {
            var totalHeight = 0;
            var scrollHeight = document.body.scrollHeight;
            function scrollToBottom() {
                window.scrollTo(0, totalHeight);
                totalHeight += 2;
                var newScrollHeight = document.body.scrollHeight;
                if (newScrollHeight >= scrollHeight) {
                    scrollHeight = newScrollHeight;
                    requestAnimationFrame(scrollToBottom);
                } else {
                    console.log("Reached bottom!");
                }
            }
            scrollToBottom();
        }
        smoothScroll();
    """)

    start_time = time.time()
    for i in range(1,40):
        if not is_bottom():
            if time.time() - start_time >timeout:
                break
            else:
                time.sleep(1)
        else:
            break

    # wait! not to check frequently, to avoid load
    wait = WebDriverWait(driver,10)
    footer_locator = (By.XPATH,"//footer")
    footer = driver.find_element(By.XPATH,"//footer")
    wait.until(EC.visibility_of_element_located(footer_locator))
    scroll_into_view(driver,footer)

    print(f'scrolling ended... {time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())}')

# helper
def screenshot_file_path(file_name):
    default_directory = r"../resources/screenshots"
    if not file_name:
        title_name = driver.title.replace(" ", "")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{title_name}_{timestamp}.png"

    if not os.path.dirname(file_name):
        file_path = os.path.join(default_directory, file_name)
    else:
        file_path = file_name
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    return file_path

def take_screenshot(file_name=None):
    """
    Saves a screenshot of the current page.
    The screenshots will be saved at the specified file path.
    If only file_name is provided the file will be saved at 'resources/screenshots/'.
    If no file_name is provided file will be saved with title of the page and datetime.
    """
    file_path = screenshot_file_path(file_name)
    driver.save_screenshot(file_path)
    print(f"Screenshot saved at: {file_path}")

# TODO ------
def take_element_screenshot(locator, file_name):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    file_path = screenshot_file_path(file_name)
    element.screenshot(file_path)

def wait(time_in_sec):
    driver.implicitly_wait(time_in_sec)

def wait_for_presence(locator, time_in_sec=10):
    return WebDriverWait(driver, time_in_sec).until(EC.presence_of_element_located(locator))

def wait_to_click(locator, time_in_sec=10):
    return WebDriverWait(driver, time_in_sec).until(EC.element_to_be_clickable(locator))

def wait_and_click(locator, time_in_sec=10):
    (WebDriverWait(driver, time_in_sec).until(EC.element_to_be_clickable(locator))).click()

def wait_for_text_presence_in_element(locator, text, time_in_sec=10):
    return WebDriverWait(driver, time_in_sec).until(EC.text_to_be_present_in_element(locator, text))
