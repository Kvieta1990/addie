import os
from step2_handler.table_handler import TableHandler


class CreateNdsumFile(object):
    
    list_selected_row = None
    gui_settings = None
    file_name = 'STO.ndsum'
    current_folder = None
    
    def __init__(self, parent=None):
        self.parent = parent
        self.current_folder = self.parent.current_folder
        
    def run(self):
        self._retrieve_list_of_selected_rows()
        self._retrieve_gui_settings()
        self._create_sto_output_file()
        
    def _retrieve_list_of_selected_rows(self):
        o_table_handler = TableHandler(parent = self.parent)
        o_table_handler.retrieve_list_of_selected_rows()
        self.list_selected_row = o_table_handler.list_selected_row

    def _retrieve_gui_settings(self):
        _gui_settings = {}
        _gui_settings['background_flag']= self.parent.background_yes.isChecked()
        _gui_settings['background_no_field'] = str(self.parent.background_no_field.text())
        _gui_settings['background_yes_field'] = str(self.parent.background_line_edit.text())
        _gui_settings['muscat_flag'] = self.parent.muscat_yes.isChecked()
        _gui_settings['scale_data_flag'] = self.parent.scale_data_yes.isChecked()
        _gui_settings['run_rmc_flag'] = self.parent.run_rmc_yes.isChecked()
        _gui_settings['plazcek_from'] = str(self.parent.plazcek_fit_range_min.text())
        _gui_settings['plazcek_to'] = str(self.parent.plazcek_fit_range_max.text())
        _gui_settings['bfil_from'] = str(self.parent.fourier_filter_from.text())
        _gui_settings['bfil_to'] = str(self.parent.fourier_filter_to.text())
        self.gui_settings = _gui_settings

    def _create_sto_output_file(self):
        full_file_name = os.path.join(self.current_folder, self.file_name)
        _text = []
        for _entry in self.list_selected_row:
            _text.append(_entry['name'] + ' ' + _entry['runs'] + '\n')

        _text.append('endsamples\n')

        _gui_settings = self.gui_settings
        if _gui_settings['background_flag']:
            _background = _gui_settings['background_yes_field']
        else:
            _background = _gui_settings['background_no_field']
        _text.append('Background\t' + _background + '\n')        

        if _gui_settings['muscat_flag']:
            _muscat_flag = 'Yes'
        else:
            _muscat_flag = 'No'
        _text.append('muscat\t' + _muscat_flag + '\n')
        
        _bfil = "bfil \t%s,%s\n" %(_gui_settings['bfil_from'], _gui_settings['bfil_to'])
        _text.append(_bfil)
        
        if _gui_settings['scale_data_flag']:
            _scale_data = "Yes"
        else:
            _scale_data = "No"
        _text.append("scale_data \t%s\n" %_scale_data)
        
        if _gui_settings['run_rmc_flag']:
            _run_rmc = "Yes"
        else:
            _run_rmc = "No"
        _text.append("run_rmc \t%s\n" %_run_rmc)
        
        _plazcek = "plarange \t%s,%s\n" %(_gui_settings['plazcek_from'], _gui_settings['plazcek_to'])
        _text.append(_plazcek)

        f = open(full_file_name, 'w')
        for _line in _text:
            f.write(_line)
        f.close()

        
        
        
        
        
        
        