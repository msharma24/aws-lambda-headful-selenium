from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
import json
import sys
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
import requests
import re
import sys
import json
import time
from shapely.geometry import Polygon
import atexit
import warnings
import random
warnings.filterwarnings("ignore", category=DeprecationWarning) 


#kill -9 $(ps -eo comm,pid,etimes | awk '/^chrome/ {if ($3 > 320) { print $2}}')
#ps aux | grep chromedriver | wc -l
#ps aux | grep /opt/google/chrome/chrome | grep pallas.p.shifter.io | wc -l




def findSeatmap2(sectionId):    
    sectionNode = page.execute_script('return document.querySelectorAll(".s-'+sectionId+'[class*=\'sm-\']").length');    

    #print (page.page_source)
    #if cinput["pId"] == '9139677':    
    #    page.get_screenshot_as_file("screenshot.png")
    if sectionNode > 0:        
        className = page.execute_script('return document.querySelector(".s-'+sectionId+'[class*=\'sm-\']").getAttribute("class")');
        print (className)
        m = re.search('sm-(\d+)', className)
        res = ''
        if m: 
            res = m.group(1)
            return res

#932.7777777777776,340 969.4444444444443,369.44444444444446 1045.5555555555554,331.1111111111111 1046.1111111111109,327.22222222222223 1007.2222222222222,300
    points = page.execute_script('return document.querySelector(".s-'+sectionId+'[points]").getAttribute("points")');
    if points:
        seatmapNode = page.execute_script('return document.querySelectorAll(".seatmap[points*=\''+points+'\']").length')
        if(seatmapNode > 0):
            className = page.execute_script('return document.querySelector(".seatmap[points*=\''+points+'\']").getAttribute("class")')
            m = re.search('sm-(\d+)', className)
            if m: 
                res = m.group(1)
                return res

    return ''

def findSeatMap(section,seatmaps):
    matches = []
    polygon = section.get('polygon')
    if polygon:         
        if not polygon:
            return [] 
        polygon = polygon[0]   
        if len(polygon) != 4:
            return []

        p1 = Polygon([(float(polygon[0][0]),float(polygon[0][1])), (float(polygon[1][0]), float(polygon[1][1])), (float(polygon[2][0]), float(polygon[2][1])), (float(polygon[3][0]), float(polygon[3][1]))])        
        for seatmap in seatmaps:
            polygon2 = seatmap.get('polygon')
            if not polygon2:
                continue                        
            polygon2 = polygon2[0]            
            if len(polygon2) != 4:
                continue                        
            p2 = Polygon([(float(polygon2[0][0]),float(polygon2[0][1])), (float(polygon2[1][0]), float(polygon2[1][1])), (float(polygon2[2][0]), float(polygon2[2][1])), (float(polygon2[3][0]), float(polygon2[3][1]))])            
            if p2.contains(p1):
                matches.append(seatmap)
    return matches

def getSeatmaps(seatmapIds,page):
    page.execute_script('window.seatmaps = {}; Object.filter = (obj, predicate) => Object.fromEntries(Object.entries(obj).filter(predicate));')
    for seatmapId in seatmapIds:    
        print ("Sending: ",seatmapId)
        page.execute_script('var seatmapId = "'+seatmapId+'";  window.seatmaps[seatmapId] = "pending"; window.fetchPending=1; fetch("https://mpv.tickets.com/api/pvodc/v1/events/seatmap/"+seatmapId+"/availability/?pid='+cinput['pId']+'&agency='+cinput['agency']+'&orgId=undefined&supportsVoucherRedemption=true", {"headers": {"accept": "application/json","accept-language": "en-US", "sec-ch-ua-mobile": "?0","sec-fetch-dest": "empty","sec-fetch-mode": "cors","sec-fetch-site": "same-origin","x-referer": "null"},"referrerPolicy": "strict-origin-when-cross-origin","body": null,"method": "GET","mode": "cors","credentials": "include"}).then(response => response.text()).then(data => { if(data.indexOf("have permission to access")>0)data="denied"; window.seatmaps[seatmapId] = data; });')

    wait = 60*2
    while True:
        wait = wait - 1
        time.sleep(1)    
        pending = page.execute_script('var filtered = Object.filter(window.seatmaps, ([k,v]) => v=="pending"); return Object.keys(filtered).length;')    
        print ("Pending requests: ", pending)
        if pending == 0:
            break    
        if wait <= 0:
            break

    data = page.execute_script('return window.seatmaps')
    return data



def expand_shadow_element(element):
  shadow_root = page.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

