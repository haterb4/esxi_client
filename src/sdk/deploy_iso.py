from pyVmomi import vim
from pyVim.task import WaitForTask
from sdk.tools import cli, service_instance




def get_dc(si, name):
    for datacenter in si.content.rootFolder.childEntity:
        if datacenter.name == name:
            return datacenter
    raise Exception('Failed to find datacenter named %s' % name)


# Returns the first cdrom if any, else None.
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


def find_device(vm, device_type):
    result = []
    for dev in vm.config.hardware.device:
        if isinstance(dev, device_type):
            result.append(dev)
    return result


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


def main(args):
    # parser = cli.Parser()
    # parser.add_required_arguments(cli.Argument.VM_NAME, cli.Argument.ISO)
    # parser.add_optional_arguments(cli.Argument.DATACENTER_NAME)
    # args = parser.get_args()
    print("starting")
    si = service_instance.connect(args)

    if args.datacenter_name:
        datacenter = get_dc(si, args.datacenter_name)
    else:
        datacenter = si.content.rootFolder.childEntity[0]

    vm = si.content.searchIndex.FindChild(datacenter.vmFolder, args.vm_name)
    if vm is None:
        raise Exception('Failed to find VM %s in datacenter %s' %
                        (args.vm_name, datacenter.name))

    controller = find_free_ide_controller(vm)
    if controller is None:
        raise Exception('Failed to find a free slot on the IDE controller')

    cdrom = None

    print("Looking for physical CD-ROM")
    cdrom_lun = get_physical_cdrom(vm.runtime.host)

    if cdrom_lun is not None:
        backing = vim.vm.device.VirtualCdrom.AtapiBackingInfo()
        backing.deviceName = cdrom_lun.deviceName
        device_spec = vim.vm.device.VirtualDeviceSpec()
        device_spec.device = new_cdrom_spec(controller.key, backing)
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

    print("Mounting ISO")
    cdrom_operation = vim.vm.device.VirtualDeviceSpec.Operation
    iso = args.iso
    if iso is not None:
        device_spec = vim.vm.device.VirtualDeviceSpec()
        if cdrom is None:  # add a cdrom
            backing = vim.vm.device.VirtualCdrom.IsoBackingInfo(fileName=iso)
            cdrom = new_cdrom_spec(controller.key, backing)
            device_spec.operation = cdrom_operation.add
        else:  # edit an existing cdrom
            backing = vim.vm.device.VirtualCdrom.IsoBackingInfo(fileName=iso)
            cdrom.backing = backing
            device_spec.operation = cdrom_operation.edit
        device_spec.device = cdrom
        config_spec = vim.vm.ConfigSpec(deviceChange=[device_spec])
        WaitForTask(vm.Reconfigure(config_spec))

        cdroms = find_device(vm, vim.vm.device.VirtualCdrom)
        # TODO isinstance(x.backing, type(backing))
        cdrom = next(
            filter(
                lambda x: type(x.backing) == type(backing) and x.backing.fileName == iso,
                cdroms
            )
        )
        print("Mounting ISO OK")
    else:
        print('Skipping ISO test as no iso provided.')

    if cdrom is not None:  # Remove it
        print("Remove ISO")
        device_spec = vim.vm.device.VirtualDeviceSpec()
        device_spec.device = cdrom
        device_spec.operation = cdrom_operation.remove
        config_spec = vim.vm.ConfigSpec(deviceChange=[device_spec])
        WaitForTask(vm.Reconfigure(config_spec))
        print("Remove ISO OK")
    else:
        print("Nothing happened")


if __name__ == '__main__':
    main()
