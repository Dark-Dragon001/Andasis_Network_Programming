import csv
import time
import pysnmp
from pysnmp.hlapi import *

class DeviceInfo:
    def __init__(self, ip_address, snmp_community, oids):
        self.ip_address = ip_address
        self.snmp_community = snmp_community
        self.oids = oids

class DeviceMetrics:
    def __init__(self, device_info):
        self.device_info = device_info
        self.metrics = {}

    def collect_metrics(self):
        for oid in self.device_info.oids:
            errorIndication, errorStatus, errorIndex, varBinds = next(
                getCmd(SnmpEngine(),
                       CommunityData(self.device_info.snmp_community),
                       UdpTransportTarget((self.device_info.ip_address, 161)),
                       ContextData(),
                       ObjectType(ObjectIdentity(oid)))
            )
            if errorIndication:
                raise Exception(errorIndication)
            elif errorStatus:
                raise Exception("Error: %s at %s" % (errorStatus.prettyPrint(), errorIndex))
            else:
                for varBind in varBinds:
                    self.metrics[str(varBind[0])] = str(varBind[1])

    def save_metrics_to_csv(self, csv_file):
        with open(csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([time.time()] + list(self.metrics.values()))

def main():
    device_info_table = {
        "device1": DeviceInfo("192.168.1.1", "public", ["1.3.6.1.2.1.1.5.0", "1.3.6.1.2.1.2.2.1.10.1"])
        # Add more devices with their respective IP addresses, SNMP communities, and OIDs
    }

    while True:
        for device_name, device_info in device_info_table.items():
            device_metrics = DeviceMetrics(device_info)
            device_metrics.collect_metrics()
            device_metrics.save_metrics_to_csv(f"{device_name}_metrics.csv")
        
        time.sleep(60)  # Wait for 1 minute before collecting metrics again

if __name__ == "__main__":
    main()
