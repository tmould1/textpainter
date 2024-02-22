# Python class to hold text object data
# text object data includes raw text and color segment data

class XtermColor:
    def __init__(self, xterm_code: str):
        self.xterm_code = xterm_code
        
    def __str__(self):
        return self.xterm_code

class ColorSegment:
    def __init__(self, color: XtermColor, start_index: int, end_index: int):
        self.color = color
        self.start_index = start_index
        self.end_index = end_index

class ColorSegmentSet:
    def __init__(self):
        self.segments = []
        
    def append(self, segment: ColorSegment):
        self.segments.append(segment)
        
        # sort the segments by start index
        self.segments.sort(key=lambda x: x.start_index)

class TextDataObject:
    def __init__(self, raw_text: str, color_segments: ColorSegmentSet):
        self.raw_text = raw_text
        self.color_segments = color_segments
        self.text_length = len(raw_text)

    def __str__(self):
        return f"Raw Text: {self.raw_text}\nColor Segments: {self.color_segments}\nText Length: {self.text_length}"
    
    def color_coded_output(self):
        output = ""
        text_index = 0
        for segment in self.color_segments.segments:
            segment_start = segment.start_index
            segment_end = segment.end_index
            if segment_start > text_index:
                output += self.raw_text[text_index:segment_start]
            output += f"{segment.color}{self.raw_text[segment_start:segment_end]}"
            text_index = segment_end
        if text_index < self.text_length:
            output += self.raw_text[text_index:]
        return output
    
