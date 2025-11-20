import requests;
import re;
import base64;

url = "https://github.com/Alvin9999/new-pac/wiki/v2ray%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7";

#url = "https://gitlab.com/zhifan999/fq/-/wikis/v2ray%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"

#url = "https://s3.dualstack.us-west-2.amazonaws.com/zhifan2/wiki.html"

#url = "https://www.baidu.com"

html = requests.get(url).text;

#print(html)

def write_to_local(file_name, content):
    f = open(file_name, "w");
    f.write(content)
    f.close();

#write_to_local("v2ray_demo.html", html);

def read_from_local(file_name):
    f = open(file_name, "r");
    return f.read();

#html = read_from_local("v2ray_demo.html");

#github
urls = re.findall(r"data-snippet-clipboard-copy-content=\"([^\"]+)\"", html);

#gitlab
#urls = re.findall(r"```bash\\r\\n([^`]+)\\r\\n```", html);

subUrls = [];
for url in urls:
    if not re.match(r"vless|vmess|hysteria", url):
        url = f"vmess://{url}"
    elif not re.match("&amp;", url):
        url = url.replace("&amp;", "&");

    subUrls.append(url)


#format
#subUrls = [u.replace("&amp;", "&")  for u in urls ]

#print(f"find {len(subUrls)} url")

#print(subUrls)

subContent = base64.b64encode("\n".join(subUrls).encode("utf-8")).decode("utf-8");
write_to_local("v2ray_sub", subContent)
print("succeed")
#patten = r"vless://([a-f0-9-]+)@([\d.]+):(\d+)\?encryption=([^&]+)&security=([^&]+)&sni=([^&]+)&fp=([^&]+)&pbk=([^&]+)&sid=([^&]+)&spx=([^&]+)&type=([^&]+)";
#patten = r"vless://([a-f0-9-]+)@([\d.]+):(\d+)";
#patten = r"<div class=\"wiki-page-details\">\n.*\n.*\n.*"
#divs = re.findall( patten, html)

#write_to_local(divs[0])


