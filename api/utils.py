import re
import numpy
"""
Parsing methods to feed the classifier

"""

def parseJs(js):
    dic = {"createElement":0, "write":0, "charCodeAt":0, "concat":0, "ecsape":0, "eval": 0, "exec":0, "fromCharCode":0, "link":0, "parseInt":0,
               "replace": 0, "search": 0, "subString": 0, "unescape":0, "addEventListener": 0, "setInterval": 0, "setTimeout": 0, "push": 0, "indexOf":0,
               "documentWrite": 0, "get": 0, "find": 0, "documentCreateElement": 0, "windowSetTimeout": 0, "windowSetInterval":0}
    if js:
        if js is not None:
            for i in js: 
                try:
                        dic["createElement"] += len(re.findall(r'(createElement\()', i))
                        dic["write"] += len(re.findall(r'(write\()', i))
                        dic["charCodeAt"] +=len(re.findall(r'(charCodeAt\()', i))
                        dic["concat"] += len(re.findall(r'(concat\()', i))
                        dic["ecsape"] += len(re.findall(r'((?<!n)escape\()', i))
                        dic["eval"] += len(re.findall(r'(eval\()', i))
                        dic["exec"] += len(re.findall(r'(exec\()', i))
                        dic["fromCharCode"] += len(re.findall(r'(fromCharCode\()', i))
                        dic["link"] += len(re.findall(r'(link\()', i))
                        dic["parseInt"] += len(re.findall(r'(parseInt\()', i))
                        dic["replace"] += len(re.findall(r'(replace\()', i))
                        dic["search"] +=  len(re.findall(r'(search\()', i))
                        dic["subString"] += len(re.findall(r'(substring\()', i))
                        dic["unescape"] += len(re.findall(r'(unescape\()', i))
                        dic["addEventListener"] += len(re.findall(r'(addEventListener\()', i))
                        dic["setInterval"] += len(re.findall(r'(setInterval\()', i))
                        dic["setTimeout"] += len(re.findall(r'(setTimeout\()', i))
                        dic["push"] += len(re.findall(r'(push\()', i))
                        dic["indexOf"] += len(re.findall(r'(indexOf\()', i))
                        dic["documentWrite"] += len(re.findall(r'(document\.write\()', i))
                        dic["get"] += len(re.findall(r'(get\()', i))
                        dic["find"] += len(re.findall(r'(find\()', i))
                        dic["documentCreateElement"] += len(re.findall(r'(document\.createElement\()', i))
                        dic["windowSetTimeout"] += len(re.findall(r'(window\.setTimeout\()', i))
                        dic["windowSetInterval"] += len(re.findall(r'(window\.setInterval\()', i))   
                except:
                    pass
        return dic    
    
