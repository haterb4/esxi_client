from sdk.tools import cli, service_instance, tasks, pchelper
from pyVmomi import vim


def main(args):
    si = service_instance.connect(args)

    VM = None
    if args.uuid:
        VM = si.content.searchIndex.FindByUuid(None, args.uuid, True, True)
    elif args.dns_name:
        VM = si.content.searchIndex.FindByDnsName(None, args.dns_name, True)
    elif args.vm_ip:
        VM = si.content.searchIndex.FindByIp(None, args.vm_ip, True)
    elif args.vm_name:
        content = si.RetrieveContent()
        VM = pchelper.get_obj(content, [vim.VirtualMachine], args.vm_name)

    if VM is None:
        raise SystemExit("Unable to locate VirtualMachine.")

    print("Found: {0}".format(VM.name))
    print("The current powerState is: {0}".format(VM.runtime.powerState))
    TASK = VM.ResetVM_Task()
    tasks.wait_for_tasks(si, [TASK])
    print("its done.")
