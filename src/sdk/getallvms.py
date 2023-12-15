#####################################################################################
############## TP sur ESXI                            ###############################
############## Virtualisation                         ###############################
############## ANZIE SEVERIN BRADLEY                  ###############################
############## Lister toutes les vm                   ###############################
############## Modifié depuis Written by Michael Rice ###############################
#####################################################################################
import re
from pyVmomi import vmodl, vim
from sdk.tools import cli, service_instance


def print_vm_info(virtual_machine):
    """
    Print information for a particular virtual machine or recurse into a
    folder with depth protection
    """
    summary = virtual_machine.summary
    print("Name       : ", summary.config.name)
    print("Template   : ", summary.config.template)
    print("Path       : ", summary.config.vmPathName)
    print("Guest      : ", summary.config.guestFullName)
    print("Instance UUID : ", summary.config.instanceUuid)
    print("Bios UUID     : ", summary.config.uuid)
    annotation = summary.config.annotation
    if annotation:
        print("Annotation : ", annotation)
    print("State      : ", summary.runtime.powerState)
    if summary.guest is not None:
        ip_address = summary.guest.ipAddress
        tools_version = summary.guest.toolsStatus
        if tools_version is not None:
            print("VMware-tools: ", tools_version)
        else:
            print("Vmware-tools: None")
        if ip_address:
            print("IP         : ", ip_address)
        else:
            print("IP         : None")
    if summary.runtime.question is not None:
        print("Question  : ", summary.runtime.question.text)
    print("")


def main(args):
    si = service_instance.connect(args)

    try:
        content = si.RetrieveContent()

        container = content.rootFolder  # starting point to look into
        view_type = [vim.VirtualMachine]  # object types to look for
        recursive = True  # whether we should look into it recursively
        container_view = content.viewManager.CreateContainerView(
            container, view_type, recursive)

        children = container_view.view
        if args.find is not None:
            pat = re.compile(args.find, re.IGNORECASE)
        for child in children:
            if args.find is None:
                print_vm_info(child)
            else:
                if pat.search(child.summary.config.name) is not None:
                    print_vm_info(child)

    except vmodl.MethodFault as error:
        print("Caught vmodl fault : " + error.msg)
        return -1

    return 0


if __name__ == "__main__":
    main()