def parseHtml(html,js,text):
    dic = dict()
    if html is not None:
        try:
            numOfWords = len(text.split())
        except:
            numOfWords = 0
        try:
            lines = len(text.splitlines())
        except:
            lines = 0
        try:
            uniqueWords = len(set(text.split()))
        except:
            uniqueWords = 0
        try:
            words = text.split()
            averageWordLenght = sum(len(word) for word in words) / len(words)
        except:
                averageWordLenght = 0
        allTags = html.findAll()
        allParagraphs = html.findAll("p")
        divs = html.findAll("div")
        titles = html.findAll("title")
        scriptsExternal = html.find_all("script", {"src":True}) #external java script
        scripts = html.find_all("script", {"src":False}) #inline js
        scriptsAsync = html.find_all("script", {"async":True})
        scriptsType = html.find_all("script", {"type":"text/javascript"})
        anchores = html.find_all("a") #number of anchores
        anchoresToHash = html.find_all("a", {"href": "#"})
        try:
            anchoresToHttps = [httpsA for httpsA in anchores if "http" in httpsA.get("href")]
        except:
                anchoresToHttps = []
        try:
            anchoresToCom = [comA for comA in anchores if ".com" in comA.get("href")]
        except:
            anchoresToCom = []
        inputs = html.find_all("input")
        inputPassword = html.find_all("input", {"type":"password"})
        hiddenElements = html.find_all(attrs={"hidden":True}) #hidden elements
        inputHidden = html.find_all("input",{"type":"hidden"}) #hidden inputs
        objects = html.find_all("object")
        embeds = html.find_all("embed")
        frame = html.find_all("frame")
        iframe = html.find_all("iframe")
        iframeSrc = html.find_all("iframe", {"src":True})
        try:
            iframeSrcHttps = [Https for Https in iframeSrc if "http" in Https.get("src")]
        except:
            iframeSrcHttps = [] 
        center = html.find_all("center")
        imgs = html.find_all("img")
        imgsSrc = html.find_all("img", {"src": True})
        meta = html.find_all("meta")
        links = html.find_all("link")
        linksHref = html.find_all("link", {"href":True})
        try:
            linksHrefHttps = [httpsLink for httpsLink in linksHref if "http" in httpsLink.get("href")]
        except:
            linksHrefHttps = []
        try:
            linksHrefCss = [CssLink for CssLink in linksHref if ".css" in CssLink.get("href")]
        except:
            linksHrefCss = []
        linksType = html.find_all("link", {"type":"text/css"})
        linkTypeApp = html.find_all("link", {"type":"application/rss+xml"})
        linkRel = html.find_all("link", {"rel":"shortlink"})
        icon = html.find_all("link", {"rel":"shortcut icon"})
        try:
            iconHttp = [iconH for iconH in icon if "http" in iconH.get("href")]
        except:
            iconHttp = []
        if len(iconHttp) == 0:
            iconExternal = 0
        else:
            iconExternal = 1
  
        allHrefs = html.find_all(href=True)
        try:
            hrefsHttp = [hrefH for hrefH in allHrefs if "http" in hrefH.get("href")]
        except:
            hrefsHttp = []
        try:
            hrefsInternal= [hrefI for hrefI in allHrefs if "http" not in hrefI.get("href")]
        except:
            hrefsInternal = []
        allXlinkHrefs = html.find_all(attrs={"xlink:href":True})
        try:
            xlinkhrefsHttp = [xhrefH for xhrefH in allXlinkHrefs if "http" in xhrefH.get("xlink:href")]
        except:
            xlinkhrefsHttp = []
            
        try:
            xlinkhrefsInternal = [xhrefI for xhrefI in allXlinkHrefs if "http" not in xhrefI.get("xlink:href")]
        except:
            xlinkhrefsInternal = []
        if (len(allHrefs) + len(allXlinkHrefs)) == 0:
            noHrefs = 1
            externalHrefsRatio = 0 
            internalHrefsRatio = 0
        else:
            noHrefs = 0 
            if (len(hrefsHttp) + len(xlinkhrefsHttp))/(len(allHrefs) + len(allXlinkHrefs)) > 0.5:
                externalHrefsRatio = 1
            else:
                externalHrefsRatio = 0
            if (len(hrefsInternal) + len(xlinkhrefsInternal))/(len(allHrefs) + len(allXlinkHrefs)) > 0.5:
                internalHrefsRatio = 0
            else:
                internalHrefsRatio = 1
            
        formAction = html.find_all("form", {"action":True})
        try:
            formHttp = [formH for formH in formAction if "http" in formH.get("action")]
        except:
            formHttp = []
        try:
            formPhp = [formH for formH in formAction if ".php" in formH.get("action")]
        except:
            formPhp = []
        try:
            formHash = [formH for formH in formAction if "#" in formH.get("action")]
        except:
            formHash = []
        try:
            formjavascript = [formH for formH in formAction if "javascript:void()" in formH.get("action") or "javascript:void(0)" in formH.get("action")]
        except:
            formjavascript= []
        if len(formHttp) > 0 or len(formPhp) > 0 or len(formHash) > 0 or len(formjavascript) > 0:
            maliciousForm = 1
        else:
            maliciousForm = 0
        strong = html.find_all("strong")
        jsFromHtml = [x.string for x in scripts]

        for i in jsFromHtml:
            js.append(i)
           
        dic3 = parseJs(js)
  
            
            

        dic = {"AllWords":numOfWords,"UniqueWords":uniqueWords,"AverageWordLenght":averageWordLenght,"AllLines":lines,"AllTags":len(allTags), "AllParagraphs":len(allParagraphs), "divs":len(divs), "titles":len(titles), "externalJavaScripts":len(scriptsExternal), "links": len(links), "scripts":len(scripts), "scriptsAsync":len(scriptsAsync),
                    "scriptsType": len(scriptsType), "anchores": len(anchores), "anchoresToHash": len(anchoresToHash), "anchoresToHttps": len(anchoresToHttps), "anchoresToCom": len(anchoresToCom),
                    "inputs": len(inputs),"inputPassword": len(inputPassword), "hiddenElements": len(hiddenElements), "inputHidden": len(inputHidden),"objects": len(objects), "embeds": len(embeds), 
                    "frame": len(frame), "iframe": len(iframe), "iframeSrc": len(iframeSrc), "iframeSrcHttps":len(iframeSrcHttps), "center":len(center), "imgs": len(imgs), "imgsSrc": len(imgsSrc),
                    "meta": len(meta), "links": len(links), "linksHref": len(linksHref), "linksHrefHttps":len(linksHrefHttps), "linksHrefCss": len(linksHrefCss), "linksType": len(linksType),"linkTypeApp": len(linkTypeApp),
                    "linkRel": len(linkRel), "allHrefs":len(allHrefs)+len(allXlinkHrefs),"formAction": len(formAction), "formHttp":len(formHttp), "strong": len(strong),"noHrefs": noHrefs, "internalHrefRatio":internalHrefsRatio,
                    "internalHrefs":len(hrefsInternal) + len(xlinkhrefsInternal), "externalHrefRatio":externalHrefsRatio, "externalHref":len(hrefsHttp) + len(xlinkhrefsHttp), "icon":len(icon),
                    "iconExternal":iconExternal,"formPhp": len(formPhp),"formHash": len(formHash),"formjavascript": len(formjavascript),"maliciousForm":maliciousForm,"phishing": 1}
        dic.update(dic3)
        print(dic)   
    return dic

