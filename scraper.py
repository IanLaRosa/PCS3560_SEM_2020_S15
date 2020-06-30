import urllib.request

pageURL = "https://g1.globo.com/"

fp = urllib.request.urlopen(pageURL)
mybytes = fp.read()

baseHTMLstring = mybytes.decode("utf8")
fp.close()

if(baseHTMLstring.find('currículo') != -1):
    print("SIM")
else:
    print("NÃO")