import datetime
import re

import parse
import time
import os
import pandas as pd
import pytest
import json
import warnings

from _pytest.runner import runtestprotocol
from pytest_bdd import feature, scenario
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver

from utils.Report_Database import insertintodb
from utils.browser_manager import BrowserManager
from utils.config_loader import load_config_json
from saucelabs_visual.client import SauceLabsVisual
from pages.BasePage import set_driver
from utils.config_loader import PropertiesReader

CONFIG_PATH = r'config/testconfig.json'
JSON_PATH = r'config/siteconfig.json'
DEFAULT_WAIT_TIME = 10
SUPPORTED_BROWSERS = ['chrome', 'firefox', 'RemoteChromeDriver']

scenario_name = "Test scenario name"
failed_tc = 0
start_timestamp = None
end_timestamp = None
manualexecutiontime = None
driver = None
driver_g = None
project_id = 'Test705'
config_browser_g = ''
site_str = ''
session_complete = False
build_update = False
CF_failure_ready = False
prod_version = ' '
environment = ''
applicationname = None

json_data = load_config_json(JSON_PATH)

def pytest_addoption(parser):
    parser.addoption('--site', type=str, help='Enter the site name!')
    parser.addoption('--env', type=str, help='Enter the environment ["prod", "live", "test"]!')
    parser.addoption('--rversion', type=str, default="Regression", help='Enter the current version "v24.10.01"!')

def pytest_configure(config):
    if any(cb in config_browser_g for cb in ['sauce_android', 'sauce_android_tunnel', 'sauce_iphone', 'sauce_ipad']):
        pytest.xpath_index = 2
    else:
        pytest.xpath_index = 1
        warnings.filterwarnings("ignore",".handshake failed.")

@pytest.fixture()
def site(pytestconfig):
    global site_str, applicationname
    site_str = pytestconfig.getoption("site")
    applicationname = pytestconfig.getoption("site")
    return pytestconfig.getoption("site")

@pytest.fixture()
def env(pytestconfig):
    global environment
    environment = pytestconfig.getoption("env")
    return pytestconfig.getoption("env")

@pytest.fixture
def rversion(pytestconfig):
    global prod_version
    print("version: (Initial) -: ", prod_version)
    prod_version = pytestconfig.getoption("rversion")
    print("version: (default/latest) -: ", prod_version)
    return pytestconfig.getoption("rversion")

@pytest.fixture
def url(site, env):
    print("env :", env)
    print("site", site)
    url = None
    if env in json_data:
        for site_info in json_data[env]:
            if site == site_info["site"]:
                url = site_info["url"]
    else:
        print('env is not there in json')
    print("url: ", url)
    return url

@pytest.fixture()
def searchers(site, env):
    searchers = None
    if env in json_data:
        for site_info in json_data[env]:
            if site == site_info["site"]:
                searchers = site_info["searchers"]
    else:
        print(f'{searchers} is not there in json')
    return searchers

@pytest.fixture()
def socialnum(site, env):
    print("environment: ", env)
    print(site)
    socialnum = None
    if env in json_data:
        for site_info in json_data[env]:
            if site == site_info["site"]:
                socialnum = site_info["socialnum"]
                print("socialnum :", socialnum)
    else:
        print(f'{socialnum} is not there in json')
    print("social num :", socialnum)
    return socialnum

@pytest.fixture(scope='session')
def config():
    with open(CONFIG_PATH) as config_file:
        data = json.load(config_file)
    return data

@pytest.fixture(scope='session')
def config_browser(config):
    global config_browser_g
    if 'browser' not in config:
        raise TypeError(f'"{config["browser"]}" is not a supported browser')
    elif config['browser'] not in SUPPORTED_BROWSERS:
        raise TypeError(f'"{config["browser"]}" is not a supported browser')
    global view
    if 'view' in config:
        view = config['view']
    config_browser_g = config['browser']
    return config['browser']

@pytest.fixture(scope='session')
def config_wait_time(config):
    return config['wait_time'] if 'wait_time' in config else DEFAULT_WAIT_TIME

def pytest_bdd_before_scenario(request, feature, scenario):
    global scenario_name
    scenario_name = scenario.name
    global manualexecutiontime
    pattern = r'\{(\d+)\}'
    matches = re.findall(pattern, scenario.name)
    if matches:
        manualexecutiontime = int(matches[0])
        scenario_name = re.sub(pattern, '', scenario.name)
    else:
        scenario_name = scenario.name
        manualexecutiontime = 0

class CommandListener(AbstractEventListener):
    def __init__(self, timeout=15, target_texts=None):
        self.timeout = timeout
        self.last_command_time = time.time()
        self.target_texts = target_texts if target_texts is not None else []

    def before_execute_script(self, script, params):
        self.last_command_time = time.time()

    def after_navigate_to(self, url, driver):
        self.check_texts(driver)

    def after_click(self, element, driver):
        self.check_texts(driver)

    def check_texts(self, driver):
        global build_update
        page_source = driver.page_source
        cfv = False
        for text in self.target_texts:
            if text in page_source:
                cfv = True
        if cfv:
            print(f'{"=" * 25}\nCloudflare has been encountered at {time.strftime("%d-%m-%Y %H:%M")}\n{"=" * 25}')
            build_update = True

    def check_command_timeout(self):
        current_time = time.time()
        elapsed_time = current_time - self.last_command_time
        if elapsed_time >= self.timeout:
            print("No new command executed for {} seconds.".format(elapsed_time))

