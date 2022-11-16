from azure.mgmt.resource import ResourceManagementClient
from azure.identity import AzureCliCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
import os


credential = AzureCliCredential()

subscription_id = "092aa3b0-d11f-43fc-b8aa-d8f5bc406384"

resource_client = ResourceManagementClient(credential, subscription_id)

rg_name = "VMs"
location = "uksouth"

VNET_NAME = "VMs-vnet"
SUBNET_NAME = "/subscriptions/092aa3b0-d11f-43fc-b8aa-d8f5bc406384/resourceGroups/VMs/providers/Microsoft.Network/virtualNetworks/VMs-vnet/subnets/default"
IP_NAME = "newIP"
NIC_NAME = "newNetwork"

network_client = NetworkManagementClient(credential, subscription_id)

poller = network_client.public_ip_addresses.begin_create_or_update("VMs",
    IP_NAME,
    {
        "location": "uksouth",
        "sku": {
            "name": "Basic"
        },
        "public_ip_allocation_method": "Static",
        "public_ip_address_version": "IPV4"

    }
)

ip_address_result = poller.result()

print(f"Provisioned public IP address {ip_address_result.name} with address {ip_address_result.ip_address}")

poller = network_client.network_interfaces.begin_create_or_update("VMs",
    NIC_NAME,
    {
        "location" : "uksouth",
        "ip_configurations" : [{
            "name": "ipconfig1",
            "subnet" : {"id": "/subscriptions/092aa3b0-d11f-43fc-b8aa-d8f5bc406384/resourceGroups/VMs/providers/Microsoft.Network/virtualNetworks/VMs-vnet/subnets/default"},
            "public_ip_address": {"id": "/subscriptions/092aa3b0-d11f-43fc-b8aa-d8f5bc406384/resourceGroups/VMs/providers/Microsoft.Network/publicIPAddresses/newIP" }
        }]
    }
)

nic_result = poller.result()

print(f"Provisioned network interface client {nic_result.name}")

compute_client = ComputeManagementClient(credential, subscription_id)

VM_NAME = "newVM"
USERNAME = "rezix"

print(f"Provisioning virtual machine {VM_NAME}; this operation might take a few minutes.")

poller = compute_client.virtual_machines.begin_create_or_update("VMs", VM_NAME,
    {
        "id": "/subscriptions/092aa3b0-d11f-43fc-b8aa-d8f5bc406384/resourceGroups/VMs/providers/Microsoft.Compute/virtualMachines/myVM",
        "type": "Microsoft.Compute/virtualMachines",
        "properties": {
            "osProfile": {
                "adminUsername": "rezix",
                "secrets": [

                ],
                "computerName": "myVM",
                "linuxConfiguration": {
                    "disablePasswordAuthentication": True
                }
            },
            "networkProfile": {
                "networkInterfaces": [
                    {
                        "id": "/subscriptions/092aa3b0-d11f-43fc-b8aa-d8f5bc406384/resourceGroups/VMs/providers/Microsoft.Network/networkInterfaces/newNetwork",
                        "properties": {
                            "primary": True
                        }
                    }
                ]
            },
            "storageProfile": {
                "imageReference": {
                    "sku": "16.04-LTS",
                    "publisher": "Canonical",
                    "version": "latest",
                    "offer": "UbuntuServer"
                },
                "dataDisks": [

                ]
            },
            "hardwareProfile": {
                "vmSize": "Standard_D1_v2"
            },
            "provisioningState": "Creating"
        },
        "name": "newVM",
        "location": "uksouth"
    }
)

vm_result = poller.result()

print(f"Provisioned virtual machine {vm_result.name}")

