from FileListView import FileListView
from Preset import Preset
import copy

class PresetListView(FileListView):
    """displays all presets on card"""
    curr_preset = 0
    preset_area = 0     ## object that holds knobs and other preset-controls

    def __init__(self, master=None, **kw):
        self.preset_area=kw.pop('preset_area')
        kw.setdefault("context_entries", (("Add After", self.add_after), ("Duplicate", self.duplicate)))
        master.binder.bind("<<TreeviewSelect>>", self.selection_change)
        kw.setdefault('height', 10)
        self.x = 414
        self.y = 150
        self.name_width = 200


        ret= super().__init__(master=master, **kw)
        self.selection_set([])
        self.selection_add(self.get_children()[0])
        curr_preset=self.file_list.presets[0]
        return ret

    def get_list(self):
        return self.file_list.presets

    def selection_change(self, event):
        if event.widget==self and len(self.selection()) and not self.empty:
            self.preset_area.display_preset(self.file_list.get_file_by_name(self.item(self.selection()[-1])['values'][3])) ##display selected item

    def add_after(self):
        preset = Preset('',self.file_list.get_free_preset_name())
        preset.name = 'New Preset'
        self.add_preset(preset)

    def add_preset(self, preset):
        self.file_list.insert_preset(self.menu_pos+1, preset)
        self.set_files(self.file_list.presets)

    def duplicate(self):
        if not self.empty:
            preset = copy.deepcopy(self.file_list.get_file_by_name(self.item(self.get_children()[self.menu_pos])['values'][3]))
            preset.file_name=self.file_list.get_free_preset_name()
            self.add_preset(preset)
            self.update()