def getNp(document):
    np = numpy.empty((0,77), int)
    np = numpy.append(np,[[document["AllWords"],document["UniqueWords"],document["AverageWordLenght"],document["AllLines"],document['AllParagraphs'], document['AllTags'],document['addEventListener'],
                                document['allHrefs'],document['anchores'],document['anchoresToCom'],document['anchoresToHash'],
                                document['anchoresToHttps'], document['center'], document['charCodeAt'], document['concat'], document['createElement'], document['divs'], document['documentCreateElement'],
                                document['documentWrite'], document['ecsape'], document['embeds'], document['eval'], document['exec'], document['externalJavaScripts'], document['find'], document['formAction'],
                                document['formHttp'], document['frame'], document['fromCharCode'], document['get'], document['hiddenElements'], document['iframe'], document['iframeSrc'],
                                document['iframeSrcHttps'], document['imgs'], document['imgsSrc'], document['indexOf'], document['inputHidden'], document['inputPassword'], document['inputs'], document['link'],
                                document['linkRel'], document['linkTypeApp'], document['links'], document['linksHref'], document['linksHrefCss'], document['linksHrefHttps'], document['linksType'], 
                                document['meta'], document['objects'], document['parseInt'], document['push'], document['replace'], document['scripts'], document['scriptsAsync'],
                                document['scriptsType'], document['search'], document['setInterval'], document['setTimeout'], document['strong'], document['subString'], document['titles'], document['unescape'],
                                document['windowSetInterval'], document['windowSetTimeout'], document['write'], document['noHrefs'], document['internalHrefRatio'], document['internalHrefs'],
                                document['externalHrefRatio'], document['externalHref'],document['icon'], document['iconExternal'], document['formPhp'], document['formHash'],
                                document['formjavascript'], document['maliciousForm']]], axis=0)
    return np