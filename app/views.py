from app import app
from flask import render_template, request, Response, redirect, url_for, flash
from datetime import datetime, timedelta
import subprocess
import ipaddress
import requests

BASE_URL = "https://my.api.mockaroo.com/"
hdrs = {"content-type": "application/json", "X-API-Key": "f6f21d00"}


@app.route("/")
@app.route("/index")
def index():
    """ 
    endpoint for index
    :param none
    :return template
    """
    return render_template(
        "index.html",
        today=get_date()
    )


@app.route("/nmap", methods=["GET", "POST"])
def nmap():
    """
    endpoint for nmap scan
    :return template
    """
    total_hosts = 0
    hosts = None
    ip = None
    scan_type = None

    if request.method == "POST":
        ip = request.form["ip_network"]
        scan_type = request.form["scan_type"]

        try:
            cidr = ipaddress.IPv4Network(ip)
            
            # set hosts to our network scan response
            hosts = scan_network(cidr)
            total_hosts = len(hosts)/2 - 2

        except ipaddress.AddressValueError as err:
            # log the error
            msg = "The IP Address {} CIDR range is invalid: {}".format(str(ip), str(err))
            flash(msg, category="danger")
            return redirect(url_for("nmap"))    

    return render_template(
        "nmap.html",
        ip=ip,
        hosts=hosts,
        total_hosts=int(total_hosts),
        scan_type=scan_type,
        today=get_date()
    )


@app.route("/qradar", methods=["GET", "POST"])
def qradar():
    """
    endpoint for qradar health check data
    :param none
    :return template
    """
    security_endpoint = "/health_data_-_security_data_count.json"
    top_offenses_endpoint = "/health_data_-_top_offenses.json"
    top_rules_endpoint = "/health_data_-_top_rules.json"
    security_data, top_offenses, top_rules = None, None, None

    try:
        security_data = call_qradar_api(security_endpoint)        
        top_offenses = call_qradar_api(top_offenses_endpoint)
        top_rules = call_qradar_api(top_rules_endpoint)   

    except Exception as err:
        msg = "Unable to contact the QRadar API server for health data: {}".format(str(err))
        flash(msg, category="danger")
        return redirect(url_for("index"))

    return render_template(
        "qradar.html",
        today=get_date(),
        security_data=security_data,
        top_offenses=top_offenses,
        top_rules=top_rules
    )


def get_date():
    return datetime.now().strftime("%c")


def call_qradar_api(endpoint):
    """ 
    Base REST API function
    :param endpoint
    :return json obj
    """
    resp = None

    if not isinstance(endpoint, str):
        endpoint = str(endpoint)
    
    try:
        r = requests.request(
            "GET",
            BASE_URL + endpoint,
            headers=hdrs
        )

        if r.status_code == 200:
            resp = r.json()
        else:
            resp = "HTTP returned status code: {}".format(str(r.status_code))
    
    except requests.HTTPError as http_err:
        resp = "HTTP Error: {}".format(str(http_err))
    
    return resp



def scan_network(cidr):
    """
    Scan the CIDR using subprocess check_output
    :param CIDR network
    :return hosts <list>
    """
    hosts = None
    network = str(cidr)

    try:
        data = subprocess.check_output(
            ["/usr/local/bin/nmap", "-sP", "-n", network],
            stderr=subprocess.STDOUT
        )
        # set hosts to a list split on new line
        hosts = data.split("\n")
    
    except subprocess.CalledProcessError as err:
        print(str(err))

    return hosts
