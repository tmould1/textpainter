
# Importing tkinter and ttk modules
from tkinter import * 
 
# Importing Collapsible Pane class that we have
# created in separate file
from collapsible_frame_container import CollapsiblePane as cp
 
# Making root window or parent window
root = Tk()
root.geometry('200x200')
 
# Creating Object of Collapsible Pane Container
# If we do not pass these strings in
# parameter the default strings will appear
# on button that were, expand >>, collapse <<
# cpane = cp(root, 'Expanded', 'Collapsed')
# cpane.grid(row = 0, column = 0)
 
# # Button and checkbutton, these will
# # appear in collapsible pane container
# b1 = Button(cpane.frame, text ="GFG").grid(
#             row = 1, column = 2, pady = 10)
 
# cb1 = Checkbutton(cpane.frame, text ="GFG").grid(
#                   row = 1, column = 3, pady = 10)

# cpane2 = cp(root, 'Expanded', 'Collapsed')
# cpane2.grid(row = 1, column = 0)
# b2 = Button(cpane2.frame, text ="GFG").grid(
#             row = 1, column = 2, pady = 10)
# cb2 = Checkbutton(cpane2.frame, text ="GFG").grid(
#                     row = 2, column = 3, pady = 10)

collapsible_panes = []
background_layer_pane = cp(root, "Background Layer", "Background Layer")
collapsible_panes.append(background_layer_pane)
background_layer_pane.pack(side = TOP)
background_layer_frame = background_layer_pane.frame
label_1 = Label(background_layer_frame, text = "Label 1")
label_1.grid(row = 0, column = 0)
text_input_1 = Entry(background_layer_frame)
text_input_1.grid(row = 0, column = 1)
checkbox_1 = Checkbutton(background_layer_frame, text = "Checkbox 1")
checkbox_1.grid(row = 1, column = 0)

foreground_layer_pane = cp(root, "Foreground Layer", "Foreground Layer")
collapsible_panes.append(foreground_layer_pane)
foreground_layer_pane.pack(side = TOP)
foreground_layer_frame = foreground_layer_pane.frame
label_2 = Label(foreground_layer_frame, text = "Label 2")
label_2.grid(row = 0, column = 0)
text_input_2 = Entry(foreground_layer_frame)
text_input_2.grid(row = 0, column = 1)
checkbox_2 = Checkbutton(foreground_layer_frame, text = "Checkbox 2")
checkbox_2.grid(row = 1, column = 0)

highlight_layer_panel = cp(root, "Highlight Layer", "Highlight Layer")
collapsible_panes.append(highlight_layer_panel)
highlight_layer_panel.pack(side = TOP)
highlight_layer_frame = highlight_layer_panel.frame
label_3 = Label(highlight_layer_frame, text = "Label 3")
label_3.grid(row = 0, column = 0)
text_input_3 = Entry(highlight_layer_frame)
text_input_3.grid(row = 0, column = 1)
checkbox_3 = Checkbutton(highlight_layer_frame, text = "Checkbox 3")
checkbox_3.grid(row = 1, column = 0)


#mainloop()