def pytest_runtest_protocol(item, nextitem):
    global end_timestamp
    global start_timestamp, driver, config_browser_g, build_update, site_str
    json_file = open(CONFIG_PATH, 'r')
    json_data = json_file.read()
    obj = json.loads(json_data)
    savelogs = str(obj['save_logs'])
    pytest_report = runtestprotocol(item, nextitem=nextitem)
    for report in pytest_report:
        if report.when == 'call':
            start_timestamp = datetime.datetime.fromtimestamp(report.start)
            start_timestamp = start_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            end_timestamp = datetime.datetime.fromtimestamp(report.stop)
            end_timestamp = end_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            duration = round(report.duration)
            result = report.outcome.upper()
            try:
                if config_browser_g == "chrome":
                    if build_update and report.outcome.lower() == 'failed':
                        print(f'{"=" * 25}\nFailed due to CF\n{"=" * 25}')
                else:
                    if build_update and report.outcome.lower() == 'failed':
                        print(f'{"=" * 25}\nFailed due to CF\n{"=" * 25}')
                        print("build update : ", build_update)
                        print("report: ", report.outcome.lower())
                        driver.execute_script("sauce:job-build=CF_Failure_Android")
                    driver.execute_script(f"sauce:job-result={report.outcome.lower()}")
            finally:
                if driver:
                    try:
                        driver.quit()
                    except Exception as e:
                        print(f'\n{"=" * 45}\nError while quitting driver: {e}\n{"=" * 45}')
            if savelogs == 'true':
                insertintodb(scenario_name, result, start_timestamp, end_timestamp, duration, manualexecutiontime,
                             applicationname, project_id, environment, prod_version)
    return pytest_report

@pytest.fixture
def browser(config_browser, config_wait_time, request, site, rversion):
    global scenario_name, failed_tc, driver, driver_g, session_complete, CF_failure_ready
    target_texts = ["you are human", "www.cloudflare.com", "needs to review the security"]
    driver_obj = BrowserManager()
    capabilities = {}
    if config_browser == 'chrome':
        driver = driver_obj.get_chrome_driver()
    elif 'sauce' in config_browser:
        driver = driver_obj.get_saucelabs_browser(config_browser_g, rversion, scenario_name, site)
    elif config_browser == 'firefox':
        driver = driver_obj.get_firefox_driver()
    elif config_browser == 'chrome_headless':
        driver = driver_obj.get_chrome_driver(headless=True)
    else:
        raise TypeError(f'"{config_browser}" is not a supported browser')

    driver_g = driver
    event_driver = EventFiringWebDriver(driver, CommandListener(target_texts=target_texts))
    driver = event_driver
    set_driver(driver)
    yield driver
    print("driver after yield: ", driver)
    session_complete = True
    if request.session.testsfailed > 0:
        CF_failure_ready = True
    print("request.session.testsfailed", type(request.session.testsfailed))
    if build_update and CF_failure_ready:
        print(f"{'=' * 25}\nFailure Reason: !!!Failed due to cloudflare encounter!!!\n{'=' * 25}")
    current_scenario = scenario
    print("current_scenario 'before yield driver': ", current_scenario)

# get sauce_creds
config_reader = PropertiesReader("config\config.properties")
sauce_creds = config_reader.get_section('SAUCELABS_CRED')
sauce_user = sauce_creds.get_key('USER_NAME')
sauce_key = sauce_creds.get_key('ACCESS_KEY')

def create_sauce_snapshot(browser, name):
    global scenario_name, site_str
    os.environ['SAUCE_USERNAME'] = sauce_user
    os.environ['SAUCE_ACCESS_KEY'] = sauce_key
    os.environ["SAUCE_REGION"] = 'eu-central-1'
    client_v = SauceLabsVisual()
    session_id = browser.session_id
    print("Session id : ", session_id)
    if 'validate' in scenario_name.lower():
        scenario_name = scenario_name.lower().split('validate')[1]
    client_v.create_build(name=f'{site_str}Build')
    metadata = client_v.get_selenium_metadata(session_id)
    client_v.create_snapshot_from_webdriver(
        name=f"{name}_Snapshot", session_id=session_id, test_name=f"{scenario_name}",
        suite_name="Python_SUITE", capture_dom=True)
    client_v.finish_build()

@pytest.fixture(scope="session")
def sauce_client():
    global site_str, config_browser_g
    exclude_visual = {"saucelabs_mobile", "saucelabs_desktop", "chrome"}
    if not any(exv in config_browser_g for exv in exclude_visual):
        os.environ['SAUCE_USERNAME'] = sauce_user
        os.environ['SAUCE_ACCESS_KEY'] = sauce_key
        os.environ["SAUCE_REGION"] = 'eu-central-1'
        client_v = SauceLabsVisual()
        client_v.create_build(name=f'{site_str}{config_browser_g}')
        yield client_v
        client_v.finish_build()
    else:
        yield None

@pytest.fixture
def create_snapshot(sauce_client):
    global config_browser_g
    exclude_visual = {"saucelabs_mobile", "saucelabs_desktop", "chrome"}
    if not any(exv in config_browser_g for exv in exclude_visual):
        def create_snapshot(browser, name):
            global scenario_name, site_str
            if 'validate' in scenario_name.lower():
                scenario_name = scenario_name.lower().split('validate')[1]
            session_id = browser.session_id
            sauce_client.create_snapshot_from_webdriver(
                name=f"{name}_Snapshot{site_str}_{config_browser_g}", session_id=session_id,
                test_name=f"{scenario_name}",
                suite_name="Python_SUITE", capture_dom=True)
        return create_snapshot
    else:
        return lambda *args, **kwargs: None
