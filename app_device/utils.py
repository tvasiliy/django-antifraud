import requests
from http import HTTPStatus

proxy_ports = ['8080', '80', '3128']


def is_proxy(proxy_ip):
    try:
        response = requests.get(
            'https://google.com',
            proxies={'https': proxy_ip},
            timeout=5
        )
        if response.status_code == HTTPStatus.PROXY_AUTHENTICATION_REQUIRED:
            # proxy auth code
            return True
        elif response.status_code == HTTPStatus.OK:
            # http status ok
            return True
    except requests.exceptions.ConnectTimeout:
        pass
    except requests.exceptions.ProxyError:
        pass
    except requests.exceptions.ConnectionError:
        pass

    return False


def check_ip_is_proxy(ip):
    proxy_lists = ["https//{}:{}".format(ip, x) for x in proxy_ports]
    result = False

    for proxy_ip in proxy_lists:
        if is_proxy(proxy_ip):
            result = True

    return result
