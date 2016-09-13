#!/usr/bin/env python
import abc
import StringIO
from ansible import errors
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser
from InventoryFilter import InventoryFilter


class AWSInventory(InventoryFilter):
    def get_host_ips(self, topo):
        host_public_ips = []
        for group in topo['aws_ec2_res']:
            for instance in group['instances']:
                host_public_ips.append(str(instance['public_dns_name']))
        return host_public_ips

    def get_inventory(self, topo, layout):
        inventory = ConfigParser(allow_no_value=True)
        no_of_groups = len(topo['aws_ec2_res'])
        layout_hosts = self.get_layout_hosts(layout)
        inven_hosts = self.get_host_ips(topo)
        # adding sections to respective host groups
        host_groups = self.get_layout_host_groups(layout)
        inventory = self.add_sections(inventory, host_groups)
        # set children for each host group
        inventory = self.set_children(inventory, layout)
        # set vars for each host group
        inventory = self.set_vars(inventory, layout)
        # add ip addresses to each host
        inventory = self.add_ips_to_groups(inventory, inven_hosts, layout)
        inventory = self.add_common_vars(inventory, host_groups, layout)
        output = StringIO.StringIO()
        inventory.write(output)
        return output.getvalue()