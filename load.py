# -*- coding: utf-8 -*-

import os
import Tkinter as tk
import ttk
import myNotebook as nb
from config import config
import sys
import plug
import heading
import version
import waypoints
import rate
from sys import platform
from util import GridHelper, debug, error
from ttkHyperlinkLabel import HyperlinkLabel
from waypoints import Waypoints

this = sys.modules[__name__]	# For holding module globals

this.target = None
this.rate = rate.Rate()

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

def format_distance(distance_km):
    if distance_km < 1.0:
        return "{:3.0f}m".format(distance_km*1000)
    else:
        return "{:3.1f}km".format(distance_km)

def update_remaining_time():
    t = this.rate.remaining_secs()
    if not t:
        this.remaining_time.set('Unknown')
    else:
        if t < 60: 
            this.remaining_time.set("{} seconds".format(t))
        elif t < 3600:
            this.remaining_time.set("{} mins {} secs".format(t//60, t % 60, t))
        else:
            this.remaining_time.set("{}:{}:{} H:M:S".format(t//3600, (t % 3600)// 60, t % 60))

def dashboard_entry(cmdr, is_beta, entry):
    if 'Latitude' in entry and 'Longitude' in entry:
        if hasattr(this, 'target'):
            if 'lat' in this.target:
                info = heading.target_info( 
                    ( entry['Latitude'], entry['Longitude']), 
                    ( this.target['lat'], this.target['lon']),
                    height = entry['Altitude'],
                    radius = 605) # Ick - hard-coded for Kumay for now

            this.rate.progress(info['distance'], time.time())
            this.current_distance.set(format_distance(info['distance']))
            this.target_heading.set( info['heading'] )
            update_remaining_time()

def waypoint_change(a, b, c):
    wp = this.waypoints.info(this.target_waypoint.get())
    if wp:
        this.target = wp
        this.selected_waypoint = this.target_waypoint.get()
        config.set("Kumay3305.target_waypoint", this.selected_waypoint)
        this.current_distance.set('---')
        this.rate = rate.Rate()

def plugin_app(parent):
    """
    Returns a frame containing the status fields we want to display to the 
    app in the main window
    """
    h = GridHelper()
    this.status_frame = tk.Frame(parent)

    vcheck = version.Version("kumay3305", "https://raw.githubusercontent.com/factabulous/kumay3305/master/VERSION.md")
    if vcheck.is_new_version():
        HyperlinkLabel(this.status_frame, url="https://github.com/factabulous/kumay3305", text="New Kumay3305 version available! Click here").grid(row=h.row(), column=h.col(4), columnspan=4)
        h.newrow()

    tk.Label(this.status_frame, text="Waypoint").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.target_waypoint = tk.StringVar()
    this.target_waypoint.set(this.selected_waypoint)
    this.target_waypoint.trace("w", waypoint_change)
    w = tk.OptionMenu(this.status_frame, this.target_waypoint, *this.waypoints.names())
    w['highlightthickness'] = 0
    w['borderwidth'] = 0
    w.grid(row=h.row(), column=h.col(3), columnspan=3, sticky=tk.W)
    h.newrow()
    # Target Heading
    tk.Label(this.status_frame, text="Heading").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.target_heading = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.target_heading).grid(row=h.row(), column=h.col(), sticky=tk.W)
    # Distance
    tk.Label(this.status_frame, text="Distance").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.current_distance = tk.StringVar()
    tk.Label(this.status_frame, textvariable=this.current_distance).grid(row=h.row(), column=h.col(), sticky = tk.W)
    h.newrow()
    tk.Label(this.status_frame, text="Remaining Time").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.remaining_time = tk.StringVar()
    tk.Label(this.status_frame, textvariable=this.remaining_time).grid(row=h.row(), column=h.col(), sticky = tk.W)

    return this.status_frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
    """
    We do nothing with the journal - I guess we could track material 
    usage and warn when low on synth mats?
    """
    pass 