def send(driver, cmd, params={}):
    resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
    url = driver.command_executor._url + resource
    body = json.dumps({'cmd': cmd, 'params': params})
    response = driver.command_executor._request('POST', url, body)
    return response.get('value')
  



def lambda_handler(event, context):
    #
    print ("Starting...")

    print(event)
    print("--------------")
    event = str(event)
    print(event)
    cinput = json.loads(event.replace('\'', '"'))



    """
    cinput = {    
        'pId': '9062478',
        'agency': 'UOPV_PL_MPV',
        'proxy': 'pallas.p.shifter.io:15286',
        'origid': '55269',
        'seatmaps': '1'
    }
    """

     
    cinput['preurl'] = 'https://mpv.tickets.com/schedule/?agency='+cinput['agency']+'&orgid='+cinput['origid']+'#/?view=list&includePackages=true'
    cinput['url'] = 'https://mpv.tickets.com/?agency='+cinput['agency']+'&pid='+cinput['pId']+'#/event/'+cinput['pId']+'/seatmap/?seatSelection=true'
    proxyHost, proxyPort = cinput['proxy'].split(':')
    proxy = {
        'host': proxyHost,
        'port': proxyPort,
        'user': '',
        'pass': ''
    }
    output = {"requests":[]}


    #if('debug' not in cinput):exit()


    #print ("Setting up display...")
    #display = Display(visible=0, size=(1024, 768), manage_global_env=False)
    #display.start()
    #print ("display set up")

    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--proxy-server=http://'+cinput['proxy'])

    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    d = DesiredCapabilities.CHROME
    #d['loggingPrefs'] = { 'browser':'ALL', 'performance': 'ALL' }
    d["goog:loggingPrefs"] = {"performance": "ALL"}

    """
    desiredCapabilites = DesiredCapabilities.chrome()
    LoggingPreferences logPrefs = new LoggingPreferences()
    logPrefs.enable(LogType.PERFORMANCE, Level.ALL)
    desiredCapabilites.setCapability(CapabilityType.LOGGING_PREFS, logPrefs)
    """

    agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/109.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15','Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/109.0','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0','Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0','Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.55','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:108.0) Gecko/20100101 Firefox/108.0','Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; rv:108.0) Gecko/20100101 Firefox/108.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/22.11.7.42 Yowser/2.5 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.69','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/110.0','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36']
    userAgent = random.choice(agents)   
    #userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    #userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41'
    print ("User Agent: ",userAgent)



    page = webdriver.Chrome('/home/ubuntu/chromedriver',chrome_options=chrome_options,desired_capabilities=d)

    page.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": userAgent})
    page.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Selenium Stealth settings
    stealth(page,
          user_agent= userAgent,
          languages=["en-US", "en"],
          vendor="Google Inc.",
          platform="Win32",
          webgl_vendor="Intel Inc.",
          renderer="Intel Iris OpenGL Engine",
          fix_hairline=True,
      )

    page.set_page_load_timeout(30)

    print ("Browser Launched...")


    """
    page.get(cinput['preurl'])
    print(driver.page_source)
    time.sleep(1)    
    driver.save_screenshot('python.png')
    """

    tries = 0
    successLoad = False
    seatmapLoaded = False
    while successLoad == False and tries<3:
        tries = tries+1
        print ("Getting ",tries," ",cinput['url'])    
        try:
            page.get(cinput['url'])
        except:
            continue;
        
        page.save_screenshot('python.png')
        
        print ("Checking network logs...")
        browser_log = page.get_log('performance') 
        events = [process_browser_log_entry(entry) for entry in browser_log]
        events = [event for event in events if 'Network.response' in event['method']]

        for e in events:
            #if(e['params'] and e['params']['response']):
            #    print(e['params']['response']['url'])        
            #print (e)    
            params = ''
            response = ''
            url = ''
            code = ''

            params = e.get('params')    
            if(params):
                response = params.get('response')
            if(response):
                url = response.get('url')
                code = response.get('status')

            if('akamaized.net/pvimages/' in url):
                seatmapLoaded = True

            if('navmap/availability' in url):
                body = send(page,'Network.getResponseBody',{'requestId': params["requestId"]})
                print ('URL: ',url)
                print (body)
                output["avl"] = body['body']        
                output["requests"].append({"url":url,"type":"avl","code":code})
                successLoad = True

                #sec = input('Let us wait for user input. Let me know how many seconds to sleep now.\n')
                #print (body)

    if successLoad == False:
        output["requests"].append({"url":cinput['url'],"type":"mainpage","code":"500"})
        output["blocked"] = 1
        print("Failed to load main page")
        exit()

    #if cinput["pId"] == '9057060':    
    #    page.get_screenshot_as_file("screenshot.png")

    output['gaEvent'] = 0
    output['errorCode'] = ''
    if(output["avl"]):
        m = re.search('response_error code="(.+?)"', output["avl"])
        if m: output['errorCode'] = m.group(1)
        
        if 'event_inventory_type="NON_INVENTORIED"' in output["avl"]: output['gaEvent'] = True

    print("Error Code: ",output['errorCode'])
    print("GA Event: ",output['gaEvent'])
    #print (output["avl"])

    if "Access Denied" in output["avl"]:  
        output["requests"].append({"url":cinput['url'],"type":"mainpage","code":"500"})
        output["blocked"] = 1
        print("Failed to load seatmaps")
        exit()  


    #Checking for seatmap load
    if cinput['seatmaps'] == "1" and output['gaEvent'] != 1:
        print ("Checking network logs for seatmap...")
        wait = 60
        while seatmapLoaded == False:
            wait = wait - 1
            time.sleep(1)  

            print ("Waiting fot seatmap...",wait)  
            page.save_screenshot('python.png')
                
            browser_log = page.get_log('performance') 
            events = [process_browser_log_entry(entry) for entry in browser_log]
            events = [event for event in events if 'Network.response' in event['method']]

            for e in events:        
                params = e.get('params')    
                if(params):
                    response = params.get('response')
                if(response):
                    url = response.get('url')
                    code = response.get('status')
                
                if('akamaized.net/pvimages/' in url):
                    seatmapLoaded = True

            if wait <= 0:
                break    

        print (seatmapLoaded)
        time.sleep(10)

    page.save_screenshot('python.png')


    #print(events[0])
    #print(events[0]["params"]["requestId"])
    #body = page.execute_cdp_cmd('Network.getResponseBody', {'requestId': events[0]["params"]["requestId"]})
    #body = send(page,'Network.getResponseBody',{'requestId': events[5]["params"]["requestId"]})
    #body = page.execute("executeCdpCommand", {"cmd": 'Network.getResponseBody', "params": {'requestId': events[0]["params"]["requestId"]}})
    #print(body)

    output["avlSections"] = []
    if cinput['seatmaps'] == "1" and output['gaEvent'] != 1:
        print ("Processing seatmaps...")

        sections = page.execute_script('return angular.element(document.querySelector(".seatmap-page")).scope().vm.availableSections')
        seatmaps = page.execute_script('return angular.element(document.querySelector(".seatmap-page")).scope().vm.eventData.seatmaps')
        
        activeSeatmaps = []
        for section in sections:        
            map2 = findSeatmap2(section["id"])
            print ("Section ",section["id"]," Seatmap: ",map2)
            if map2 != '':
                output["avlSections"].append({"sectionId":section["id"],"seatmapId":map2})
                activeSeatmaps.append(map2)
            
            """
            maps = findSeatMap(section,seatmaps)                

            print ("--------------------------")
            print("New: ",map2)
            if len(maps)>0: print("Old: ",maps[0])
            print ("--------------------------")


            if(len(maps)>1):
                print("Matched maps: ",len(maps))    
            if(len(maps)>0):
                output["avlSections"].append({"sectionId":section["id"],"seatmapId":maps[0].get('id')})
                activeSeatmaps.append(maps[0].get('id'))
            """

        mapsData = {}
        pendingMaps = activeSeatmaps;
        allfailed = 0
        while len(pendingMaps):    
            print("Pending: ",len(pendingMaps))
            ok = 0
            notok = 0
            chunk = 4        

            group = pendingMaps[:chunk]
            print (len(group))

            data = getSeatmaps(group,page)
            pendingMaps = pendingMaps[chunk:]    

            for x in data.items():
                value = x[1]
                if(value and value!='denied' and value!='pending'):
                    output["requests"].append({"url":"seatmapId: "+x[0],"type":"seatmap","code":"200"})
                    ok = ok + 1 
                    mapsData[x[0]] = value
                else:
                    notok = notok + 1            
                    output["requests"].append({"url":"seatmapId: "+x[0],"type":"seatmap","code":"503"})
                    pendingMaps.append(x[0])

            if(notok == len(group)): 
                allfailed = allfailed+1
            else:
                allfailed = 0

            print ("OK ",ok)
            print ("Not OK ",notok)
            print (len(pendingMaps))        
            page.get('about:blank')
            page.get(cinput['url'])
            if(allfailed>3): 
                pendingMaps = []
                output["seatmaps"] = []

        #print (len(mapsData))
        output["seatmaps"] = mapsData


    page.quit()  
    print (json.dumps(output))
    exit()



