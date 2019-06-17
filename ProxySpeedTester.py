from helper_functions.BrowserActions import click_element, get_element_text
from helper_functions.zoe_api_requester import get_proxy_list, getProxydetails
from selenium import webdriver
from multiprocessing import Pool
import os
import argparse
from helper_functions.excel_converter import listOfJSONtoExcel
import collections


def argument_parser():
    text = 'This is a test program. It demonstrates how to use the argparse module with a program description.'
    # initiate the parser with a description
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("-m", dest="multithreaded", help="number of processes", default=None, type=int)
    parser.add_argument("-p", dest="proxyAddresses", help="Addresses to check", default=[], nargs="*", type=str)

    args = parser.parse_args()
    print("\n===================================================================")
    print("COMMAND LINE ARGUMENTS")
    print("===================================================================")
    print(f"MULTITHREAD FLAG: {args.multithreaded}")
    print(f"SUPPLIED PROXIES: {args.proxyAddresses}")
    print("===================================================================\n")

    return args


class SpeedTester:
    def __init__(self, proxy_details):
        self.proxy_ip = proxy_details['ProxyServerIPAddress']
        self.proxy_port = proxy_details['ProxyServerPort']

        self.title = proxy_details['Title']
        self.purpose = proxy_details['Purpose']

        self.defaultTestSite = "https://fast.com/"
        self.defaultResultXpath = '//div[@class="speed-results-container succeeded"]'
        self.resultUnitsXpath = '//*[@id="speed-units"]'

        print(f"\nTesting {self.proxy_ip}:{self.proxy_port}\n")

    def __startBrowserSession(self):
        print("Need to set up random profile folder")
        random_profile_name = f"profile_{os.getpid()}"
        print(f"Process Id for current session: {os.getpid()}")
        profilename = random_profile_name

        # SETTING UP PROFILE FOLDER
        path_to_dir = f"C:/ChromeprofilesOther_Container/{random_profile_name}"

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('user-data-dir=' + path_to_dir)

        # profilefolder = random_profile_name
        # chrome_options.add_argument('--profile-directory=' + profilefolder)

        # SETTTING UP PROXY
        ProxyServerIPAddress = self.proxy_ip
        ProxyServerPort = self.proxy_port
        PROXY_setting = f"{ProxyServerIPAddress}:{ProxyServerPort}"  # IP:PORT or HOST:PORT
        chrome_options.add_argument('--proxy-server=%s' % PROXY_setting)

        print("Setting Chrome Options.")
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1000, 1300)
        driver.delete_all_cookies()

        return driver

    def doTest(self):
        driver = self.__startBrowserSession()

        driver.get(self.defaultTestSite)
        speedTestresult = get_element_text(driver, self.defaultResultXpath, time_delay=60)
        speedresultsUnits = get_element_text(driver, self.resultUnitsXpath)

        driver.quit()

        msg = f"\nProxy: {self.proxy_ip}\nSpeed: {speedTestresult} {speedresultsUnits}\n"

        result = collections.OrderedDict()
        result['Proxy'] = self.proxy_ip
        result['Port'] = self.proxy_port
        result['Title'] = self.title
        result['Purpose'] = self.purpose
        result['Speed'] = speedTestresult
        result['Units'] = speedresultsUnits

        print(msg)
        return result


def proxytest(proxy_details):
    # NEW INSTANCE OF SPEED TESTER WITH GIVEN PROXY DETAILS JSON
    newProxyTest = SpeedTester(proxy_details)
    testResults = newProxyTest.doTest()

    return testResults


def testProcesshandler():
    # PARSE ANY COMMAND LINE ARGUMENTS HERE
    cmdArgs = argument_parser()

    # GET PROXIES FROM DATABASE AND PASS INFORMATION TO PROXYTEST FUNCTION
    # IF PROXIES ARE SUPPLIED AT COMMAND LINE, WILL USE THOSE TO TEST INSTEAD OF ALL THE PROXIES
    proxyListJson = []
    if cmdArgs.proxyAddresses:
        print("Adding list of proxies passed at command line to proxies to be processed")
        for proxyAddress in cmdArgs.proxyAddresses:
            proxydetail = getProxydetails(proxyAddress)
            # GET DICTIONARY OBJECTS OF THE PROXY ADDRESSES PASSED AT COMMAND LINE AND APPEND TO A LIST
            proxyListJson.append(proxydetail)
    else:
        print("No proxies passed at command line. Will use all available proxies for testing")
        proxyListJson = get_proxy_list()

    resultsList = []
    if cmdArgs.multithreaded:
        print("MULTITHREADED ENABLED")

        numthreads = cmdArgs.multithreaded
        if numthreads > 8:
            numthreads = 8

        print(f"Total number of processes running: {numthreads}")
        pool = Pool(numthreads)

        resultsList = pool.starmap(proxytest, zip(proxyListJson))
        pool.close()
        pool.join()

    else:
        for proxyInfo in proxyListJson:
            singleresult = proxytest(proxy_details=proxyInfo)
            resultsList.append(singleresult)

    print(f"List of results:\n{resultsList}")

    listOfJSONtoExcel(resultsList, 'ProxyTestResults')


if __name__ == "__main__":
    testProcesshandler()
