import ast

try:
    import httplib
except:
    import http.client as httplib


def active_internet():

    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        return False


def str_to_dict(s):
    d = {}
    try:
        d = ast.literal_eval(s)
    except Exception as e:
        print e
    finally:
        return d
