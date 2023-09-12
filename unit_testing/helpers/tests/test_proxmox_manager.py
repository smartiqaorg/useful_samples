from unittest.mock import MagicMock, patch
import pytest
from assertpy import assert_that
import time

from helpers.ProxmoxManager import ProxmoxManager
from helpers.api.ProxmoxAPI import ProxmoxAPI


@pytest.fixture
def t_proxmox_manager():
    t_proxmox_manager = ProxmoxManager('token')
    t_proxmox_manager.api = MagicMock(ProxmoxAPI)
    return t_proxmox_manager


# region 1. Test self._get_free_id()
vm_config = {
    'scsihw': 'virtio-scsi-pci',
    'ostype': 'other',
    'smbios1': 'uuid=63cdab3a-cbfe-4f77-942c-dacdcf0420e2',
    'sockets': 4,
    'net0': 'e1000=F2:4A:26:72:CB:C3,bridge=vmbr0',
    'memory': 8192,
    'digest': 'afec73da6f2e171ff88d5f792ca07f38c3a55cb6',
    'boot': 'order=sata0;ide2;net0',
    'ide2': 'none,media=cdrom',
    'name': 'test-winserver22-x64-192.168.23.250',
    'vmgenid': '0d93f94b-d30f-4ac4-bbe1-b706d669f477',
    'numa': 0,
    'sata0': 'nvme:vm-2213-disk-0,size=70G',
    'cores': 4}


@pytest.mark.parametrize("start_id,get_config_value,expected_result",
                         [(1200, [None], 2200),  # id is found at first attempt
                          (1200, [vm_config, None], 3200)])  # id is found at second attempt
def test_get_free_id_success(t_proxmox_manager, start_id, get_config_value, expected_result):
    t_proxmox_manager.api.get_config.side_effect = get_config_value
    free_id = t_proxmox_manager._get_free_id(start_id, t_proxmox_manager.node)
    assert_that(expected_result).is_equal_to(free_id)


def test_get_free_id_fail(t_proxmox_manager):
    t_proxmox_manager.api.get_config.return_value = vm_config
    with pytest.raises(RuntimeError):
        t_proxmox_manager._get_free_id(1200, t_proxmox_manager.node)
# endregion


# region 2. Test self.clone_vm_and_power_on()
@patch.object(target=time, attribute='sleep')
def test_clone_vm_and_power_on_basic(p_sleep, t_proxmox_manager):
    expected_vm_id = 2200
    expected_vm_name = 'test_win10-x64'
    t_proxmox_manager._get_free_id = MagicMock()
    t_proxmox_manager._get_free_id.return_value = expected_vm_id
    proxmox_vm = t_proxmox_manager.clone_vm_and_power_on(template_vm_id=1200,
                                                         template_vm_name=expected_vm_name)
    t_proxmox_manager.api.vm_power_on.assert_called_once()
    t_proxmox_manager.api.vm_power_off.assert_not_called()
    t_proxmox_manager.api.vm_configure_network.assert_not_called()
    assert_that(proxmox_vm.name).is_equal_to(expected_vm_name)
    assert_that(proxmox_vm.id).is_equal_to(expected_vm_id)
    assert_that(proxmox_vm.node).is_equal_to(t_proxmox_manager.node)


@patch.object(target=time, attribute='sleep')
def test_clone_vm_and_power_on_with_network_configuration(p_sleep, t_proxmox_manager):
    t_proxmox_manager._get_free_id = MagicMock()
    t_proxmox_manager._get_free_id.return_value = 2200
    t_proxmox_manager.api.get_config.return_value = {}
    t_proxmox_manager.clone_vm_and_power_on(template_vm_id=1200,
                                            template_vm_name='test_win10-x64',
                                            network_configuration=True)
    t_proxmox_manager.api.vm_configure_network.assert_called_once()
    t_proxmox_manager.api.vm_power_off.assert_not_called()


@patch.object(target=time, attribute='sleep')
def test_clone_vm_and_power_on_with_additional_reset(p_sleep, t_proxmox_manager):
    t_proxmox_manager._get_free_id = MagicMock()
    t_proxmox_manager._get_free_id.return_value = 2200
    t_proxmox_manager.clone_vm_and_power_on(template_vm_id=1200,
                                            template_vm_name='test_win10-x64',
                                            additional_reset=True)
    t_proxmox_manager.api.vm_power_off.assert_called_once()
    t_proxmox_manager.api.vm_configure_network.assert_not_called()
# endregion
