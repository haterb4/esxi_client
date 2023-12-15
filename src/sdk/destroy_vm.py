#####################################################################################
############## TP sur ESXI                            ###############################
############## Virtualisation                         ###############################
############## ANZIE SEVERIN BRADLEY                  ###############################
############## Detruire une vm                        ###############################
############## Modifié depuis Written by Michael Rice ###############################
#####################################################################################

from pyVmomi import vim
from sdk.tools import cli, service_instance, tasks, pchelper


def main(args):
    si = service_instance.connect(args)

    VM = None
    if args.vm_name:
        VM = pchelper.get_obj(si.content, [vim.VirtualMachine], args.vm_name)
    elif args.uuid:
        VM = si.content.searchIndex.FindByUuid(
            None,
            args.uuid,
            True,
            False
        )
    elif args.dns_name:
        VM = si.content.searchIndex.FindByDnsName(
            None,
            args.dns_name,
            True
        )
    elif args.vm_ip:
        VM = si.content.searchIndex.FindByIp(None, args.vm_ip, True)

    if VM is None:
        raise SystemExit(
            "Unable to locate VirtualMachine. Arguments given: "
            "vm - {0} , uuid - {1} , name - {2} , ip - {3}"
            .format(
                args.vm_name,
                args.uuid,
                args.dns_name,
                args.vm_ip
            )
        )

    print("Found: {0}".format(VM.name))
    print("The current powerState is: {0}".format(VM.runtime.powerState))
    if format(VM.runtime.powerState) == "poweredOn":
        print("Attempting to power off {0}".format(VM.name))
        TASK = VM.PowerOffVM_Task()
        tasks.wait_for_tasks(si, [TASK])
        print("{0}".format(TASK.info.state))

    print("Destroying VM from vSphere.")
    TASK = VM.Destroy_Task()
    tasks.wait_for_tasks(si, [TASK])
    print("Done.")
