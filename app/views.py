from app import app
from flask import render_template, request, Response, redirect, url_for, flash
from datetime import datetime, timedelta
import subprocess
import ipaddress


@app.route("/")
@app.route("/index")
def index():
    return render_template(
        "index.html",
        today=get_date()
    )


@app.route("/nmap", methods=["GET", "POST"])
def nmap():
    """
    Endpoint for nmap scan
    :return template
    """
    total_hosts = 0
    hosts = None
    ip = None

    if request.method == "POST":
        ip = request.form["ip_network"]
        try:
            cidr = ipaddress.IPv4Network(ip)
            
            # set hosts to our network scan response
            hosts = scan_network(cidr)
            total_hosts = len(hosts)/2 - 2

        except ipaddress.AddressValueError as err:
            # log the error
            msg = "The IP Address {} CIDR range is invalid: {}".format(str(ip), str(err))
            flash(msg, category="danger")
            return redirect(url_for("index"))    

    return render_template(
        "nmap.html",
        ip=ip,
        hosts=hosts,
        total_hosts=int(total_hosts),
        today=get_date()
    )

def get_date():
    return datetime.now().strftime("%c")


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
