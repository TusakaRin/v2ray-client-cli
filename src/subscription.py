import requests, json, os, base64, subprocess, datetime, sys


def query_config(url):
    try:
        payload={}
        headers = {
            "User-Agent": "PostmanRuntime/7.28.4"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        result = base64.b64decode(response.text).decode('utf-8')
        subs = result.strip("\n").split("\n")
        subconfigs = []
        for sub in subs:
            subconfig = json.loads(base64.b64decode(sub[8:]).decode('utf-8'))
            subconfigs.append(subconfig)
        if subconfigs:
            return True, subconfigs
        else:
            return False, [] 
    except Exception as e:
        return False, []


def run_v2ray(cfg, v2rayCore, localcfg):
    workingPath = os.path.join(localcfg['cwd'], 'v2ray-client-cli')
    os.makedirs(workingPath, exist_ok=True)
    os.makedirs(os.path.join(workingPath, 'logs'), exist_ok=True)
    template = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'configs/template.json')
    with open(template, 'r') as f:
        template = json.load(f)
    with open(os.path.join(workingPath, 'config.json'), 'w') as f:
        config = template
        config['outbounds'][0]['settings']['vnext'][0]['address'] = cfg['add']
        config['outbounds'][0]['settings']['vnext'][0]['port'] = int(cfg['port'])
        config['outbounds'][0]['settings']['vnext'][0]['users'][0]['id'] = cfg['id']
        config['outbounds'][0]['settings']['vnext'][0]['users'][0]['alterId'] = int(cfg['aid'])
        json.dump(config, f)
    dt = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logpath = os.path.join(workingPath, 'logs', f"{dt}_stdout.log")
    errpath = os.path.join(workingPath, 'logs', f"{dt}_stderr.log")
    outf = open(logpath, 'w')
    errf = open(errpath, 'w')
    p = subprocess.Popen([v2rayCore, '-c', os.path.abspath(os.path.join(workingPath, 'config.json'))], cwd=workingPath, stdout=outf, stderr=errf)
    p.wait()


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        args = f.readlines()

    url = args[0].strip()
    core = args[1].strip()
    cwd = args[2].strip()

    flag, result = query_config(url)
    for i, j in enumerate(result):
        print(i, j['ps'])
    choice = int(input("input: "))
    run_v2ray(result[choice], core, {"cwd": cwd})
