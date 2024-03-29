import os
import json
import time
import re

from tkinter import *

from tkinter import colorchooser

from text_painter import TextPainter

from collapsible_frame_container import CollapsiblePane

class CollapsiblePane_Palette(CollapsiblePane):
    def __init__(self, parent, expanded_text="Collapse <<", collapsed_text="Expand >>"):
        CollapsiblePane.__init__(self, parent, expanded_text, collapsed_text)
        self.palette_color_frames_and_buttons = []
        self.palette_modifier_settings = PaletteLayerSettings()

class TextEditor:
    def __init__(self, root):
        self.palette_window = None

        self.palette_storage_info = PaletteSetStorageManager()
        self.text_painter = TKinterTextPainter()
        
        self.font = ("Courier New", 16)
        self.root = root
        self.root.title("Text Painter")
        self.paint_refresh_rate = 1
        self.paint_last_update_time = time.time()
        self.default_text_color_rgb = "#a0a0a0" # grey

        self.input_and_result_frame = Frame(self.root)
        self.input_and_result_frame.pack(side=TOP)
        self.create_input_text_display(self.input_and_result_frame, LEFT)
        self.create_output_text_display(self.input_and_result_frame, RIGHT)
        
        self.user_options_frame = Frame(self.root)
        self.user_options_frame.pack(side=BOTTOM)
        self.create_manual_convert_button(self.user_options_frame, LEFT)
        self.create_button_for_palette_window(self.user_options_frame, LEFT)
        self.create_output_background_selector_button(self.user_options_frame, LEFT)
        
        ## BEGIN CONVERSION TO LAYERS INSTEAD OF A SINGLE PALETTE FRAME
        self.palette_color_frames_and_buttons = []
        self.palette_modifier_settings = PaletteLayerSettings()

        # self.layers_section_frame = Frame(self.input_and_result_frame)
        # self.layers_section_frame.pack(side=TOP)
        
        # self.first_layer_pane = CollapsiblePane_Palette(self.layers_section_frame, "First Layer", "First Layer")
        # self.first_layer_pane.pack(side=TOP)
        # self.create_palette(parent=self.first_layer_pane.frame, alignment=TOP)
        
        # self.second_layer_pane = CollapsiblePane_Palette(self.layers_section_frame, "Second Layer", "Second Layer")
        # self.second_layer_pane.pack(side=TOP)
        # self.create_palette(parent=self.second_layer_pane.frame, alignment=TOP)
        
        
        self.palette_frame = Frame(self.input_and_result_frame)
        self.palette_frame.pack(side=TOP)
        self.create_palette(parent=self.palette_frame, alignment=TOP)
        
        ## END CONVERSION TO LAYERS INSTEAD OF A SINGLE PALETTE FRAME
        
        # DELEGATES!
        self.root.bind("<KeyRelease>", self.key_released)
        
        # Experimental Button for animating
        self.animate_button = Button(self.user_options_frame, text="Animate", command=self.animate, bg="green")
        self.animate_button.pack(side=LEFT)
        self.animated_slider_value_index = 0
        self.animated_slider_values = [1, 2, 4, 8, 4, 2]
        self.is_animating = False
        # variable to hold the frame rate
        self.frame_rate_frame = Frame(self.user_options_frame)
        self.frame_rate_frame.pack(side=LEFT)
        self.frame_rate_title = Label(self.frame_rate_frame, text="Frame Rate", font=self.font)
        self.frame_rate_title.pack(side=LEFT)
        self.frame_rate_slider = Scale(self.frame_rate_frame, from_=1, to=60, orient=HORIZONTAL, command=lambda x: self.update_frame_rate())
        self.frame_rate_slider.pack(side=LEFT)
        
    def update_frame_rate(self):
        # pull the frame from the slider
        self.frame_rate = self.frame_rate_slider.get()
        
    def animate(self):
        # toggle the state
        self.is_animating = not self.is_animating
        
        if self.is_animating:
            self.animate_button.config(text="Stop", bg="red")
            self.update_frame_rate()
            self.animated_slider_value_index = 0
            self.next_frame()
        else:
            self.animate_button.config(text="Animate", bg="green")
        
    def next_frame(self):
        self.update_frame_rate()
        #print("Next Frame")
        # animate the slider on a timer
        self.animated_slider_value = self.animated_slider_values[self.animated_slider_value_index]
        self.settings_count_per_color.set(self.animated_slider_value)
        self.animated_slider_value_index += 1
        if self.animated_slider_value_index >= len(self.animated_slider_values):
            self.animated_slider_value_index = 0
        self.convert()
        if self.is_animating:
            self.root.after(int(1000 / self.frame_rate), self.next_frame)
     
    def create_input_text_display(self, parent, alignment=TOP):
        self.input_display_frame = Frame(parent)
        self.input_display_frame.pack(side=alignment)
        self.input_text_label = Label(self.input_display_frame, text="Input Text", font=self.font)
        self.input_text_label.pack(side=BOTTOM)
        self.input_text = Text(self.input_display_frame, wrap=WORD, font=self.font, bg="black", fg="grey")
        self.input_text.pack(expand=True, fill=BOTH)
        
    def create_output_text_display(self, parent, alignment=TOP):
        self.output_display_frame = Frame(parent)
        #self.output_display_frame.pack(side=alignment)
        self.output_text_label = Label(self.output_display_frame, text="Text with color codes", font=self.font)
        self.output_text_label.pack(side=BOTTOM)
        self.output_text = Text(self.output_display_frame, wrap=WORD, font=self.font, bg="black")
        self.output_text.pack()

    def create_manual_convert_button(self, parent, alignment=TOP):
        self.convert_button = Button(parent, text="Convert", command=self.convert)
        self.convert_button.pack(side=alignment)
        
    def convert(self):
        convert_request_time = time.time()
        if convert_request_time - self.paint_last_update_time < self.paint_refresh_rate:
            #print(f"Skipping paint, last paint was {convert_request_time - self.paint_last_update_time} seconds ago")
            #print(f"Refresh rate is {self.paint_refresh_rate} seconds")
            return
        
        self.output_text.delete(1.0, END)
        # get a list of all the colors from the palette
        # palette_colors = []
        # for entry in self.palette_color_frames_and_buttons:
        #     palette_colors.append(entry[1].cget("text"))
        # # Clear existing tags
        # for tag in self.input_text.tag_names():
        #     self.input_text.tag_delete(tag)
        # self.text_painter.paint(self.input_text, self.output_text, palette_colors, self.palette_modifier_settings)
        self.paint_layer(self.first_layer_pane.palette_color_frames_and_buttons, self.first_layer_pane.palette_modifier_settings)

    # args are: Palette set and how to paint that on the text
    def paint_layer(self, paletee_color_frames_and_buttons, palette_modifier_settings):
        # get a list of all the colors from the palette
        palette_colors = []
        for entry in paletee_color_frames_and_buttons:
            palette_colors.append(entry[1].cget("text"))
        # Clear existing tags
        for tag in self.input_text.tag_names():
            self.input_text.tag_delete(tag)
        self.text_painter.paint(self.input_text, self.output_text, palette_colors, palette_modifier_settings)

    def create_button_for_palette_window(self, parent, alignment=TOP):
        self.palette_button = Button(parent, text="Palette Selector", command=self.create_palette)
        self.palette_button.pack(side=alignment)
    
    def create_output_background_selector_button(self, parent, alignment=TOP):
        self.output_background_selector_button = Button(parent, text="Output Background", command=self.select_output_background)
        self.output_background_selector_button.pack(side=alignment)
    
    def create_palette(self, parent=None, alignment=TOP):
        if parent is None:
            window_exists = False
            if self.palette_window is not None:
                window_exists = self.palette_window.winfo_exists()
            if window_exists:
                self.palette_window.deiconify()
            else:
                self.palette_window = Toplevel(self.root)
                self.palette_window.title("Palette")
                self.create_palette_widgets(parent=self.palette_window)
        else:
            self.create_palette_widgets(parent=parent)
                
    def create_palette_widgets(self, parent=None):
        # Color Selection Frame
        self.color_selection_frame = Frame(parent)
        self.color_selection_frame.pack(side=LEFT)
        # Palette List SubFrame of Color Selection
        self.palette_frame = Frame(self.color_selection_frame)
        self.palette_frame.pack(side=TOP)
        self.palette_name_label = Label(self.palette_frame, text="Unsaved Palette", font=("Courier New", 14))
        self.palette_name_label.pack()
        # Palette List Modifiers SubFrame of Color Selection
        self.palette_list_interactions_frame = Frame(self.color_selection_frame)
        self.palette_list_interactions_frame.pack(side=BOTTOM)
        self.add_color_button = Button(self.palette_list_interactions_frame, text="Add Color", command=self.add_color)
        self.add_color_button.pack(side=TOP)
        self.serialization_frame = Frame(self.palette_list_interactions_frame)
        self.serialization_frame.pack(side=BOTTOM)
        self.save_palette_button = Button(self.serialization_frame, text="Save Palette", command=self.save_palette)
        self.save_palette_button.pack(side=LEFT)
        self.load_palette_button = Button(self.serialization_frame, text="Load Palette", command=self.load_palette)
        self.load_palette_button.pack(side=RIGHT)
        self.clear_palette_button = Button(self.serialization_frame, text="Clear Palette", command=self.clear_palette, bg="red")
        self.clear_palette_button.pack()
        # Settings Frame
        self.paint_settings_frame = Frame(parent)
        self.paint_settings_frame.pack(side=RIGHT)
        self.strategy_frame = Frame(self.paint_settings_frame)
        self.strategy_frame.pack(side=TOP)
        self.settings_strategy_variable = StringVar()
        self.settings_strategy_variable.set(self.palette_modifier_settings.strategy_options[0])
        self.settings_strategy_variable.trace_add("write", self.strategy_changed)
        self.settings_selector = OptionMenu(self.strategy_frame, self.settings_strategy_variable, *self.palette_modifier_settings.strategy_options)
        self.settings_selector.pack()
        self.settings_count_per_color = Scale(self.strategy_frame, from_=1, to=32, orient=HORIZONTAL, label="Count per Color", command=lambda x: self.handle_slider_update(x))
        self.settings_count_per_color.pack()
        self.add_reverse_palette_button = Button(self.strategy_frame, text="Add Reverse Palette", command=self.add_reverse_palette)
        self.add_reverse_palette_button.pack()        

    def strategy_changed(self, *args):
        old_strategy_name = self.palette_modifier_settings.get_variable_by_name("strategy")
        new_strategy_name = self.settings_strategy_variable.get()
        self.palette_modifier_settings.set_variable_by_name("strategy", new_strategy_name)
        
        if old_strategy_name != new_strategy_name:
            # Change detected
            # Hack, move additional UI elements per strategy to a strategy object method. atm, we only track string names, but we need functionality here
            self.strategy_frame.pack_forget()
            self.strategy_frame.pack()
            if old_strategy_name == "Paint String":
                self.strategy_parameter_entry.unbind("<KeyRelease>")
                self.strategy_parameter_frame.pack_forget()
            self.settings_count_per_color.pack_forget()
            self.add_reverse_palette_button.pack_forget()
            
            self.settings_selector.pack()
            if new_strategy_name == "Paint String":
                # add a new label and text input to capture the string to paint
                self.strategy_parameter_frame = Frame(self.strategy_frame)
                self.strategy_parameter_frame.pack()
                self.strategy_parameter_label = Label(self.strategy_parameter_frame, text="String to Paint")
                self.strategy_parameter_label.pack(side=LEFT)
                self.strategy_parameter_entry = Entry(self.strategy_parameter_frame)
                self.strategy_parameter_entry.insert(0, self.palette_modifier_settings.get_variable_by_name("string_to_paint"))
                self.strategy_parameter_entry.pack(side=RIGHT)
                            
            self.settings_count_per_color.pack()
            self.add_reverse_palette_button.pack()
             
        self.convert()

    def string_to_paint_changed(self, *args):
        string_to_paint = self.strategy_parameter_entry.get()
        self.palette_modifier_settings.set_variable_by_name("string_to_paint", string_to_paint)
        self.convert()

    def handle_slider_update(self, value):
        self.palette_modifier_settings.set_variable_by_name("count_per_color", int(value))
        self.convert()

    def add_color(self, parent=None):
        color_code = colorchooser.askcolor()
        if color_code[1]:
            self.do_add_color(color_code[1], parent)
            
    def do_add_color(self, color_code, parent=None):
        if parent is None:
            parent = self.palette_frame
        button_frame = Frame(parent)
        color_button = Button(button_frame, text=color_code, bg=color_code, command=lambda: self.edit_color(button_frame))
        if self.does_color_need_bright_text(color_code):
            color_button.config(fg="white")
        color_button.pack(side = LEFT)
        remove_color_button = Button(button_frame, text="Remove", command=lambda: self.remove_color(button_frame))
        remove_color_button.pack(side = RIGHT)
        move_down_button = Button(button_frame, text="Down", command=lambda: self.move_color_down(button_frame))
        move_down_button.pack(side = RIGHT)
        move_up_button = Button(button_frame, text="Up", command=lambda: self.move_color_up(button_frame))
        move_up_button.pack(side = RIGHT)
        palette_entry = (button_frame, color_button, remove_color_button)
        self.palette_color_frames_and_buttons.append(palette_entry)
        button_frame.pack()
        self.convert()
    
    def move_color_up(self, button_frame):
        did_move = False
        for entry in self.palette_color_frames_and_buttons:
            if entry[0] == button_frame:
                index = self.palette_color_frames_and_buttons.index(entry)
                if index > 0:
                    self.palette_color_frames_and_buttons[index], self.palette_color_frames_and_buttons[index - 1] = self.palette_color_frames_and_buttons[index - 1], self.palette_color_frames_and_buttons[index]
                    self.convert()
                    did_move = True
                    break
        if did_move:
            # clear the palette buttons and repack with the new order
            for entry in self.palette_color_frames_and_buttons:
                entry[0].pack_forget()
                entry[0].pack()
        self.convert()
              
    def move_color_down(self, button_frame):
        did_move = False
        for entry in self.palette_color_frames_and_buttons:
            if entry[0] == button_frame:
                index = self.palette_color_frames_and_buttons.index(entry)
                if index < len(self.palette_color_frames_and_buttons) - 1:
                    self.palette_color_frames_and_buttons[index], self.palette_color_frames_and_buttons[index + 1] = self.palette_color_frames_and_buttons[index + 1], self.palette_color_frames_and_buttons[index]
                    self.convert()
                    did_move = True
                    break
        if did_move:
            # clear the palette buttons and repack with the new order
            for entry in self.palette_color_frames_and_buttons:
                entry[0].pack_forget()
                entry[0].pack()
            self.convert()
    
    def edit_color(self, button_frame):
        current_color = button_frame.winfo_children()[0].cget("text")
        color_code = colorchooser.askcolor(current_color)
        if color_code[1]:
            palette_entry = None
            for entry in self.palette_color_frames_and_buttons:
                if entry[0] == button_frame:
                    palette_entry = entry
            color_button = palette_entry[1]
            color_button.config(bg=color_code[1], text=color_code[1])
            if self.does_color_need_bright_text(color_code[1]):
                color_button.config(fg="white")
            else:
                color_button.config(fg="black")
            self.convert()
                
    def remove_color(self, button_frame):
        palette_entry = None
        for entry in self.palette_color_frames_and_buttons:
            if entry[0] == button_frame:
                palette_entry = entry
                            
        if palette_entry is not None:
            palette_entry[0].pack_forget()
            self.palette_color_frames_and_buttons.remove(palette_entry)
        
        self.convert()
            
    def does_color_need_bright_text(self, color):
        # if color is dark, return True
        # if color is light, return False
        # if 0 is dark and F is bright, then we can form a "color average" over the channels
        r_value = int(color[1:3], 16)
        g_value = int(color[3:5], 16)
        b_value = int(color[5:7], 16)
        color_sum = r_value + g_value + b_value
        if color_sum > 0x7F * 3:
            return False
        else:
            return True

    def save_palette(self, parent = None):
        if parent is None:
            parent = self.palette_window
        colors_in_palette = []
        for entry in self.palette_color_frames_and_buttons:
            colors_in_palette.append(entry[1].cget("text"))

        # Pop up a window to ask for a palette name
        self.get_palette_name_window = Toplevel(self.palette_window)
        self.get_palette_name_window.title("Palette Name")
        listbox_of_existing_palettes = Listbox(self.get_palette_name_window)
        listbox_of_existing_palettes.pack(side = TOP)
        existing_palettes = self.palette_storage_info.get_all_palette_sets()
        for palette_name in existing_palettes:
            listbox_of_existing_palettes.insert(END, palette_name)
        user_interaction_frame = Frame(self.get_palette_name_window)
        user_interaction_frame.pack(side = BOTTOM)
        palette_name_entry = Entry(user_interaction_frame)
        palette_name_entry.pack(side = LEFT)
        save_palette_button = Button(user_interaction_frame, text="Save", command=lambda: self.do_save_palette(palette_name_entry.get(), colors_in_palette, self.palette_modifier_settings))
        save_palette_button.pack(side = RIGHT)
        
    def do_save_palette(self, palette_name, colors_in_palette, palette_settings):
        did_save = self.palette_storage_info.save_palette_set(palette_name, colors_in_palette, palette_settings)
        self.saved_success_popup = Toplevel(self.palette_window)
        self.saved_success_popup.title("Saved")
        self.saved_success_popup_label = Label(self.saved_success_popup, text="Palette Saved!")
        self.saved_success_popup_label.pack()
        if self.saved_success_popup is not None:
            ok_button = Button(self.saved_success_popup, text="OK", command=self.clear_save_windows)
            ok_button.pack()
        self.palette_name_label.config(text=palette_name)
        
    def clear_save_windows(self):
        self.saved_success_popup.destroy()
        self.get_palette_name_window.destroy()
        if self.palette_window is not None:
            self.palette_window.deiconify()
        
    def load_palette(self, parent=None):
        self.load_palette_window = Toplevel(self.palette_window)
        self.load_palette_window.title("Load Palette")
        directions_textbox = Text(self.load_palette_window, wrap=WORD)
        directions_textbox.insert(1.0, "Select a palette to load")
        listbox_of_existing_palettes = Listbox(self.load_palette_window)
        listbox_of_existing_palettes.pack(side = TOP)
        existing_palettes = self.palette_storage_info.get_all_palette_sets()
        for palette_name in existing_palettes:
            listbox_of_existing_palettes.insert(END, palette_name)
        user_interaction_frame = Frame(self.load_palette_window)
        user_interaction_frame.pack(side = BOTTOM)
        load_palette_button = Button(user_interaction_frame, text="Load", command=lambda: self.do_load_palette(listbox_of_existing_palettes.get(ACTIVE), parent))
        load_palette_button.pack()
    
    def do_load_palette(self, palette_name, parent=None):
        palette_data = self.palette_storage_info.load_palette_set(palette_name)
        palette_colors = palette_data["layer_one"]["colors"]
        palette_settings = palette_data["layer_one"]["settings"]
        
        if palette_colors is None:
            # clear the tags in the window
            for tags in self.input_text.tag_names():
                self.input_text.tag_delete(tags)
            return
        
        for key in palette_settings:
            #print("Setting: " + key + " Value: " + str(palette_settings[key]))
            self.palette_modifier_settings.set_variable_by_name(key, palette_settings[key])
            
        # if the loaded data didnt have new values, check for them and use the default settings object to grab the proper values
        default_settings = PaletteLayerSettings()
        for key in self.palette_modifier_settings.get_keys():
            if self.palette_modifier_settings.get_variable_by_name(key) is None:
                self.palette_modifier_settings.set_variable_by_name(key, default_settings.get_variable_by_name(key))
        
        self.settings_count_per_color.set(self.palette_modifier_settings.get_variable_by_name("count_per_color"))
        strategy = self.palette_modifier_settings.get_variable_by_name("strategy")
        self.settings_strategy_variable.set(strategy)
        self.settings_selector.config(text=strategy)
        
        # clear the current palette
        for entry in self.palette_color_frames_and_buttons:
            entry[0].pack_forget()
        self.palette_color_frames_and_buttons = []
        
        for color in palette_colors:
            self.do_add_color(color)
        
        self.load_palette_window.destroy()
        self.convert()
        self.palette_name_label.config(text=palette_name)

    def clear_palette(self, parent=None):
        self.are_you_sure_window = Toplevel(self.palette_window)
        self.are_you_sure_window.title("Are you sure?")
        are_you_sure_label = Label(self.are_you_sure_window, text="Are you sure you want to clear the palette?")
        are_you_sure_label.pack()
        yes_no_frame = Frame(self.are_you_sure_window)
        yes_no_frame.pack()
        yes_button = Button(yes_no_frame, text="Yes", command=lambda: self.do_clear_palette())
        yes_button.pack(side=LEFT)
        no_button = Button(yes_no_frame, text="No", command=lambda: self.are_you_sure_window.destroy())
        no_button.pack(side=RIGHT)
        
    def do_clear_palette(self):
        for entry in self.palette_color_frames_and_buttons:
            entry[0].pack_forget()
        self.palette_color_frames_and_buttons = []
        self.are_you_sure_window.destroy()
        self.palette_name_label.config(text="Unsaved Palette")

    def select_output_background(self):
        color_code = colorchooser.askcolor()
        if color_code[1]:
            self.output_text.config(bg=color_code[1])

    def add_reverse_palette(self):
        copy_of_palette_colors = []
        for entry in self.palette_color_frames_and_buttons:
            copy_of_palette_colors.append(entry[1].cget("text"))
        
        copy_of_palette_colors.reverse()
        copy_of_palette_colors.pop(0)
        for color in copy_of_palette_colors:
            self.do_add_color(color)

    def key_released(self, event):
        if event.keysym == "Escape":
            # get the focused window
            focused_window = self.root.focus_get()
            focused_window.destroy()
        else:
            self.update_string_variable_fields()
            self.convert()
            
    def update_string_variable_fields(self):
        if self.palette_modifier_settings.get_variable_by_name("strategy") == "Paint String":
            self.palette_modifier_settings.set_variable_by_name("string_to_paint", self.strategy_parameter_entry.get())

