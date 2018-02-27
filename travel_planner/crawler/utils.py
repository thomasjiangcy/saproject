import sys

def make_request(req, uri, params, data=None):
    try:
        if data is None:
            res = req(uri, params=params, timeout=10)
        else:
            res = req(uri, data=data, params=params, timeout=10)
        return res
    except:
        print("Something went wrong while making request to ", uri)
        sys.exit(1)
