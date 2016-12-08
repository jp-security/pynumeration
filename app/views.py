from flask import render_template, request, redirect
from app import app, models
import json

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',
                            title="Home")

@app.route('/raw/hosts')
def hosts_json():
    all_hosts = models.Hosts.query.all()

    allHostsDataset = []

    for host in all_hosts:
        hostInfo = {'ip': host.host_ip, 'hostname': host.host_name, 'openports': host.ports_open}
        allHostsDataset.append(hostInfo)

    return json.dumps(allHostsDataset)

@app.route('/raw/<hostinfo>')
def host_json(hostinfo):
    host_information = models.HostInformation.query.filter_by(host=hostinfo).all()

    allHostInfo = []

    for host in host_information:
        hostInfo = {'ip': host.host, 'portstate': host.port_state, 'portnumber': host.port_number,
        'portname': host.port_name, 'product': host.product_used, 'version': host.product_version}
        allHostInfo.append(hostInfo)

    return json.dumps(allHostInfo)

@app.route('/<host_ip>')
def host_ip(host_ip):
    host_information = models.HostInformation.query.filter_by(host=host_ip).all()


    return render_template('hostinformation.html',
                            title='Host Information')
