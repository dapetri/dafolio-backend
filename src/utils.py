from functools import wraps
from flask import request, jsonify
import ipaddress

def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return False

def restrict_to_local_network(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        if not is_private_ip(client_ip):
            return jsonify({"error": "Access denied"}), 403
        return f(*args, **kwargs)
    return decorated_function