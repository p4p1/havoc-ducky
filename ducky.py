#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Sat 03 Feb 2024 06:04:14 PM CET
# ducky.py
# Description:
#  A havoc extension to generate ducky script payloads for havoc on red team
#  engagements.

import havoc, havocui
import os, json

ducky_current_dir = os.getcwd()
ducky_install_path = "/data/extensions/havoc-ducky/"

while not os.path.exists(ducky_current_dir + ducky_install_path):
    # not installed through havoc-store so prompt for the path
    ducky_current_dir = ""
    ducky_install_path = havocui.inputdialog("Install path", "Please enter your install path here for the module to work correctly:")

# Global variables
ducky_settings = {
    "bin_file_path": "demon.x64.bin",
    "server_url_bin": "http://localhost:8080/demon.x64.exe",
    "payload_folder": os.path.join(ducky_current_dir, ducky_install_path, "payloads/")
}
ducky_config_path = ducky_current_dir + ducky_install_path + "settings.json"
ducky_payload = ""
ducky_settings_pane = havocui.Widget("Ducky Settings", True)

# save the settings
def save_ducky_settings():
    global ducky_settings
    global ducky_config_path
    with open(ducky_config_path, "w") as fp:
        # save the config
        json.dump(ducky_settings, fp)

def open_ducky_list():
    print("Opening list of payloads")

# Function for settings
def change_ducky_bin_path():
    global ducky_settings
    new_path = havocui.openfiledialog("select file").decode('ascii')
    old_path = ""
    if os.path.exists(ducky_settings["bin_file_path"]):
        old_path = "<span style='color:#00ff00'>%s</span>" % ducky_settings["bin_file_path"]
    else:
        old_path = "<span style='color:#ff6347'>%s</span>" % ducky_settings["bin_file_path"]
    ducky_settings_pane.replaceLabel(old_path, "<span style='color:#ffa07a'>%s</span>" % new_path)
    ducky_settings["bin_file_path"] = new_path
def change_ducky_payload_folder():
    global ducky_settings
    new_path = havocui.openfiledialog("select file").decode('ascii')
    old_path = ""
    if os.path.exists(ducky_settings["payload_folder"]):
        old_path = "<span style='color:#00ff00'>%s</span>" % ducky_settings["payload_folder"]
    else:
        old_path = "<span style='color:#ff6347'>%s</span>" % ducky_settings["payload_folder"]
    ducky_settings_pane.replaceLabel(old_path, "<span style='color:#ffa07a'>%s</span>" % new_path)
    ducky_settings["payload_folder"] = new_path
def get_domain_ducky(url):
    global ducky_settings
    ducky_settings["server_url_bin"] = url
# Display the settings
def open_ducky_setting():
    global ducky_settings
    ducky_settings_pane.clear()
    ducky_settings_pane.addLabel("<h3 style='color:#bd93f9'>Ducky Settings:</h3>")
    ducky_settings_pane.addLabel("<span style='color:#71e0cb'>Havoc Binary Payload:</span>")
    if os.path.exists(ducky_settings["bin_file_path"]):
        ducky_settings_pane.addLabel("<span style='color:#00ff00'>%s</span>" % ducky_settings["bin_file_path"])
    else:
        ducky_settings_pane.addLabel("<span style='color:#ff6347'>%s</span>" % ducky_settings["bin_file_path"])
    ducky_settings_pane.addButton("Change", change_ducky_bin_path)
    ducky_settings_pane.addLabel("<span style='color:#71e0cb'>Server Payload Host:</span>")
    ducky_settings_pane.addLineedit(ducky_settings["server_url_bin"], get_domain_ducky)
    ducky_settings_pane.addLabel("<span style='color:#71e0cb'>Ducky Payload Folder:</span>")
    if os.path.exists(ducky_settings["payload_folder"]):
        ducky_settings_pane.addLabel("<span style='color:#00ff00'>%s</span>" % ducky_settings["payload_folder"])
    else:
        ducky_settings_pane.addLabel("<span style='color:#ff6347'>%s</span>" % ducky_settings["payload_folder"])
    ducky_settings_pane.addButton("Change", change_ducky_payload_folder)
    ducky_settings_pane.addButton("Save", save_ducky_settings)
    ducky_settings_pane.setSmallTab()

def ducky_generate():
    print("Running generate")

# Handle the settings of the tool load / save
if os.path.exists(ducky_config_path):
    # find the settings path
    with open(ducky_config_path, "r") as fp:
        # load the settings
        ducky_settings = json.load(fp)
else:
    save_ducky_settings()

havocui.createtab("Ducky", "Generate", ducky_generate, "Payload list", open_ducky_list, "Settings", open_ducky_setting)
