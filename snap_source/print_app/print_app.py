import sys

import gi

import os

gi.require_version('Gdk', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gdk, Pango, GLib, Gio, Gtk

# This would typically be its own file
MENU_XML = """
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="app-menu">
    <section>
      <item>
        <attribute name="action">win.maximize</attribute>
        <attribute name="label" translatable="yes">Maximize</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""


class AppWindow(Gtk.ApplicationWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # This will be in the windows group and have the "win" prefix
        max_action = Gio.SimpleAction.new_stateful("maximize", None,
                                                   GLib.Variant.new_boolean(False))
        max_action.connect("change-state", self.on_maximize_toggle)
        self.add_action(max_action)

        # Keep it in sync with the actual state
        self.connect("notify::is-maximized",
                     lambda obj, pspec: max_action.set_state(
                         GLib.Variant.new_boolean(obj.props.is_maximized)))

        self.set_icon_from_file(self.get_resource_path("terminal.png"))
        self.color = "Red"
        self.box = Gtk.Box(spacing=6)
        self.button = Gtk.Button(label="Print")
        self.button.connect("clicked", self.click)
        self.label = Gtk.Label()
        self.label.set_text("Print")
        self.entry = Gtk.Entry()
        self.entry.connect("activate", self.click)
        self.entry.set_placeholder_text("Print text")
        self.box.pack_start(self.button, True, True, 0)
        self.box.pack_start(self.label, True, True, 0)
        self.box.pack_start(self.entry, True, True, 0)
        self.ver_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.switch = Gtk.ToggleButton("Print: On")
        self.switch.set_active(True)
        self.switch.connect("toggled", self.on_button_toggled)
        self.add(self.ver_box)
        # a new checkbutton
        button = Gtk.CheckButton()
        #  with a label
        button.set_label("Visible")
        # connect the signal "toggled" emitted by the checkbutton
        # with the callback function toggled_cb
        button.connect("toggled", self.on_check)
        # by default, the checkbutton is active
        button.set_active(True)
        self.print_box = Gtk.Box(spacing=6)
        self.print_box.pack_start(self.switch, True, True, 0)
        self.print_box.pack_start(button, True, True, 0)
        self.ver_box.pack_start(self.box, True, True, 0)
        self.ver_box.pack_start(self.print_box, True, True, 0)

        self.hbox = Gtk.Box(spacing=6)
        self.ver_box.pack_start(self.hbox, True, True, 0)

        self.button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Red")
        self.button1.connect("toggled", self.on_radio_toggled)
        self.hbox.pack_start(self.button1, False, False, 0)

        self.button2 = Gtk.RadioButton.new_from_widget(self.button1)
        self.button2.set_label("Green")
        self.button2.connect("toggled", self.on_radio_toggled)
        self.hbox.pack_start(self.button2, False, False, 0)

        button3 = Gtk.RadioButton.new_with_mnemonic_from_widget(self.button1, "Blue")
        button3.connect("toggled", self.on_radio_toggled)
        self.hbox.pack_start(button3, False, False, 0)
        link = Gtk.LinkButton("http://www.gtk.org", "Gtk Home Page")
        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.spinbutton = Gtk.SpinButton()
        self.spinbutton.set_adjustment(adjustment)
        self.spin_box = Gtk.Box(spacing=6)
        self.spin_label = Gtk.Label("Text size:")
        self.spin_box.pack_start(self.spin_label, True, True, 0)
        self.spin_box.pack_start(self.spinbutton, True, True, 0)
        self.ver_box.pack_start(self.spin_box, True, True, 0)
        self.ver_box.pack_start(link, True, True, 0)
        self.spinbutton.connect("value-changed", self.on_spin_changed)
        self.spinbutton.set_numeric(True)
        self.spinbutton.set_property("value", 10)
        self.on_spin_changed(self)
        self.on_radio_toggled(self.button1)
        self.ver_box.show()
        self.hbox.show()
        self.spin_label.show()
        self.spin_box.show()
        self.spinbutton.show()
        self.box.show()
        self.print_box.show()
        self.entry.show()
        self.label.show()
        self.button1.show()
        self.button2.show()
        self.button.show()
        button.show()
        self.switch.show()
        button3.show()
        link.show()

    @staticmethod
    def get_resource_path(rel_path):
        dir_of_py_file = os.path.dirname(__file__)
        rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
        abs_path_to_resource = os.path.abspath(rel_path_to_resource)
        return abs_path_to_resource

    def on_button_toggled(self, button):
        if button.get_active():
            self.switch.set_property("label", "Print: On")
        else:
            self.switch.set_property("label", "Print: Off")

    def click(self, entry):
        if self.switch.get_active():
            text = self.entry.get_text()
            self.button.set_property("label", text)
            self.label.set_text(text)
            self.label.set_selectable(True)
            if self.color == "Red":
                print('\033[1;31m'+text+'\033[1;m')
            elif self.color == "Green":
                print('\033[1;32m'+text+'\033[1;m')
            elif self.color == "Blue":
                print('\033[1;34m'+text+'\033[1;m')
        else:
            text = self.entry.get_text()
            self.button.set_property("label", text)
            self.label.set_text(text)
            self.label.set_selectable(True)

    def on_check(self, check_box):
        # if the toggle button is active, set the visibility of the text True
        if check_box.get_active():
            self.entry.set_visibility(True)
        # else, set it False
        else:
            self.entry.set_visibility(False)

    def on_radio_toggled(self, button):
        self.color = button.get_property("label")
        if self.color == "Red":
            self.entry.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(1.0, 0.0, 0.0, 1.0))
        elif self.color == "Green":
            self.entry.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 1.0, 0.0, 1.0))
        elif self.color == "Blue":
            self.entry.override_color(Gtk.StateFlags.NORMAL, Gdk.RGBA(0.0, 0.0, 1.0, 1.0))

    def on_spin_changed(self, spinbutton):
        value = self.spinbutton.get_value_as_int()
        self.entry.modify_font(Pango.FontDescription('Dejavu Sans Mono '+str(value)))

    def on_maximize_toggle(self, action, value):
        action.set_state(value)
        if value.get_boolean():
            self.maximize()
        else:
            self.unmaximize()


class Application(Gtk.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="org.example.myapp",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.window = None

        self.add_main_option("test", ord("t"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.NONE, "Command line test", None)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_string(MENU_XML, -1)
        self.set_app_menu(builder.get_object("app-menu"))

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = AppWindow(application=self, title="Print App")

        self.window.present()

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()

        if options.contains("test"):
            # This is printed on the main instance
            print("Test argument recieved")

        self.activate()
        return 0

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


def main():
    app = Application()
    app.run(sys.argv)


if __name__ == "__main__":
    main()
