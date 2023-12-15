# create vm:
    python create_vm.py --host 192.168.100.91 --user root -p 'admin admin'  -nossl -v tinyVm --esx-ip localhost.localdomain --datacenter-name ha-datacenter --datastore-name datastore1

    with args:
    Namespace(host='192.168.100.91', port=443, user='root', password='admin admin', disable_ssl_verification=True, vm_name='tinyVm', datacenter_name='ha-datacenter', datastore_name='datastore1', esx_ip='localhost.localdomain')

# get all vms:
    python getallvms.py --host 192.168.100.91 --user root -p 'admin admin'  -nossl
    - response:
    --------------------------------------------
    Namespace(host='192.168.100.91', port=443, user='root', password='admin admin', disable_ssl_verification=True, find=None)
    ---------------------------------------------------------

    Name       :  tinyVm
    Template   :  False
    Path       :  [datastore1] tinyVm/tinyVm.vmx
    Guest      :  Other (32-bit)
    Instance UUID :  52cf12de-1821-f5d8-98f1-3de203b96ad9
    Bios UUID     :  564da017-c05b-d567-6483-4264bec17d11
    Annotation :  Sample
    State      :  poweredOff
    VMware-tools:  toolsNotInstalled
    IP         : None

# Destroy vm by name:
python destroy_vm.py --host 192.168.100.91 --user root -p 'admin admin'  -nossl -v tinyVm
    - response:
    --------------------------------------------
    Namespace(host='192.168.100.91', port=443, user='root', password='admin admin', disable_ssl_verification=True, uuid=None, vm_name='tinyVm', vm_ip=None, dns_name=None)
    ---------------------------------------------------------

    Found: tinyVm
    The current powerState is: poweredOff
    Destroying VM from vSphere.
    Done.

# deploy vm from ova file:
    python deploy_ova.py --host 192.168.100.91 --user root -p 'admin admin'  -nossl --ova-path C:/Users/bradley/Documents/5GI/Cloud/Project/esx/src/resources/ova/yVM.ova
    -response:
    --------------------------------------------
    Namespace(host='192.168.100.91', port=443, user='root', password='admin admin', disable_ssl_verification=True, ova_path='C:/Users/bradley/Documents/5GI/Cloud/Project/esx/src/resources/ova/yVM.ova', datacenter_name=None, resource_pool=None, datastore_name=None)
    ---------------------------------------------------------

    Waiting for lease to be ready...
    Starting deploy...
    Finished deploy successfully.
    Progress: 99%