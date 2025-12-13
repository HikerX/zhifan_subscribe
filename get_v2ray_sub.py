#!/usr/bin/python3

import requests;
import re;
import base64;
import json
import uuid;
import urllib.parse

ss_url_github = "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7";
v2ray_url_github = "https://github.com/Alvin9999/new-pac/wiki/v2ray%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7";
#url = "https://gitlab.com/zhifan999/fq/-/wikis/v2ray%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
#url = "https://s3.dualstack.us-west-2.amazonaws.com/zhifan2/wiki.html"

#
ssv2_url_fn = "https://proxy.v2gh.com/https://raw.githubusercontent.com/free-nodes/v2rayfree/main/v2"



def write_to_local(file_name, content):
    f = open(file_name, "w");
    f.write(content)
    f.close();

#write_to_local("v2ray_demo.html", html);

def read_from_local(file_name):
    f = open(file_name, "r");
    return f.read();


#将SS-URI链接转换为在线更新要求的json格式配置
#https://shadowsocks.org/doc/sip008.html
def trans_uri2cfg(ss_uri):
	#SS-URI = "ss://" userinfo "@" hostname ":" port [ "/" ] [ "?" plugin ] [ "#" tag ]
	#userinfo = websafe-base64-encode-utf8(method  ":" password)
	#           method ":" password 
	# hostname ipv4 111.22.22.33:2345, ipv6 [2001:bc8:32d7:2013::10]:1111，提取ipv6地址需注意包围[]
	mPattern = r"ss://(?P<userinfo>[\w=+-]+)@\[?(?P<hostname>[A-Za-z0-9:.]+)\]?:(?P<port>[A-Za-z0-9:.]+)#(?P<tag>.+)"
	matched = re.search(mPattern, ss_uri)
	#print(matched.group("hostname"))
	#print(matched.group("port"))    
	info_ec = matched.group("userinfo");
	while len(info_ec) % 4 != 0:
		info_ec += "=";
	info = base64.urlsafe_b64decode(
	info_ec.encode("utf-8")).decode("utf-8")   
	info_sub = info.split(":");
	uuidv4 = str(uuid.uuid4())
	#print(uuidv4)
	
	cfg = {'id': uuidv4, \
	'remarks': urllib.parse.unquote(matched.group('tag')),\
	'server': matched.group('hostname'),\
	'server_port': matched.group('port'),\
	'password': info_sub[1],\
	'method': info_sub[0],\
	'plugin': '',\
	'plugin_opts': ''}    
	#print(cfg);
	return cfg
        
def add_ssr_group(ssr_url):
	content = ssr_url.replace("ssr://", "")
	while len(content) % 4 !=0:
		content += "=";
	plain_content = base64.urlsafe_b64decode(content.encode("utf-8"))\
	.decode("utf-8");    
	#根据模板，添加"group"属性
	plain_content += "&group=eXVuZmFu"; #yunfan    
	return "ssr://" + base64.urlsafe_b64encode(plain_content.encode("utf-8")).decode("utf-8");            

def main():

    ss_html = requests.get(ss_url_github).text;
    v2ray_html = requests.get(v2ray_url_github).text;
    #print(html)

    fn_uri_ec = requests.get(ssv2_url_fn).text;
    
    #write_to_local("freenodes-uri.txt", fn_uri_ec)
    
    while len(fn_uri_ec) % 4 != 0:
        fn_uri_ec += "=";
    fn_ss_text = base64.urlsafe_b64decode(fn_uri_ec.encode("utf-8")).decode("utf-8")

    fn_ss_list = fn_ss_text.split("\n");
    fn_ss_iter = filter(lambda s : re.match("ss://", s), fn_ss_list)

    #html = read_from_local("v2ray_demo.html");

    #github
    alv_ss_ssr = re.findall(r"data-snippet-clipboard-copy-content=\"([^\"]+)\"", ss_html);
    alv_v2_mix = re.findall(r"data-snippet-clipboard-copy-content=\"([^\"]+)\"", v2ray_html);

    #gitlab
    #v2ray_urls = re.findall(r"```bash\\r\\n([^`]+)\\r\\n```", html);

    #sub_urls = ssr_urls;

    #v2 从html页面提取，替换"&amp;"符号为"&"
    for url in alv_v2_mix:
        #上游已经修复 缺少 vmess前缀的格式错误
        '''
        if not re.match(r"vless|vmess|hysteria", url):
            url = f"vmess://{url}"
        '''
        if not re.match("&amp;", url):
            url = url.replace("&amp;", "&");
        #sub_urls.append(url)

    
    #finding pure ssr , filter
    alv_ss_uris = filter( lambda s : re.match(r"ss://", s), alv_ss_ssr)
    alv_ssr_uris = filter( lambda s : re.match(r"ssr://", s), alv_ss_ssr)
    
    #ssr 添加 group属性
    alv_ssr_uris = [ add_ssr_group(ssr) for ssr in alv_ssr_uris]

    #ss_urls = filter ( lambda url : re.match("ss://", url) ,  ssr_urls )

    print(f"{len(alv_v2_mix)} v2ray_uri, {len(alv_ss_ssr)} ssr_uri\
    {len(fn_ss_iter)} fn_ss_uri")
    
    #将 ss-uri 转换成 json 格式 config    
    ss_cfg_list = []
    for s in alv_ss_uris:
        ss_cfg_list.append(trans_uri2cfg(s))    
        
    for s in fn_ss_iter:
        ss_cfg_list.append(trans_uri2cfg(s))
    cfg_json = json.dumps({'version': 1,'servers': ss_cfg_list})

    #format
    #sub_urls = [u.replace("&amp;", "&")  for u in urls ]
    #print(sub_urls)
    #ss_pure_sub = base64.b64encode("\n".join(alv_ss_uris).encode("utf-8")).decode("utf-8");
    ssr_sub = base64.b64encode("\n".join(alv_ssr_uris).encode("utf-8")).decode("utf-8");
    #ss+ssr 
    ss_ssr_sub = base64.b64encode("\n".join(alv_ss_ssr).encode("utf-8")).decode("utf-8");
    #ss, ssr, v2
    v2_mix_sub = base64.b64encode("\n".join(alv_ss_ssr+ alv_v2_mix)\
    .encode("utf-8")).decode("utf-8");
    write_to_local("ss-cfg.json", cfg_json)
    write_to_local("ssr-pure.txt", ssr_sub)
    #write_to_local("ss-ssr.txt", ss_ssr_sub)
    write_to_local("v2-mix.txt", v2_mix_sub)

if __name__ == "__main__":
    main();

