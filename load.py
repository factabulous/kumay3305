# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import myNotebook as nb
from config import config
import sys
import plug
import heading
import version
import waypoints
from sys import platform
from util import GridHelper, debug, error
from ttkHyperlinkLabel import HyperlinkLabel
from waypoints import Waypoints

this = sys.modules[__name__]	# For holding module globals

this.target = None

#this.debug = True if platform == 'darwin' else False
this.NO_VALUE = "---" # Used when we don't have a value for a field
this.debug_buttons = False # Set True to display buttons for debugging

window=tk.Tk()
window.withdraw()

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

this.waypoints = Waypoints(local_file("waypoints.json"))

def plugin_start():
    this.selected_waypoint = config.get("Kumay3305.target_waypoint")
    return "Kumay3305"

def plugin_stop():
    window.destroy()


def dashboard_entry(cmdr, is_beta, entry):
    if 'Latitude' in entry and 'Longitude' in entry:
        if hasattr(this, 'target'):
            info = heading.target_info( 
                ( entry['Latitude'], entry['Longitude']), 
                ( this.target['lat'], this.target['lon']),
                height = entry['Altitude'],
                radius = this.target['radius'])
            this.current_distance.set(info['distance'])
            this.target_heading.set( info['heading'] )

def waypoint_change(a, b, c):
    wp = this.waypoints.info(this.target_waypoint.get())
    if wp:
        this.target = wp
    else:
        print("[kumay3305] Failed to detect waypoint from {}".format(this.target_waypoint.get()))

def plugin_app(parent):
    """
    Returns a frame containing the status fields we want to display to the 
    app in the main window
    """
    h = GridHelper()
    this.status_frame = tk.Frame(parent)

    vcheck = version.Version("kumay3305")
    if vcheck.is_new_version():
        HyperlinkLabel(this.status_frame, url="https://github.com/factabulous/kumay3305", text="New Kumay3305 version available! Click here").grid(row=h.row(), column=h.col(4), columnspan=4)
        h.newrow()

    tk.Label(this.status_frame, text="Waypoint").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.target_waypoint = tk.StringVar()
    this.target_waypoint.set(this.selected_waypoint)
    this.target_waypoint.trace("w", waypoint_change)
    tk.OptionMenu(this.status_frame, this.target_waypoint, *this.waypoints.names()).grid(row=h.row(), column=h.col(3), columnspan=3, sticky=tk.W)
    h.newrow()
    # Target Heading
    tk.Label(this.status_frame, text="Heading").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.target_heading = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.target_heading).grid(row=h.row(), column=h.col(), sticky=tk.W)
    # Distance
    tk.Label(this.status_frame, text="Distance").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.current_distance = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.current_distance).grid(row=h.row(), column=h.col(), sticky = tk.W)

    return this.status_frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
    """
    We do nothing with the journal - I guess we could track material 
    usage and warn when low on synth mats?
    """
    pass 

