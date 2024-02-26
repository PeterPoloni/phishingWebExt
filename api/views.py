from django.shortcuts import render
from django.http import JsonResponse , HttpResponse
import aiohttp
from bs4 import BeautifulSoup
import requests
import asyncio
from . import utils
from xgboost import XGBClassifier, DMatrix, train, plot_importance, Booster
import numpy
import lightgbm
import joblib

def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")

def parseHtml(contents):
    soup = BeautifulSoup(contents,"html.parser")
    scriptsExternal = soup.find_all("script", {"src":True}) #external java script
    links = [link.get("src") for link in scriptsExternal]
    return links 

def scrapeHTML(url):
    html=""
    try:
        with requests.get(url, timeout=10) as r:
            html = r.text
            if r.ok: #if return code is under 400 go on
                if html != "":
                    links = parseHtml(html)
                    return html,links
                else:
                    return "",[]
            else:
                return "",[]
    except requests.ConnectionError as e:
        print(f"Connection error out `{url}`: {e}")
        return html,[]
    except requests.Timeout as e:
        print(f"Timed out `{url}`: {e}")
        return html,[]
    except Exception as e:
        print(f"Unexpected error while fetching URL `{url}`: {e}")
        return html,[]

async def scrapeExternal(domainQ, sem):
            queueContents = domainQ
            try:
                if queueContents[1] != "":
                    if "http" in queueContents[1]:
                        url = queueContents[1]
                    elif queueContents[1][0]==".":
                        queueContents[1] = queueContents[1][1:]
                        url=queueContents[0]+queueContents[1]
                    else:
                        url=queueContents[0]+queueContents[1]

                sessionTimeout = aiohttp.ClientTimeout(total=20) #set timeout
                async with sem:
                    async with aiohttp.ClientSession(timeout=sessionTimeout) as s:
                        async with s.get(url, timeout=20) as r:
                            if r.ok:
                                js = await r.text()
                                return js

            except aiohttp.ServerTimeoutError as e:
                print("Timed out")

            except aiohttp.InvalidURL as e:
                print("Unable to fetch invalid URL")

            except aiohttp.ClientError as e:
                print("ClientError while fetching URL")

            except asyncio.CancelledError as e:
                print(e, "canceled")

            except asyncio.TimeoutError as e:
                print("timed out", url)

            except AssertionError as e:
                print("AssertionError")

            except UnicodeDecodeError as e:
                print("UnicodeDecodeError error")
                
            except Exception as e:
                print("Unexpected error while fetching URL" )


async def GetExternal(URLs, domain):
        sem = asyncio.Semaphore(30)
        tasks = list()
        for url in URLs:
            task = asyncio.create_task(scrapeExternal([domain,url], sem))
            tasks.append(task)

        js = await asyncio.gather(*tasks)
        return js
        
    

def getUrl(request):
    url = request.GET.get('URL')
    html, jsExternalURL = scrapeHTML(url)
    if html=="":
        return JsonResponse("Unable to get the page HTML!", safe=False)
    jsExternal = asyncio.run(GetExternal(jsExternalURL, url))
    try:
        soup = BeautifulSoup(html,"html.parser")
        dic = utils.parseHtml(soup, jsExternal, html)
    except:
        return JsonResponse("Unable to parse the HTML!", safe=False)
    
    
    np = utils.getNp(dic)
    print(np)
    #lightGBM
    model = joblib.load('lgbm.pkl')
    predictions = model.predict(np)
    print(predictions)
    
    if predictions==0:
        return JsonResponse("This site is safe to use!", safe=False)
    else:
        return JsonResponse("This site may be malicious! Make sure to check if the URL is correct.", safe=False)
    
    #xgBoost
    #model = Booster()
    #model = XGBClassifier()
    #model.load_model('tst13second.json')
    """if predictions == 0:
        return JsonResponse("This site is safe to use!", safe=False)
    else:
        return JsonResponse("This site may be malicious! Make sure to check if the URL is correct.", safe=False)"""

