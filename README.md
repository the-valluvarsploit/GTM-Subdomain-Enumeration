# GTM-Subdomain-Enumeration
Subdomain Enumeration using Google Tag Manager (GTM). Inspider from https://github.com/novasecurityio/community-scripts/tree/main/GTM-subdomain-enum

# Usage
```bash
$ python3 gtm.py --url https://binance.com
$ python3 gtm.py --url https://www.hy-vee.com --gtm_id GTM-5TL68P
$ cat urls.txt | xargs -I{} sh -c "python3 gtm.py -u {}"
```
