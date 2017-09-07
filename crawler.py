import re
import urllib2
import BeautifulSoup
import requests


regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

email_re = re.compile(r'([\w.,\"-]+@[\w.,-]+\.\w+)')


def isValidUrl(url):
    if regex.match(url) is not None:
        return True
    return False


def crawler(SeedUrl):
    tocrawl = [SeedUrl]
    crawled = []
    while tocrawl:
        emails = []
        page = tocrawl.pop()
        print 'Crawled:' + page + "\n"

        req = requests.get(page)
        if req.status_code != 200:
            return
        emails += email_re.findall(req.text)
        print "Email addresses are"
        print "======================"
        for e in emails:
            print e
        print "==END==\n\n\n"
        pagesource = urllib2.urlopen(page)
        s = pagesource.read()
        soup = BeautifulSoup.BeautifulSoup(s)
        links = soup.findAll('a', href=True)
        if page not in crawled:
            for l in links:
                if isValidUrl(l['href']):
                    tocrawl.append(l['href'])
            crawled.append(page)
    return crawled

print "Enter the URL you wish to crawl.."
print 'Usage  - "http://e-mailid.blogspot.in/" <-- With the double quotes'
myurl = input("@> ")
crawler(myurl)
