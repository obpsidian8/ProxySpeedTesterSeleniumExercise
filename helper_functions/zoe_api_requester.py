import requests
import re
from itemscrap import getzoeapiserverurl


def get_purchaser_accounts_for_seller(seller_id):
    """ Takes a seller ID (same as the seller ID value of the current deal being run from a vendor site) and returns a list of accounts associated with that vendor """
    proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoePurchaserAccounts?$filter=ZoeSellerId eq {seller_id} and Status eq 'Active'"
    site_response = requests.get(proxy_url_end_point)
    data = site_response.json()
    results = data['value']

    try:
        additional_responses_link = data['@odata.nextLink']
        print("Checking for additional results")
    except:
        additional_responses_link = None

    while additional_responses_link is not None:
        suffix_for_next_results_regex = re.compile(r"skip=(\d+)")
        suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
        additional_responses_link = f"{proxy_url_end_point}&$skip={suffix_for_next_results}"

        additional_gc_code_site_response = requests.get(additional_responses_link)
        additional_data = additional_gc_code_site_response.json()

        results = results + additional_data['value']

        try:
            additional_responses_link = additional_data['@odata.nextLink']
            suffix_for_next_results_regex = re.compile(r"skip=(\d+)")
            suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
            additional_responses_link = f"{proxy_url_end_point}&$skip={suffix_for_next_results}"
            print(f"More results available: {additional_responses_link}")
        except KeyError:
            print(f"No more results available")
            additional_responses_link = None

    return results


def getProxydetails(proxyAddress: str):
    """ Takes a proxy IP and returns a details for the proxy specified in json format """

    if proxyAddress is None:
        print("No Proxy IP address supplied")
        return None

    print(f"Looking for proxy details for: {proxyAddress}")
    proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoeProxyServers?&$filter=ProxyServerIPAddress eq '{proxyAddress}'"
    site_response = requests.get(proxy_url_end_point)

    print(site_response)

    data = site_response.json()
    results = data['value'][0]

    if results:
        print(f"Proxy  details found for IP: {results['ProxyServerIPAddress']} and port: {results['ProxyServerPort']}")
        # print(results)
        return results
    else:
        print("No proxy found")
        return None


def get_proxy_list_by_filter(filter):
    # proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoeProxyServers"
    proxy_url_end_point = f"{getzoeapiserverurl()}ZoeProxyServers"

    initialurl = proxy_url_end_point

    if filter:
        initialurl = proxy_url_end_point + f"?$filter={filter}"
    site_response = requests.get(initialurl)
    print(site_response)
    data = site_response.json()
    results = data['value']
    try:
        additional_responses_link = data['@odata.nextLink']
        print("Checking for additional results")
    except:
        additional_responses_link = None
    while additional_responses_link is not None:
        suffix_for_next_results_regex = re.compile(r"(\?.+)")
        suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
        additional_responses_link = f"{proxy_url_end_point}{suffix_for_next_results}"
        additional_gc_code_site_response = requests.get(additional_responses_link)
        additional_data = additional_gc_code_site_response.json()
        results = results + additional_data['value']
        try:
            additional_responses_link = additional_data['@odata.nextLink']
            suffix_for_next_results_regex = re.compile(r"(\?.+)")
            suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
            additional_responses_link = f"{proxy_url_end_point}{suffix_for_next_results}"
            print(f"More results available: {additional_responses_link}")
        except KeyError:
            print(f"No more results available")
            additional_responses_link = None
    return results


def get_proxy_by_id(proxy_id):
    """ Takes a proxy_id and returns a single proxy that matches the proxy_id specified """

    if proxy_id is None:
        print("This user account has not been assigned a proxy id")
        return None

    print(f"Looking for proxy for current user. Proxy Id: {proxy_id}")
    proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoeProxyServers?$filter=Id eq {proxy_id}"
    site_response = requests.get(proxy_url_end_point)

    print(site_response)

    data = site_response.json()
    results = data['value'][0]

    if results:
        print(f"Proxy found with IP: {results['ProxyServerIPAddress']} and port: {results['ProxyServerPort']}")
        return results
    else:
        print("No proxy found")
        return None


def get_proxy_list():
    proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoeProxyServers"
    site_response = requests.get(proxy_url_end_point)

    print(site_response)

    data = site_response.json()
    results = data['value']

    try:
        additional_responses_link = data['@odata.nextLink']
        print("Checking for additional results")
    except:
        additional_responses_link = None

    while additional_responses_link is not None:
        suffix_for_next_results_regex = re.compile(r"skip=(\d+)")
        suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
        additional_responses_link = f"{proxy_url_end_point}?&$skip={suffix_for_next_results}"

        additional_gc_code_site_response = requests.get(additional_responses_link)
        additional_data = additional_gc_code_site_response.json()

        results = results + additional_data['value']

        try:
            additional_responses_link = additional_data['@odata.nextLink']
            suffix_for_next_results_regex = re.compile(r"skip=(\d+)")
            suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
            additional_responses_link = f"{proxy_url_end_point}?&$skip={suffix_for_next_results}"
            print(f"More results available: {additional_responses_link}")
        except KeyError:
            print(f"No more results available")
            additional_responses_link = None

    return results


