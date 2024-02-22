from text_edit_and_preview import *

def test_text_editor():
    root = Tk()
    text_editor = TextEditor(root)
    assert text_editor.root == root
    root.destroy()
    
def test_does_color_need_bright_text():
    root = Tk()
    text_editor = TextEditor(root)
    assert text_editor.does_color_need_bright_text("#000000") == True
    assert text_editor.does_color_need_bright_text("#FF0000") == True
    assert text_editor.does_color_need_bright_text("#FFFFFF") == False
    assert text_editor.does_color_need_bright_text("#FFFF00") == False
    root.destroy()