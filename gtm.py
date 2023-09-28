import argparse
import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

green = "\x1b[32m"
red = "\x1b[31m"
reset = "\x1b[0m"

GTM_URL = "https://googletagmanager.com/gtm.js"

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="Target URL")
    parser.add_argument("-g", "--gtm_id", dest="gtm_id", help="Google Tag Manager ID")
    parser.add_argument("-t", "--timeout", dest="timeout", type=int, default=10, help="Timeout in seconds (default is 10)")
    args = parser.parse_args()
    if not (args.url or args.gtm_id):
        parser.print_help()
        exit()
    return args

def fetch_gtm_id(url, timeOut):
    try:
        request = requests.get(url, timeout=timeOut, verify=False)
        response = request.text
    except requests.exceptions.Timeout:
        print(f"{red}[-] Timeout occurred while fetching {url}{reset}")
        exit()
    except Exception as e:
        print(f"{red}[-] Connection Error on {url}{reset}")
        exit()

    pattern = re.compile(r"GTM-[A-Z0-9]{7}")
    gtmIdMatch = pattern.search(response)

    if gtmIdMatch:
        gtmId = gtmIdMatch.group()
        print(f"[+] GTM ID is found {url} {green}{gtmId}{reset}")
        return gtmId
    else:
        print(f"{red}[-] GTM ID is not found {url}{reset}")

def fetch_subdomains(url, gtmId, timeout):
    subdomains = []
    try:
        request = requests.get(GTM_URL , params={"id": gtmId}, timeout=timeout, allow_redirects=False)
        if request.status_code != 200:
            print(f"{red}[-] Failed to fetch {url} {request.status_code}{reset}")
        response = request.text
    except requests.exceptions.Timeout:
        print(f"{red}[-] Timeout occurred while fetching {url}{reset}")
    except Exception as e:
        print(f"{red}[-] Failed to fetch url {url} {e}{reset}")

    rootDomain = parse_root_domain(url)
    pattern = rf"((?:[a-zA-Z0-9-]+\.)*){re.escape(rootDomain)}"
    subs = re.findall(pattern, response)
    domains = [s + rootDomain for s in subs]

    for domain in domains:
        inScope = re.match(rf"^(.*\.)?{rootDomain}$", domain)
        if inScope:
            subdomains.append(domain)
    
    return subdomains

def parse_root_domain(target):
    domain_parts = target.split("/")[2].split(".")
    rootDomain = domain_parts[-2] + "." + domain_parts[-1]
    return rootDomain

def remove_duplicates(domains):
    encountered = {}
    unique_domains = []

    for v in domains:
        if v not in encountered:
            encountered[v] = True
            unique_domains.append(v)

    return unique_domains

def main():
    ARGS = get_arguments()
    url = ARGS.url
    gtm_id = ARGS.gtm_id
    timeOut = ARGS.timeout

    if url and gtm_id:
        temp_subdomains = fetch_subdomains(url, gtm_id, timeOut)
        subdomains = remove_duplicates(temp_subdomains)
        if len(subdomains) > 0:
            for subs in subdomains:
                print(f"Subdomain: {green}{subs}{reset}")
        else:
            print("[-] No subdomain found")
    else:
        gtm_id = fetch_gtm_id(url, timeOut)
        if gtm_id is not None:
            temp_subdomains = fetch_subdomains(url, gtm_id, timeOut)
            subdomains = remove_duplicates(temp_subdomains)
            if len(subdomains) > 0:
                for subs in subdomains:
                    print(f"Subdomain: {green}{subs}{reset}")
            else:
                print("[-] No subdomain found")

if __name__ == "__main__":
    main()
