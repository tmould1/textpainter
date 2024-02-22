

class TextPainter():
    def __init__(self):
        pass

    def paint(self, character_matrix, color_tags, count_per_color):
        tags = []
        # go through each character in the input text and add tags for the output text
        #  based on the line and column indices
        tag_id = 0
        painted_characters = 0
        painted_sections = 0
        needs_line_finished = False
        # Known issue:
        # - Doesn't handle colors that carry across newlines
        for i, line in enumerate(character_matrix):
            for j, character in enumerate(line):
                if character.isspace():
                    # dont do anything on non-rendered characters
                    continue
                
                color_space_index = painted_characters % count_per_color
                if color_space_index == 0 or needs_line_finished:
                    characters_left_to_paint = count_per_color
                    if needs_line_finished:
                        needs_line_finished = False
                        characters_left_to_paint = count_per_color - painted_characters % count_per_color
                               
                    tkinter_line_start_index = i + 1
                    tkinter_line_end_index = tkinter_line_start_index
                    tkinter_column_start_index = j
                    tkinter_column_end_index = tkinter_column_start_index + characters_left_to_paint
                    text_from_j_to_end = line[j:tkinter_column_end_index]
                    #print("text_from_j_to_end: " + str(text_from_j_to_end))
                    
                    section_ready_for_paint = False
                    while section_ready_for_paint == False:
                        num_whitespace = 0
                        for sub_character in text_from_j_to_end:
                            if sub_character.isspace():
                                num_whitespace += 1
                        
                        tkinter_column_end_index = tkinter_column_start_index + characters_left_to_paint + num_whitespace
                                      
                        if tkinter_column_end_index > len(line):
                            tkinter_column_end_index = len(line)
                            needs_line_finished = True
                            section_ready_for_paint = True

                        # are we done?
                        num_rendered_characters = len(text_from_j_to_end) - num_whitespace
                        if characters_left_to_paint - num_rendered_characters <= 0:
                            section_ready_for_paint = True

                        text_from_j_to_end = line[j:tkinter_column_end_index]

                        
                    color_tag_index = painted_sections % len(color_tags)
                    
                    color = color_tags[color_tag_index]
                    tag_config_string = "color_tag_" + str(tag_id)
                    tag_add_string = str(tkinter_line_start_index) + "." + str(tkinter_column_start_index) + " " + str(tkinter_line_end_index) + "." + str(tkinter_column_end_index)
                    tags.append((tag_config_string, color, tag_add_string))
                    tag_id += 1       
                painted_characters += 1
                if painted_characters % count_per_color == 0:
                    painted_sections += 1

        return tags
