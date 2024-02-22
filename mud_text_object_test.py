from mud_text_object import *

# Create a test a Mud Color Object
def test_mud_color():
    color = XtermColor("@x000")
    assert str(color) == "@x000"
    
# Create a test a Color Segment Object
def test_color_segment():
    color = XtermColor("@x000")
    segment = ColorSegment(color, 0, 5)
    assert segment.color == color
    assert segment.start_index == 0
    assert segment.end_index == 5
    
# Create a test a Color Segment Set Object
def test_color_segment_set():
    color = XtermColor("@x000")
    segment = ColorSegment(color, 0, 5)
    segment_set = ColorSegmentSet()
    segment_set.append(segment)
    assert segment_set.segments[0] == segment

# Create a test a Text Data Object
def test_text_data_object():
    color = XtermColor("@x100")
    segment = ColorSegment(color, 0, 4)
    color_2 = XtermColor("@x200")
    segment_2 = ColorSegment(color_2, 5, 8)
    segment_set = ColorSegmentSet()
    # out of order on purpose to test sorting by start index
    segment_set.append(segment_2)
    segment_set.append(segment)
    text_data = TextDataObject("Test Text", segment_set)
    assert text_data.raw_text == "Test Text"
    assert text_data.color_segments == segment_set
    assert text_data.text_length == 9
    assert text_data.color_coded_output() == "@x100Test @x200Text"
    