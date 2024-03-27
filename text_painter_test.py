from text_painter import *

def test_paint_single_color():
    # Arrange
    text = "Hello, World!"
    color_tags = ["#ff0000"]
    count_per_color = 1
    text_painter = TextPainter()
    character_matrix = text.split("\n")
    
    # Act
    tags = text_painter.paint(character_matrix, color_tags, count_per_color)
    
    # Assert
    assert tags[0][0] == "color_tag_0"
    assert tags[0][1] == "#ff0000"
    assert tags[0][2] == "1.0 1.1"
    
def test_paint_red_blue_green_per_character():
    # Arrange
    text = "Hello, World!"
    color_tags = ["#ff0000", "#0000ff", "#00ff00"]
    count_per_color = 1
    text_painter = TextPainter()
    character_matrix = text.split("\n")
    
    # Act
    tags = text_painter.paint(character_matrix, color_tags, count_per_color)
    
    # Assert
    assert tags[0][0] == "color_tag_0"
    assert tags[0][1] == "#ff0000"
    assert tags[0][2] == "1.0 1.1"
    assert tags[1][0] == "color_tag_1"
    assert tags[1][1] == "#0000ff"
    assert tags[1][2] == "1.1 1.2"
    assert tags[2][0] == "color_tag_2"
    assert tags[2][1] == "#00ff00"
    assert tags[2][2] == "1.2 1.3"
    
def test_not_painting_white_space():
    # Arrange
    text = "Hello, World!"
    color_tags = ["#ff0000", "#0000ff", "#00ff00"]
    count_per_color = 1
    text_painter = TextPainter()
    character_matrix = text.split("\n")
    
    # Act
    tags = text_painter.paint(character_matrix, color_tags, count_per_color)
    
    # Assert
    # check comma color
    assert tags[5][0] == "color_tag_5"
    assert tags[5][1] == "#00ff00"
    assert tags[5][2] == "1.5 1.6"
    # check W color, whitespace has no tag
    assert tags[6][0] == "color_tag_6"
    assert tags[6][1] == "#ff0000"
    assert tags[6][2] == "1.7 1.8"

def test_paint_red_blue_green_per_two_characters():
    # Arrange
    text = "Hello, World!"
    color_tags = ["#ff0000", "#0000ff", "#00ff00"]
    count_per_color = 2
    text_painter = TextPainter()
    character_matrix = text.split("\n")
    
    # Act
    tags = text_painter.paint(character_matrix, color_tags, count_per_color)
    
    # Assert
    assert tags[0][0] == "color_tag_0"
    assert tags[0][1] == "#ff0000"
    assert tags[0][2] == "1.0 1.2"
    assert tags[1][0] == "color_tag_1"
    assert tags[1][1] == "#0000ff"
    assert tags[1][2] == "1.2 1.4"
    assert tags[2][0] == "color_tag_2"
    assert tags[2][1] == "#00ff00"
    assert tags[2][2] == "1.4 1.6"
    
def test_paint_across_newline_with_two_characters_per_color():
    # Arrange
    text = "H\nello, World!"
    color_tags = ["#ff0000", "#0000ff", "#00ff00"]
    count_per_color = 2
    text_painter = TextPainter()
    character_matrix = text.split("\n")
    
    # Act
    tags = text_painter.paint(character_matrix, color_tags, count_per_color)
    
    # Assert
    assert tags[0][0] == "color_tag_0"
    assert tags[0][1] == "#ff0000"
    assert tags[0][2] == "1.0 1.1"
    assert tags[1][0] == "color_tag_1"
    assert tags[1][1] == "#ff0000"
    assert tags[1][2] == "2.0 2.1"

def test_paint_low_frequency_dropped_marking():
    # Arrange
    text = "Beneath the sprawling"
    color_tags = ["#ff0000", "#0000ff"]
    count_per_color = 6
    text_painter = TextPainter()
    character_matrix = text.split("\n")
    
    # Act
    tags = text_painter.paint(character_matrix, color_tags, count_per_color)
    
    # Assert
    assert tags[0][0] == "color_tag_0"
    assert tags[0][1] == "#ff0000"
    assert tags[0][2] == "1.0 1.6"
    assert tags[1][0] == "color_tag_1"
    assert tags[1][1] == "#0000ff"
    assert tags[1][2] == "1.6 1.14"
    
def test_paint_spaces_edge_case_end_with_space_on_transition():
    # Arrange
    text = "B en eath"
    # 'e' in 'eath' not painted in certain circumstances
    color_tags = ["#ff0000", "#0000ff"]
    count_per_color = 4
    text_painter = TextPainter()
    character_matrix = text.split("\n")
    
    # Act
    tags = text_painter.paint(character_matrix, color_tags, count_per_color)
    
    # Assert
    assert tags[0][0] == "color_tag_0"
    assert tags[0][1] == "#ff0000"
    assert tags[0][2] == "1.0 1.6"

def test_paint_strategy_for_specific_string():
    # Arrange
    text = "The quick brown fox jumps over the lazy dog."
    color_tags = ["#ff0000"]
    string_to_color = "jumps"
    count_per_color = 1
    text_painter = TextPainter()
    
    # Act
    tags = text_painter.paint_by_strategy(text, color_tags, count_per_color, string_to_color)
    
    # Assert
    assert tags[0][0] == "color_tag_0"
    assert tags[0][1] == "#ff0000"
    assert tags[0][2] == "1.20 1.21"
    assert len(tags) == 5
