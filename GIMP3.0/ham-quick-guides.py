#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# ham-quick-guides.py
#
# A GIMP 3.0+ plugin to quickly add guides for splitting the canvas,
# creating center lines, and drawing border guides.
#
# Original GIMP 2.0 plugin by hamsolo474.
# GIMP 3.0+ migration by Claude Code.
#
# As of GIMP 3.0.6, this plugin needs to be in a directory with the same name as the file. 
# Example: %APPDATA%\GIMP\3.0\plug-ins\ham-quick-guides\ham-quick-guides.py
# 
# You must delete your plugin cache when updating this file. (%APPDATA%\GIMP\3.0\pluginrc)

import sys
import gi

# Require GIMP 3.0
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp, GObject, GLib
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi


def run_quick_guides(procedure, run_mode, image, drawables, config, data):
    """
    The main function that runs the plugin logic.
    """
    # Handle interactive mode - show dialog to get parameters
    if run_mode == Gimp.RunMode.INTERACTIVE:
        GimpUi.init('python-fu-ham-quick-guides')
        dialog = GimpUi.ProcedureDialog(procedure=procedure, config=config)
        dialog.fill(None)

        if not dialog.run():
            dialog.destroy()
            return procedure.new_return_values(Gimp.PDBStatusType.CANCEL, GLib.Error())

        dialog.destroy()

    # Get properties
    h_split = config.get_property("h-split")
    v_split = config.get_property("v-split")
    make_centre = config.get_property("make-centre")
    draw_borders = config.get_property("draw-borders")

    if not image:
        return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, GLib.Error())

    image_width = image.get_width()
    image_height = image.get_height()

    # Start a single undo group for all guide additions
    image.undo_group_start()

    try:
        # Add vertical guides
        if v_split > 1:
            for i in range(v_split - 1):
                guide_pos = int((image_width / v_split) * (i + 1))
                image.add_vguide(guide_pos)

        # Add horizontal guides
        if h_split > 1:
            for i in range(h_split - 1):
                guide_pos = int((image_height / h_split) * (i + 1))
                image.add_hguide(guide_pos)

        # Add center guides
        if make_centre:
            image.add_vguide(int(image_width / 2))
            image.add_hguide(int(image_height / 2))

        # Add border guides
        if draw_borders:
            image.add_vguide(0)
            image.add_hguide(0)
            image.add_vguide(image_width)
            image.add_hguide(image_height)

    except Exception:
        image.undo_group_end()
        return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR, GLib.Error())

    image.undo_group_end()
    return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


class HamQuickGuides(Gimp.PlugIn):
    """
    GIMP 3.0+ Plug-In class for Quick Guides.
    """

    ## Gimp.PlugIn virtual methods ##
    def do_set_i18n(self, procname):
        """
        Set up internationalization for the plugin.
        """
        return True, 'gimp30-python', None

    def do_query_procedures(self):
        """
        Tell GIMP about the procedures this plugin provides.
        """
        return ['python-fu-ham-quick-guides']

    def do_create_procedure(self, name):
        """
        Define the procedure for GIMP.
        """
        procedure = Gimp.ImageProcedure.new(
            self,
            name,
            Gimp.PDBProcType.PLUGIN,
            run_quick_guides,
            None
        )

        procedure.set_image_types("*")
        procedure.set_sensitivity_mask(Gimp.ProcedureSensitivityMask.ALWAYS)
        procedure.set_menu_label("Quick Guides...")
        procedure.add_menu_path("<Image>/Image/Guides")

        procedure.set_documentation(
            "Create guides for rule of thirds/fourths etc..",
            "Quickly adds horizontal and vertical guides to the image based "
            "on a specified number of splits. "
            "Can also add center and border guides.",
            name
        )
        procedure.set_attribution(
            "hamsolo474, Claude Code (Migration)",
            "hamsolo474, Claude Code (Migration)",
            "2022, 2025"
        )

        procedure.add_int_argument(
            "h-split",
            "Horizontal Splits",
            "Number of horizontal sections to create (e.g., 3 for thirds)",
            1, 100, 3,
            GObject.ParamFlags.READWRITE
        )

        procedure.add_int_argument(
            "v-split",
            "Vertical Splits",
            "Number of vertical sections to create (e.g., 3 for thirds)",
            1, 100, 3,
            GObject.ParamFlags.READWRITE
        )

        procedure.add_boolean_argument(
            "make-centre",
            "Draw centered guides",
            "Add guides at the horizontal and vertical center",
            True,
            GObject.ParamFlags.READWRITE
        )

        procedure.add_boolean_argument(
            "draw-borders",
            "Draw guides on canvas borders",
            "Add guides at the 0 and max width/height of the canvas",
            False,
            GObject.ParamFlags.READWRITE
        )

        return procedure


# Register the plugin and run its main loop
Gimp.main(HamQuickGuides.__gtype__, sys.argv)
