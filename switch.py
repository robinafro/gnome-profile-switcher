#!/bin/python3

import os
import json
import sys

PROFILES_FOLDER = os.path.join(os.path.dirname(__file__), 'profiles')

def unload_extensions(except_for):
    # Get all extensions, find the ones that are not in the except_for list
    for theme_path in os.listdir(PROFILES_FOLDER):
        theme_json = json.load(open(os.path.join(PROFILES_FOLDER, theme_path)))
        extensions = theme_json.get('extensions', [])
        to_remove = []

        for extension in extensions:
            if extension not in except_for:
                to_remove.append(extension)

        for extension in to_remove:
            os.system("gnome-extensions disable " + extension)

def load_extensions(extension_names):
    unload_extensions(extension_names)
    
    for extension in extension_names:
        os.system("gnome-extensions enable " + extension)

def switch_theme(theme):
    theme_path = os.path.join(PROFILES_FOLDER, theme + ".json")

    if not os.path.exists(theme_path):
        raise ValueError(f'Theme "{theme}" not found')
    
    theme_json = json.load(open(theme_path))

    # Load theme
    theme_data = theme_json['theme']
    titlebar_data = theme_json['titlebar']
    theme_dark_or_light = "prefer-dark" if theme_data['dark'] else "prefer-light"

    os.system(f"gsettings set org.gnome.desktop.interface color-scheme {theme_dark_or_light}")
    os.system(f"gsettings set org.gnome.desktop.interface gtk-theme '{theme_data['applications']}'")
    os.system(f"gsettings set org.gnome.shell.extensions.user-theme name '{theme_data['shell']}'")
    os.system(f"gsettings set org.gnome.desktop.interface icon-theme '{theme_data['icons']}'")
    os.system(f"gsettings set org.gnome.desktop.interface cursor-theme '{theme_data['cursor']}'")

    os.system(f"gsettings set org.gnome.desktop.background picture-uri 'file://{theme_data['background']}'")

    os.system(f"gsettings set org.gnome.desktop.wm.preferences button-layout '{titlebar_data['button-layout']}'")

    # Load extensions
    load_extensions(theme_json.get('extensions', []))

def logout():
    os.system("gnome-session-quit --force")

if __name__ == "__main__":
    theme = sys.argv[1]

    switch_theme(theme)

    if len(sys.argv) < 2 or sys.argv[2] != "--no-logout":
        logout()