# Converting from Palette to Palette Set.
class PaletteSetStorageManager:
    def __init__(self):
        self.palette_set_save_file = "palette_save.json"
        self.palette_set_save = {}
        self.palette_set_save_version = 1
        
        # Create or Load palette save file
        if not os.path.exists(self.palette_set_save_file):
            with open(self.palette_set_save_file, "w") as file:
                file.write("{}")
        else:
            with open(self.palette_set_save_file, "r") as file:
                self.palette_set_save = json.load(file)
   
    def save_palette_set(self, saved_palette_set_name, palette_colors, palette_layer_settings):
        palette_set_data = {}
        palette_set_data["version"] = self.palette_set_save_version
        palette_set_data["settings"] = palette_layer_settings.settings_data
        palette_set_data["colors"] = palette_colors
        self.palette_set_save[saved_palette_set_name] = palette_set_data
        with open(self.palette_set_save_file, "w") as file:
            json.dump(self.palette_set_save, file, indent=4)
        
        return True
    
    def load_palette_set(self, palette_set_name):
        palette_set = self.palette_set_save[palette_set_name]
        
        # if it doesn't contain the "version" entry, add it and set to 0
        if "version" not in palette_set:
            palette_set["version"] = 0
        
        # if the version is less than the current version, update the palette set
        # At Version 1: we added the version number
        palette_version = palette_set["version"]
        needs_resave_from_version_update = False
        if palette_version == 0:
            # update the palette set to version 1
            palette_version = 1
            needs_resave_from_version_update = True
        # At Version 2: we added layers support. each current entry should be wrapped in "layer_one"
        if palette_version == 1:
            # update the palette set to version 2
            palette_version = 2
            palette_set["layer_one"] = {}
            palette_set["layer_one"]["settings"] = palette_set["settings"]
            palette_set["layer_one"]["colors"] = palette_set["colors"]
            del palette_set["settings"]
            del palette_set["colors"]
            needs_resave_from_version_update = True
                
        # Once done updating, update version number and dump json
        if needs_resave_from_version_update:
            palette_set["version"] = palette_version
            with open(self.palette_set_save_file, "w") as file:
                json.dump(self.palette_set_save, file, indent=4)
        
        return palette_set
    
    def get_all_palette_sets(self):
        return self.palette_set_save
    
    def check_if_palette_set_name_exists_in_save(self, palette_set_name):
        return palette_set_name in self.palette_set_save

