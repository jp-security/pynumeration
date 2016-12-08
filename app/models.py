from app import db

class Hosts(db.Model):
    __tablename__ = 'hosts'

    id = db.Column(db.Integer, primary_key=True)
    host_ip = db.Column(db.String(256))
    host_name = db.Column(db.String(256), nullable=True)
    ports_open = db.Column(db.Integer)

    def __repr__(self):
        return '<Host IP: %r | Host Name: %r | Open Ports %r' (self.host_ip, self.host_name, self.ports_open)

class HostInformation(db.Model):
    __tablename__ = 'HostInformation'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(256))

    port_state = db.Column(db.String(256))
    port_number = db.Column(db.Integer)
    port_name = db.Column(db.String(256))
    product_used = db.Column(db.String(256))
    product_version = db.Column(db.String(512))
