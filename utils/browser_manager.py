from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.config_loader import PropertiesReader

class BrowserManager:

    def get_chrome_driver(self, headless=False):
        chrome_options = ChromeOptions()
        if headless:
            chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        return driver

    def get_saucelabs_browser(self, browsername, rversion, scenario_name, site, webdriver=None):
        config_reader = PropertiesReader("config\config.properties")
        sauce_creds = config_reader.get_section('SAUCELABS_CRED')
        sauce_user = sauce_creds.get_key('USER_NAME')
        sauce_key = sauce_creds.get_key('ACCESS_KEY')
        sauce_url = 'https://ondemand.eu-central-1.saucelabs.com:443/wd/hub'

        if browsername == 'sauce_desktop':
            from selenium import webdriver
            options = ChromeOptions()
            options.browser_version = 'latest'
            options.platform_name = 'Windows 10'

            sauce_options = {
                'username': sauce_user,
                'accessKey': sauce_key,
                'build': f'D2C_Advancepet_Desktop_{rversion}',
                'extendedDebugging': 'true',
                'capturePerformance': 'true',
                'name': f'{scenario_name} for {site}',
                'screenResolution': '1280x768',
                'commandTimeout': '600',
                'idleTimeout': '1000'
            }

            options.set_capability('sauce:options', sauce_options)
            driver = webdriver.Remote(command_executor=sauce_url, options=options)

        elif browsername == 'sauce_android':
            from appium import webdriver
            from appium.options.common import AppiumOptions

            caps = {
                'platformName': 'Android',
                'browserName': 'Chrome',
                'sauce:options': {
                    'username': sauce_user,
                    'accessKey': sauce_key,
                    'build': f'D2C_Advancepet_Android_{rversion}',
                    'name': f'{scenario_name} for {site}',
                    'deviceOrientation': 'PORTRAIT'
                },
                'appium:deviceName': 'Android GoogleAPI Emulator',
                'appium:platformVersion': '13.0',
                'appium:automationName': 'UiAutomator2'
            }
            CAPS = AppiumOptions().load_capabilities(caps)
            driver = webdriver.Remote(command_executor=sauce_url, options=CAPS)

        elif browsername == 'sauce_android_tunnel':
            from appium import webdriver
            from appium.options.common import AppiumOptions

            caps = {
                'platformName': 'Android',
                'browserName': 'Chrome',
                'sauce:options': {
                    'username': sauce_user,
                    'accessKey': sauce_key,
                    'build': f'D2C_Advancepet_Android_Tunnel_{rversion}',
                    'name': f'{scenario_name} for {site}',
                    'deviceOrientation': 'PORTRAIT',
                    'tunnelName': 'amit01_tunnel_name'
                },
                'appium:deviceName': 'Android GoogleAPI Emulator',
                'appium:platformVersion': '13.0',
                'appium:automationName': 'UiAutomator2'
            }
            CAPS = AppiumOptions().load_capabilities(caps)
            driver = webdriver.Remote(command_executor=sauce_url, options=CAPS)

        elif browsername == 'sauce_mac':
            options = SafariOptions()
            options.browser_version = '14'
            options.platform_name = 'macOS 11.00'

            sauce_options = {
                'username': sauce_user,
                'accessKey': sauce_key,
                'build': f'D2C_Advancepet_MAC_{rversion}',
                'name': f'{scenario_name} for {site}'
            }

            options.set_capability('sauce:options', sauce_options)
            driver = webdriver.Remote(command_executor=sauce_url, options=options)

        elif browsername == 'sauce_iphone':
            from appium import webdriver
            from appium.options.common import AppiumOptions

            caps = {
                'platformName': 'iOS',
                'browserName': 'Safari',
                'sauce:options': {
                    'username': sauce_user,
                    'accessKey': sauce_key,
                    'build': f'D2C_Advancepet_IOS_{rversion}',
                    'name': f'{scenario_name} for {site}',
                    'deviceOrientation': 'PORTRAIT'
                },
                'appium:deviceName': 'iPhone Instant Simulator',
                'appium:platformVersion': 'previous_major',
                'appium:automationName': 'XCUITest',
                'appium:safariAllowPopups': 'true',
                'appium:autoAcceptAlerts': 'true',
                'appium:connectHardwareKeyboard': 'true'
            }
            CAPS = AppiumOptions().load_capabilities(caps)
            driver = webdriver.Remote(command_executor=sauce_url, options=CAPS)

        elif browsername == 'sauce_ipad':
            caps = {
                'platformName': 'iOS',
                'browserName': 'Safari',
                'appium:deviceName': 'iPad Simulator',
                'appium:platformVersion': 'current_major',
                'appium:automationName': 'XCUITest',
                'sauce:options': {
                    'username': sauce_user,
                    'accessKey': sauce_key,
                    'build': f'D2C_Advancepet_IPad_{rversion}',
                    'name': f'{scenario_name} for {site}',
                    'deviceOrientation': 'PORTRAIT'
                }
            }
            driver = webdriver.Remote(sauce_url, caps)

        return driver

    def get_firefox_driver(self, headless=False):
        firefox_options = FirefoxOptions()
        if headless:
            firefox_options.add_argument('--headless')
        driver = webdriver.Firefox(options=firefox_options)
        driver.maximize_window()
        return driver
