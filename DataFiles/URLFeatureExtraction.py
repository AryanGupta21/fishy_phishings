# -*- coding: utf-8 -*-
# Importing required packages
from urllib.parse import urlparse
import ipaddress
import re
import requests
from datetime import datetime
# from bs4 import BeautifulSoup  # Removed since `web_traffic` is not used
# import whois  # Uncomment if using `domainAge` and `domainEnd`

# Feature 1: Check for IP address in the URL
def havingIP(url):
    try:
        ipaddress.ip_address(url)
        return 1  # Phishing
    except:
        return 0  # Legitimate

# Feature 2: Check for "@" symbol in the URL
def haveAtSign(url):
    return 1 if "@" in url else 0

# Feature 3: Check URL length
def getLength(url):
    return 1 if len(url) >= 54 else 0

# Feature 4: Calculate URL depth
def getDepth(url):
    path = urlparse(url).path.split('/')
    return sum(1 for segment in path if segment)

# Feature 5: Check for redirection ("//") in the URL
def redirection(url):
    pos = url.rfind('//')
    return 1 if pos > 6 else 0

# Feature 6: Check for "https" token in the domain
def httpDomain(url):
    domain = urlparse(url).netloc
    return 1 if 'https' in domain else 0

# Feature 7: Check for URL shortening services
shortening_services = r"bit\.ly|goo\.gl|tinyurl|t\.co|x\.co|ow\.ly|is\.gd|cli\.gs"
def tinyURL(url):
    return 1 if re.search(shortening_services, url) else 0

# Feature 8: Check for "-" in the domain name
def prefixSuffix(url):
    domain = urlparse(url).netloc
    return 1 if '-' in domain else 0

# Feature 9: Placeholder for DNS Record (default to 0)
def dnsRecordPlaceholder():
    return 0

# Feature 10: Placeholder for Domain Age (default to 1)
def domainAgePlaceholder():
    return 1

# Feature 11: Placeholder for Domain End Period (default to 1)
def domainEndPlaceholder():
    return 1

# Feature 12: Check for iframe redirection
def iframe(response):
    return 1 if response == "" or re.search(r"<iframe>|<frameBorder>", response.text) is None else 0

# Feature 13: Check for mouseover effect in status bar
def mouseOver(response):
    return 1 if response == "" or re.search(r"<script>.+onmouseover.+</script>", response.text) else 0

# Feature 14: Check for disabling right-click
def rightClick(response):
    return 1 if response == "" or re.search(r"event.button ?== ?2", response.text) else 0

# Feature 15: Check for website forwarding
def forwarding(response):
    return 1 if response == "" or len(response.history) > 2 else 0

# Feature Extraction Function
def featureExtraction(url):
  features = []
  # Address bar-based features
  features.append(havingIP(url))
  features.append(haveAtSign(url))
  features.append(getLength(url))
  features.append(getDepth(url))
  features.append(redirection(url))
  features.append(httpDomain(url))
  features.append(tinyURL(url))
  features.append(prefixSuffix(url))

  # Domain-based features (placeholders)
  features.append(0)  # Placeholder for DNS_Record
  features.append(1)  # Placeholder for web_traffic
  features.append(1)  # Placeholder for Domain_Age
  features.append(1)  # Placeholder for Domain_End

  # HTML & JavaScript-based features
  try:
    response = requests.get(url)
  except:
    response = ""

  features.append(iframe(response))
  features.append(mouseOver(response))
  features.append(rightClick(response))
  features.append(forwarding(response))

  return features
