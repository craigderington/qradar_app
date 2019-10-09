from app import db
from datetime import datetime, timedelta
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Boolean, func
from sqlalchemy.orm import backref, relationship, validates


class Message(db.Model):
    """
    Message Class
    :return message <obj>
    """
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    message_type = Column(String(64), nullable=False)
    message_text = Column(String(255), nullable=False)
    message_datetime = Column(DateTime, nullable=False, default=datetime.now)
    sender = Column(String(64), nullable=False)
    sent_date = Column(DateTime, nullable=False, default=datetime.now)
    message_read = Column(Boolean, default=False)

    def __repr__(self):
        if self.id and self.message_type:
            return "{}-{}".format(self.id, self.message_type)
    
    def get_message(self):
        return "{}".format(
            self.message_text
        )


class ScanType(db.Model):
    """
    ScanType Class
    :return scantype <obj>
    """
    __tablename__ = "scantypes"
    id = Column(Integer, primary_key=True)
    scan_type_name = Column(String(64), nullable=False)
    scan_type_cmd = Column(String(64), nullable=False)
    scan_type_active = Column(Boolean, default=True)

    def __repr__(self):
        if self.id and self.scan_type_name:
             return "{}".format(
                 self.scan_type_name
             )


class Scan(db.Model):
    """
    Scan Class
    :return scan <obj>
    """
    __tablename__ = "scans"
    id = Column(Integer, primary_key=True)
    scan_date = Column(DateTime, nullable=False, default=datetime.now())
    scan_type_id = Column(Integer, ForeignKey("scantypes.id"), nullable=False)
    scan_type = relationship("ScanType")
    scan_network = Column(String(64), nullable=False)
    scan_cidr = Column(Integer, default=32)
    scan_result = Column(String(64), nullable=False, default="Incomplete")
    scan_total_hosts = Column(Integer, default=0)

    def __repr__(self):
        if self.id and self.scan_date and self.scan_type:
            return "{} {} {}".format(
                self.id,
                self.scan_date.strftime("%c"),
                self.scan_type
            )
        return self.id


class ScanResults(db.Model):
    """
    Scan Results Class
    :return scanresults <obj>
    """
    __tablename__ = "scanresults"
    id = Column(Integer, primary_key=True)
    scan_id = Column(Integer, ForeignKey("scans.id"))
    scan_host = Column(String(64), nullable=False)
    scan_host_latency = Column(String(64), nullable=False, default="0.00 ms")
    scan_host_status = Column(String(256), nullable=False, default="down")
    scan_host_port = Column(String(64), nullable=True)
    scan_host_service = Column(String(64), nullable=True)
    scan_host_state = Column(String(64), nullable=True)

    def __repr__(self):
        if self.scan_id and self.scan_host:
            return "{} {}".format(
                self.id,
                self.can_host
            )