def get_all_sellers():
    proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoeSellers"
    site_response = requests.get(proxy_url_end_point)

    print(site_response)

    data = site_response.json()
    results = data['value']

    try:
        additional_responses_link = data['@odata.nextLink']
        print("Checking for additional results")
    except:
        additional_responses_link = None

    while additional_responses_link is not None:
        suffix_for_next_results_regex = re.compile(r"skip=(\d+)")
        suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
        additional_responses_link = f"{proxy_url_end_point}?&$skip={suffix_for_next_results}"

        additional_gc_code_site_response = requests.get(additional_responses_link)
        additional_data = additional_gc_code_site_response.json()

        results = results + additional_data['value']

        try:
            additional_responses_link = additional_data['@odata.nextLink']
            suffix_for_next_results_regex = re.compile(r"skip=(\d+)")
            suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
            additional_responses_link = f"{proxy_url_end_point}?&$skip={suffix_for_next_results}"
            print(f"More results available: {additional_responses_link}")
        except KeyError:
            print(f"No more results available")
            additional_responses_link = None


def get_zoe_seller_information(seller_id):
    proxy_url_end_point = f'http://mytestAPI.com:8888/api/odata/ZoeSellers?$filter=Id eq {seller_id}'
    site_response = requests.get(proxy_url_end_point)
    data = site_response.json()
    results = data['value'][0]

    return results


def get_zoe_seller_by_site_name(sitename):
    proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoeSellers?$filter=SiteName eq '{sitename}'"
    site_response = requests.get(proxy_url_end_point)
    data = site_response.json()
    result = data['value'][0]

    return result


def get_zoe_seller_by_sellercode(sellercode):
    proxy_url_end_point = f"{getzoeapiserverurl()}ZoeSellers?$filter=SellerCode eq '{sellercode}'"
    site_response = requests.get(proxy_url_end_point)
    data = site_response.json()
    result = data['value'][0]
    return result


def get_all_seller_items_by_site_name(sitename):
    # proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoeSellerItems?$filter=contains(ItemUrl, '{sitename}')"
    proxy_url_end_point = f"{getzoeapiserverurl()}ZoeSellerItems?$filter=contains(ItemUrl, '{sitename}')"
    if sitename is None:
        proxy_url_end_point = f"{getzoeapiserverurl()}ZoeSellerItems"
    site_response = requests.get(proxy_url_end_point)
    print(site_response)
    data = site_response.json()
    results = data['value']
    try:
        additional_responses_link = data['@odata.nextLink']
        print("Checking for additional results")
    except:
        additional_responses_link = None
    while additional_responses_link is not None:
        suffix_for_next_results_regex = re.compile(r"(\?.+)")
        suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
        additional_responses_link = f"{proxy_url_end_point}{suffix_for_next_results}"
        additional_gc_code_site_response = requests.get(additional_responses_link)
        additional_data = additional_gc_code_site_response.json()
        results = results + additional_data['value']
        try:
            additional_responses_link = additional_data['@odata.nextLink']
            suffix_for_next_results_regex = re.compile(r"(\?.+)")
            suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
            additional_responses_link = f"{proxy_url_end_point}{suffix_for_next_results}"
            print(f"More results available: {additional_responses_link}")
        except KeyError:
            print(f"No more results available")
            additional_responses_link = None
    print(f"Seller Items found for {sitename}: {len(results)}")
    return results


def get_all_seller_items_by_id(id):
    # proxy_url_end_point = f"http://mytestAPI.com:8888/api/odata/ZoeSellerItems?$filter=ZoeSellerId  eq {id}"
    proxy_url_end_point = f"{getzoeapiserverurl()}ZoeSellerItems?$filter=ZoeSellerId  eq {id}"
    if id is None:
        proxy_url_end_point = f"{getzoeapiserverurl()}ZoeSellerItems"
    site_response = requests.get(proxy_url_end_point)
    print(site_response)
    data = site_response.json()
    results = data['value']
    try:
        additional_responses_link = data['@odata.nextLink']
        print("Checking for additional results")
    except:
        additional_responses_link = None
    while additional_responses_link is not None:
        suffix_for_next_results_regex = re.compile(r"(\?.+)")
        suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
        additional_responses_link = f"{proxy_url_end_point}{suffix_for_next_results}"
        additional_gc_code_site_response = requests.get(additional_responses_link)
        additional_data = additional_gc_code_site_response.json()
        results = results + additional_data['value']
        try:
            additional_responses_link = additional_data['@odata.nextLink']
            suffix_for_next_results_regex = re.compile(r"(\?.+)")
            suffix_for_next_results = suffix_for_next_results_regex.search(additional_responses_link).group(1).strip()
            additional_responses_link = f"{proxy_url_end_point}{suffix_for_next_results}"
            print(f"More results available: {additional_responses_link}")
        except KeyError:
            print(f"No more results available")
            additional_responses_link = None
    print(f"Seller Items found for {id}: {len(results)}")
    return results
