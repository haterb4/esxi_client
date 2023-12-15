'''
Copyright 2014-2015 Reubenur Rahman
All Rights Reserved
@author: reuben.13@gmail.com
'''

import atexit
import time

from pyVmomi import vim, vmodl
from pyVim import connect
from pyVim.connect import Disconnect
from sdk.tools import cli, service_instance
from sdk.create_vm import create_vm as create_new_vm
from pyVim.task import WaitForTask

def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj

def get_physical_cdrom(host):
    for lun in host.configManager.storageSystem.storageDeviceInfo.scsiLun:
        if lun.lunType == 'cdrom':
            return lun
    return None

def find_free_ide_controller(vm):
    for dev in vm.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualIDEController):
            # If there are less than 2 devices attached, we can use it.
            if len(dev.device) < 2:
                return dev
    return None

def new_cdrom_spec(controller_key, backing):
    connectable = vim.vm.device.VirtualDevice.ConnectInfo()
    connectable.allowGuestControl = True
    connectable.startConnected = True

    cdrom = vim.vm.device.VirtualCdrom()
    cdrom.controllerKey = controller_key
    cdrom.key = -1
    cdrom.connectable = connectable
    cdrom.backing = backing
    return cdrom

def wait_for_task(task, actionName='job', hideResult=False):
    """
    Waits and provides updates on a vSphere task
    """

    while task.info.state == vim.TaskInfo.State.running:
        time.sleep(2)

    if task.info.state == vim.TaskInfo.State.success:
        if task.info.result is not None and not hideResult:
            out = '%s completed successfully, result: %s' % (actionName, task.info.result)
            print(out)
        else:
            out = '%s completed successfully.' % actionName
            print(out)
    else:
        out = '%s did not complete successfully: %s' % (actionName, task.info.error)
        raise task.info.error
        print(out)

    return task.info.result

def find_device(vm, device_type):
    result = []
    for dev in vm.config.hardware.device:
        if isinstance(dev, device_type):
            result.append(dev)
    return result

def main(args):

    try:
        si = None
        try:
            print("Trying to connect to VCENTER SERVER . . .")
            si = service_instance.connect(args)
        except IOError:
            atexit.register(Disconnect, si)

        print("Connected to VCENTER SERVER !")

        #creating empty cd to mount iso
        create_new_vm(si, args.vm_name, args.datacenter_name, args.esx_ip, args.datastore_name)
        content = si.RetrieveContent()

        vm_name = args.vm_name
        vm = get_obj(content, [vim.VirtualMachine], vm_name)

        controller = find_free_ide_controller(vm)
        if controller is None:
            raise Exception('Failed to find a free slot on the IDE controller')

        cdrom = None
        cdrom_lun = get_physical_cdrom(vm.runtime.host)

        print("physical CD-ROM device test")
        if cdrom_lun is not None:
            backing = vim.vm.device.VirtualCdrom.AtapiBackingInfo()
            backing.deviceName = cdrom_lun.deviceName
            device_spec = vim.vm.device.VirtualDeviceSpec()
            print("creating CD-ROM")
            device_spec.device = new_cdrom_spec(controller.key, backing)
            print("created")
            device_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
            config_spec = vim.vm.ConfigSpec(deviceChange=[device_spec])
            WaitForTask(vm.Reconfigure(config_spec))

            cdroms = find_device(vm, vim.vm.device.VirtualCdrom)
            # TODO isinstance(x.backing, type(backing))
            cdrom = next(
                filter(
                    lambda x: type(x.backing) == type(backing) and  x.backing.deviceName == cdrom_lun.deviceName,
                    cdroms
                )
            )
            print("CD-ROM OK")
        else:
            print('Skipping physical CD-Rom test as no device present.')
        
        print("Attaching iso to CD drive of ", vm_name)
        cdspec = None
        for device in vm.config.hardware.device:
            if isinstance(device, vim.vm.device.VirtualCdrom):
                cdspec = vim.vm.device.VirtualDeviceSpec()
                cdspec.device = device
                cdspec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit

                cdspec.device.backing = vim.vm.device.VirtualCdrom.IsoBackingInfo()
                for datastore in vm.datastore:
                    cdspec.device.backing.datastore = datastore
                    break
                cdspec.device.backing.fileName = args.iso_file
                cdspec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
                cdspec.device.connectable.startConnected = True
                cdspec.device.connectable.allowGuestControl = True
        vmconf = vim.vm.ConfigSpec()
        
        if cdspec:
            vmconf.deviceChange = [cdspec]
            print("Giving first priority for CDrom Device in boot order")
            vmconf.bootOptions = vim.vm.BootOptions(bootOrder=[vim.vm.BootOptions.BootableCdromDevice()])

            task = vm.ReconfigVM_Task(vmconf)

            wait_for_task(task, si)

            print(f"Successfully changed boot order priority and attached iso to the CD drive of VM {vm_name}")

            print("Power On the VM to boot from iso")
            vm.PowerOnVM_Task()

        else:
            print("No CD/DVD drive found in the VM configuration.")

    except vmodl.MethodFault as e:
        print("Caught vmodl fault: %s" % e.msg)
        return 1
    except Exception as e:
        print("Caught exception: %s" % str(e))
        return 1

# Start program
if __name__ == "__main__":
    main()
