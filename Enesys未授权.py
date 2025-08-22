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
    url = args.url
    file = args.file
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
                    target = f"http://{target}"
                    targets.append(target)
    pool = Pool(30)
    pool.map(check, targets)




def check(target):
    url = f"{target}/dwr/index.html"
    headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0'
    }
    r = requests.get(url, headers=headers, verify=False,timeout=5)
    try:
        if r.status_code == 200 and 'Classes known to DWR' in r.text:
            print(f"{target}存在未授权漏洞")
        else:
            print(f"{target}不存在未授权漏洞")
    except Exception as e:
        pass


if __name__ == '__main__':
    main()