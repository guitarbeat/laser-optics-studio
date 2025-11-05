import tkinter as tk
import unittest
from unittest.mock import MagicMock
from app.gui.application import OpticalDiagramCreator

class TestHandleTab(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        self.app = OpticalDiagramCreator(self.root)
        self.text_widget = self.app.latex_preview

    def tearDown(self):
        self.root.destroy()

    def test_handle_tab_with_selection_should_indent(self):
        # This test will pass with the fixed implementation
        self.text_widget.insert(tk.END, "line1\nline2")
        self.text_widget.tag_add(tk.SEL, "1.0", "end-1c") # Select all text
        self.text_widget.mark_set(tk.INSERT, "1.0")

        # Run the fixed implementation from the application
        self.app.handle_tab(MagicMock())

        # This is the expected behavior
        self.assertEqual(self.text_widget.get("1.0", "end-1c"), "    line1\n    line2")

if __name__ == '__main__':
    unittest.main()
