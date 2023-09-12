import logging
import time

from requests.exceptions import HTTPError

from clones import CLONES
from helpers.ProxmoxVM import ProxmoxVM
from helpers.api.ProxmoxAPI import ProxmoxAPI
from utilities import wait_until
from constants import PROXMOX

log = logging.getLogger(__name__)


class ProxmoxManager:

    DO_NOT_DELETE_PREFIX = 'do-not-delete'
    MAX_VMS_NUMBER = 20

    def __init__(self, token, node=PROXMOX.NODE):
        self._api = ProxmoxAPI(token=token)
        self.node = node
        self.token = token

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, api):
        self._api = api

    def clone_vm_and_power_on(self, template_vm_id, template_vm_name, node=None, additional_reset=False,
                              network_configuration=False, new_vm_name=None):
        node = node or self.node

        def cloning_is_successful():
            free_vm_id = self._get_free_id(template_vm_id, node)
            try:
                self.api.vm_clone(node=node, vmid=template_vm_id,
                                  newid=free_vm_id, new_name=new_vm_name)
                return free_vm_id
            except (HTTPError, TimeoutError):
                return False

        cloned_vm_id = wait_until(condition=cloning_is_successful, description="Cloning with free id is successful",
                                  timeout=30 * 60, period=30)
        time.sleep(20)
        if network_configuration and not self.api.get_config(node, cloned_vm_id).get('net0'):
            self.api.vm_configure_network(node, cloned_vm_id)
            time.sleep(20)
        self.api.vm_power_on(node, cloned_vm_id)
        time.sleep(10)
        if additional_reset:
            self.api.vm_power_off(node, cloned_vm_id)
            time.sleep(10)
            self.api.vm_power_on(node, cloned_vm_id)
            time.sleep(30)
        return ProxmoxVM(id=cloned_vm_id, name=template_vm_name, node=node, token=self.token)

    def delete_cloned_vms(self, nodes: list, vm_ids: list = None):
        log.info('Powering off and removing vms...')
        for node in nodes:
            proxmox_vms = self._api.get_all_vms_from_node(node=node)
            proxmox_vm_ids = [int(vm['vmid']) for vm in proxmox_vms if not vm['name'].startswith(self.DO_NOT_DELETE_PREFIX)]
            self._log_info(f"{node} node vm ids: {proxmox_vm_ids}")

            # Delete only specified vm ids if they are present on current node
            if vm_ids:
                for vm_id in vm_ids:
                    if int(vm_id) in proxmox_vm_ids:
                        self._log_info(f'vm with id={vm_id} is present on {node} node - deleting...')
                        ProxmoxVM(vm_id, '', node, token=self.token).destroy()
                        self._log_info(f'vm with id={vm_id} was deleted')
            # Delete all vm ids on current node basing on CLONES
            else:
                for vm_name, vm_info in CLONES.items():
                    log.info(f'Deleting...: {vm_name}')
                    if vm_info.node == node:
                        vmid = vm_info.id

                        for _ in range(self.MAX_VMS_NUMBER):
                            vmid += 1000
                            if vmid in proxmox_vm_ids:
                                ProxmoxVM(vmid, vm_name, node, token=self.token).destroy()
        log.info('All vms were successfully removed')

    def _get_free_id(self, start_id, node, max_vms_number=MAX_VMS_NUMBER):
        self._log_info('attempting to find free vm id...')
        id = start_id
        for index in range(max_vms_number):
            id += 1000
            if not self.api.get_config(node, id, expected_error='does not exist'):
                self._log_info(f'found free id: {id}')
                return id
        raise RuntimeError(f"You exceeded VMs number limit: {max_vms_number}. Please delete unnecessary VMs and try again.")

    @staticmethod
    def compose_new_vm_name(base_name, ip, prefix):
        new_name = base_name.replace('_', '-')
        if ip:
            new_name = f"{new_name}-{ip}"
        if prefix:
            new_name = f"{ProxmoxManager.DO_NOT_DELETE_PREFIX}-{new_name}"
        return new_name

    def _log_info(self, msg):
        log.info(f'{self.__class__.__name__}: {msg}')
