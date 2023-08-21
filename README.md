# GTM-Subdomain-Enumeration
Subdomain Enumeration using Google Tag Manager (GTM). Inspider from [Nova Security](https://github.com/novasecurityio/community-scripts/tree/main/GTM-subdomain-enum)
# Installation
```bash
$ pip3 install -r requirements.txt
```

# Usage
```bash
$ python3 gtm.py --url https://binance.com
$ python3 gtm.py --url https://www.hy-vee.com --gtm_id GTM-5TL68P
$ cat urls.txt | xargs -I{} sh -c "python3 gtm.py -u {}"
```
# Demo
![Demo](https://github.com/the-valluvarsploit/GTM-Subdomain-Enumeration/blob/main/demo.png)