class PaletteLayerSettings:
    def __init__(self):
        self.strategy_options = [
            "Paint Over Full Text",
            "Paint Per Word",
            "Paint String"
        ]
        
        self.settings_data = {}
        self.settings_data["count_per_color"] = 1
        self.settings_data["strategy"] = self.strategy_options[0]
        self.settings_data["string_to_paint"] = ""

    def get_variable_by_name(self, name):
        if name in self.settings_data:
            return self.settings_data[name]
        return None
    
    def get_keys(self):
        return self.settings_data.keys()

    def set_variable_by_name(self, name, value):
        #print("Setting: " + name + " to " + str(value))
        self.settings_data[name] = value

class TKinterTextPainter:
    def __init__(self):
        pass
        
    def paint(self, input_text_object, output_text_object, palette_colors, palette_modifier_settings):
        full_raw_text = input_text_object.get(1.0, END)

        # transfer the raw text to the output text, no paint yet (Output window will become window with XTerm tags embedded, no color)
        output_text_object.insert(END, full_raw_text)

        text_to_paint = full_raw_text
        string_to_paint = None
        
        # For each layer stuff will go here...
        # For each strategy, depth first...
        current_strategy = palette_modifier_settings.get_variable_by_name("strategy")
        
        
        
        if current_strategy == "Paint String":
            string_to_paint = palette_modifier_settings.get_variable_by_name("string_to_paint")
            # find first match to paint
            match = re.search(string_to_paint, full_raw_text) # Might not work across new lines?
            if match is None:
                text_to_paint = match.group(0)
                
            print(f"String to paint: {string_to_paint} text to paint: {text_to_paint}")
                           
                           
                           
                           
        length_of_text = len(text_to_paint) - 1 # -1 for the newline character at the end of the text
        count_per_color = palette_modifier_settings.get_variable_by_name("count_per_color")
        number_of_tags_needed = length_of_text // count_per_color
        if length_of_text % count_per_color > 0:
            number_of_tags_needed += 1
        
        if len(palette_colors) < 1:
            # put input into output as is
            output_text_object.insert(END, text_to_paint)
            return
        
        #print("Number of tags needed: " + str(number_of_tags_needed))
        color_tags = []
        for i in range(number_of_tags_needed):
            tag_color = palette_colors[i % len(palette_colors)]
            color_tags.append(tag_color)
        
        text_painter = TextPainter()
        #print("Count per color: " + str(count_per_color))
        tags = text_painter.paint_by_strategy(full_raw_text, color_tags, count_per_color, string_to_paint)
        
        # take the results from the text painter and apply the colors to the TK text object
        last_end_marker = END
        for tag in tags:
            tag_id = tag[0]
            color = tag[1]
            add_string = tag[2]
            start_marker = add_string.split(" ")[0]
            end_marker = add_string.split(" ")[1]
            # TODO: Move this to a separate window that houses the text with xterm tags embedded, with no color
            #output_text_object.tag_config(tag_id, foreground=color)
            #output_text_object.tag_add(tag_id, start_marker, end_marker)
            input_text_object.tag_config(tag_id, foreground=color)
            input_text_object.tag_add(tag_id, start_marker, end_marker)
            last_end_marker = end_marker
            
        # add default color tag at the end of the text to prevent color bleeding
        input_text_object.tag_config("default", foreground="#a0a0a0")
        input_text_object.tag_add("default", last_end_marker, END)
        
        # for tag in tags:
        #     print(f"Tag: {tag}  Color: {tag[1]}     Start: {tag[2].split(' ')[0]}     End: {tag[2].split(' ')[1]}")


if __name__ == "__main__":
    root = Tk()
    text_editor = TextEditor(root)
    root.mainloop()