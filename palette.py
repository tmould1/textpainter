

class PaletteEntry:
    def __init__(self, color, index):
        self.color = color
        self.index = index

class Palette:
    def __init__(self):
        self.palette = []
        
    def insert_color(self, color, index):
        entry = PaletteEntry(color, index)
        self.palette.append(entry)
        
    def swap_entries_and_indices(self, index_1, index_2):
        entry_1 = self.palette[index_1]
        entry_2 = self.palette[index_2]
        entry_1.index, entry_2.index = entry_2.index, entry_1.index
        self.palette[index_1], self.palette[index_2] = entry_2, entry_1
        
