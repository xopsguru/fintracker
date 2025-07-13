import socket
import os

APP_VERSION = "1.0.5"
APP_NAME = "Personal Finance Tracker"

def get_system_info():
    return {
        "version": APP_VERSION,
        "ip_address": socket.gethostbyname(socket.gethostname()),
        "hostname": socket.gethostname(),
        "is_container": os.path.exists('/.dockerenv'),
        "is_kubernetes": os.path.exists('/var/run/secrets/kubernetes.io')
    } 