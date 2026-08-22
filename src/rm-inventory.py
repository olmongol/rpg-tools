#!/usr/bin/env python3
r'''
Inventory tool - neu modularisiert
Logik -> rpgtoolbox/shop_logic, rpgtoolbox/enchant_core, rpgtoolbox/edit_inv_core
GUI (InventoryWin, shopWin, enchantItem, editinventory) -> gui/modules/inventory_gui.py
'''

from rpgtoolbox import logbox as log
from rpgtoolbox.confbox import chkCfg
from gui.modules.inventory_gui import InventoryWin


if __name__ == '__main__':
    mycnf = chkCfg()
    logger = log.createLogger('inventory', 'info', '4 MB', 1,
                              logpath=mycnf.cnfparam["logpath"],
                              logfile='rm-inventory.log')
    logger.debug('Open inventory window')
    win = InventoryWin()
