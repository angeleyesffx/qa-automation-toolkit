import gzip
import time
import calendar
import io
import requests
import zlib


def response_from_auth(method, url, payload):
    if method is None:
        print("Auth failed: method is None.")
        return None
    headers = {
        'requestTraceId': "TestData-" + method,
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = select_request(method, url, payload, headers)
    if response is not None:
        return response.json()
    print(f"Auth failed for method {method}. Check your configuration and try again.")
    return None


def get_access_token(key, method, url, payload):
    print("\nGetting Token Authentication...")
    data = response_from_auth(method, url, payload)
    if data and key in data:
        return str(data[key])
    return None


def zip_payload(payload: str) -> bytes:
    file = io.BytesIO()
    g = gzip.GzipFile(fileobj=file, mode='w')
    g.write(payload.encode("utf-8") if isinstance(payload, str) else payload)
    g.close()
    return file.getvalue()


def print_request_and_exit(method, url, headers, body_request, zip_payload_needed):
    print('\n\n*************************** DEBUG MODE ***************************')
    print('                No request made to any endpoint!!!')
    print('Add the -e flag to the command line to really execute the requests')
    print('********************************************************************\n')
    print(f'METHOD: {method}\n')
    print(f'URL: {url}\n')
    print(f'HEADERS: \n\n{headers}\n')
    payloads = body_request if isinstance(body_request, list) else [body_request]
    for req in payloads:
        unzipped = zlib.decompress(req, 16 + zlib.MAX_WBITS) if zip_payload_needed else req
        if not isinstance(unzipped, bytes):
            unzipped = unzipped.encode("utf-8")
        print(f'PAYLOAD: \n\n{unzipped.decode("utf-8")}\n')


def split(list_a, chunk_size):
    for i in range(0, len(list_a), chunk_size):
        yield list_a[i:i + chunk_size]


def get_multiple_requests(method, url, headers, payload):
    response = []
    for idx, e in enumerate(payload):
        new_headers = headers[idx] if isinstance(headers, list) else dict(headers)
        new_headers['requestTraceId'] = f"{new_headers['requestTraceId']}_part_{idx + 1}_of_{len(payload)}"
        new_headers['x-timestamp'] = str(calendar.timegm(time.gmtime()))
        response.append(requests.request(method, url, data=e, headers=new_headers))
    return response


def select_request(method, url, payload, headers, multiple_request=False):
    if method in ("post", "put", "delete"):
        if multiple_request:
            return get_multiple_requests(method, url, headers, payload)
        return requests.request(method, url, data=payload, headers=headers, verify=False)
    if method == "get":
        payloads = payload if isinstance(payload, list) else [payload]
        return [requests.get(url, headers=headers, params=p, verify=False) for p in payloads]
    print(f"Method {method} is not supported.")
    return None
