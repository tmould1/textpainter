from palette import *

def test_palette_entry():
    color = "@x100"
    entry = PaletteEntry(color, 0)
    assert entry.color == color
    assert entry.index == 0
    
def test_insert():
    palette = Palette()
    color = "@x100"
    palette.insert_color(color, 0)
    assert palette.palette[0].color == color
    assert palette.palette[0].index == 0
    
def test_swap_entries_and_indices():
    palette = Palette()
    color = "@x100"
    palette.insert_color(color, 0)
    color = "@x200"
    palette.insert_color(color, 1)
    palette.swap_entries_and_indices(0, 1)
    assert palette.palette[0].color == "@x200"
    assert palette.palette[0].index == 0
    assert palette.palette[1].color == "@x100"
    assert palette.palette[1].index == 1