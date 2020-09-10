from __future__ import (absolute_import)

import os
from qtpy.QtWidgets import (QMessageBox, QFileDialog)

from addie.utilities import math_tools


class IsRepGuiTableInitialization(object):
    _script = "/SNS/users/zjn/pytest/FOD.py"
    _cmd = "/usr/bin/python {}".format(_script)
    _fod_filename = "fod.inp"

    def __init__(self, parent=None):
        self.parent = parent
        self.parameters={}
        self.sample_info = {
            "sample_1":{
                "formula": '',
                "radius": '',
                "md": '',
                "pf": '',
                "ss": 0,
                "abs": 0
                },
            "sample_2":{
                "formula": '',
                "radius": '',
                "md": '',
                "pf": '',
                "ss": 0,
                "abs": 0
                }
            }

    def _is_table_input_valid(self):
        '''
        Validate the table input
        :return: True if all checks are valid, False otherwise
        :rtype: bool
        '''
        # sample one title
        if not self.parent.ui.sample_1_title.text().strip():
            self.err_messenger("'Sample-1 Title' missing!")
            return False

        # sample two title
        if not self.parent.ui.sample_2_title.text().strip():
            self.err_messenger("'Sample-2 Title' missing!")
            return False

        # background title
        if not self.parent.ui.bkg_title.text().strip():
            self.err_messenger("'Background Title' missing!")
            return False

        # background scans
        back_scans = self.parent.ui.bkg_scans.text().strip()
        if not back_scans:
            self.err_messenger("'Background Scans' missing!")
            return False

        if not math_tools.is_int(back_scans):
            self.err_messenger("'Background Scans' not integer")
            return False

        # sample one scans
        sample_1_scans = self.parent.ui.sample_1_scans.text().strip()
        if not sample_1_scans:
            self.err_messenger("'Sample-1 Scans' missing!")
            return False

        sample_1_scans_list = sample_1_scans.split("-")
        for scan in sample_1_scans_list:
            if not math_tools.is_int(scan):
                msg = "One of 'Sample-1 Scans' is not integer: {}".format(scan)
                self.err_messenger(msg)
                return False

        if len(sample_1_scans_list) > 2:
            msg = "'Sample-1 Scans' format is <min>-<max>, too many '-'"
            self.err_messenger(msg)
            return False

        if len(sample_1_scans_list) == 2:
            if int(sample_1_scans_list[0]) >= int(sample_1_scans_list[1]):
                msg = "'Sample-1 Scans' is not monotonically increasing"
                self.err_messenger(msg)
                return False

        # sample two scans
        sample_2_scans = self.parent.ui.sample_2_scans.text().strip()
        if not sample_2_scans:
            self.err_messenger("'Sample-2 Scans' missing!")
            return False

        sample_2_scans_list = sample_2_scans.split("-")
        for scan in sample_2_scans_list:
            if not math_tools.is_int(scan):
                msg = "One of 'Sample-2 Scans' is not integer: {}".format(scan)
                self.err_messenger(msg)
                return False

        if len(sample_2_scans_list) > 2:
            msg = "'Sample-2 Scans' format is <min>-<max>, too many '-'"
            self.err_messenger(msg)
            return False

        if len(sample_1_scans_list) == 2:
            if int(sample_2_scans_list[0]) >= int(sample_2_scans_list[1]):
                msg = "'Sample-2 Scans' is not monotonically increasing"
                self.err_messenger(msg)
                return False

        # secondary scattering ratio
        ratio = self.parent.ui.secondary_scattering_ratio.text().strip()
        if not ratio:
            self.err_messenger("'Secondary Scattering Ratio' missing!")
            return False

        if not math_tools.is_float(ratio):
            msg = "'Secondary Scattering Ratio is not a float: {}".format(ratio)
            self.err_messenger(msg)
            return False

        # plazcek
        cond1 = self.parent.ui.plazcek_fit_range_min.text().strip()
        cond2 = self.parent.ui.plazcek_fit_range_max.text().strip()
        if not cond1 or not cond2:
            self.err_messenger("Plazcek info incomplete!")
            return False

        # substitution
        cond1 = self.parent.ui.subs_init.text().strip()
        cond2 = self.parent.ui.subs_rep.text().strip()
        if not cond1 or not cond2:
            self.err_messenger("Substitution info incomplete!")
            return False

        # fourier transform
        cond1 = self.parent.ui.ft_qrange.text().strip()
        cond2 = self.parent.ui.ff_rrange.text().strip()
        cond3 = self.parent.ui.ff_qrange.text().strip()
        if not cond1 or not cond2 or not cond3:
            self.err_messenger("Fourier transform info incomplete!")
            return False

        return True

    def _is_info_in_sample_table(self):
        sample_1_row = -1
        for _row_index in range(self.parent.parent.postprocessing_ui.table.rowCount()):
            _item = self.parent.parent.postprocessing_ui.table.item(_row_index, 1)
            if _item is not None:
                title_temp = str(_item.text())
                title_1 = self.parent.ui.sample_1_title.text().strip()
                if title_temp == title_1:
                    sample_1_row = _row_index
                    break
        if sample_1_row >= 0:
            self.sample_info['sample_1']['formula'] = str(self.parent.parent.postprocessing_ui.table.item(sample_1_row, 3).text())
            self.sample_info['sample_1']['md'] = str(self.parent.parent.postprocessing_ui.table.item(sample_1_row, 4).text())
            self.sample_info['sample_1']['radius'] = str(self.parent.parent.postprocessing_ui.table.item(sample_1_row, 5).text())
            self.sample_info['sample_1']['pf'] = str(self.parent.parent.postprocessing_ui.table.item(sample_1_row, 6).text())
            _widget = self.parent.parent.postprocessing_ui.table.cellWidget(sample_1_row, 7)
            if _widget.currentIndex() == 0:
                self.sample_info['sample_1']['ss'] = 'cylindrical'
            else:
                self.sample_info['sample_1']['ss'] = 'spherical'
            _widget = self.parent.parent.postprocessing_ui.table.cellWidget(sample_1_row, 8).children()[1]
            if _widget.checkState() == 0:
                self.sample_info['sample_1']['abs'] = 'nogo'
            else:
                self.sample_info['sample_1']['abs'] = 'go'
            if self.sample_info['sample_1']['formula'].strip() is '':
                self.err_messenger("Formula for sample-1 missing! Check the sample table!")
                return False
            if self.sample_info['sample_1']['md'].strip() is '':
                self.err_messenger("Mass density for sample-1 missing! Check the sample table!")
                return False
            if self.sample_info['sample_1']['radius'].strip() is '':
                self.err_messenger("Container radius for sample-1 missing! Check the sample table!")
                return False
            if self.sample_info['sample_1']['pf'].strip() is '':
                self.err_messenger("Packing fraction for sample-1 missing! Check sample table!")
                return False
        else:
            self.err_messenger("Title not found in sample table for sample-1! Check sample table!")
            return False

        sample_2_row = -1
        for _row_index in range(self.parent.parent.postprocessing_ui.table.rowCount()):
            _item = self.parent.parent.postprocessing_ui.table.item(_row_index, 1)
            if _item is not None:
                title_temp = str(_item.text())
                title_1 = self.parent.ui.sample_2_title.text().strip()
                if title_temp == title_1:
                    sample_2_row = _row_index
                    break
        if sample_2_row >= 0:
            self.sample_info['sample_2']['formula'] = str(self.parent.parent.postprocessing_ui.table.item(sample_2_row, 3).text())
            self.sample_info['sample_2']['md'] = str(self.parent.parent.postprocessing_ui.table.item(sample_2_row, 4).text())
            self.sample_info['sample_2']['radius'] = str(self.parent.parent.postprocessing_ui.table.item(sample_2_row, 5).text())
            self.sample_info['sample_2']['pf'] = str(self.parent.parent.postprocessing_ui.table.item(sample_2_row, 6).text())
            _widget = self.parent.parent.postprocessing_ui.table.cellWidget(sample_2_row, 7)
            if _widget.currentIndex() == 0:
                self.sample_info['sample_2']['ss'] = 'cylindrical'
            else:
                self.sample_info['sample_2']['ss'] = 'spherical'
            _widget = self.parent.parent.postprocessing_ui.table.cellWidget(sample_2_row, 8).children()[1]
            if _widget.checkState() == 0:
                self.sample_info['sample_2']['abs'] = 'nogo'
            else:
                self.sample_info['sample_2']['abs'] = 'go'
            if self.sample_info['sample_2']['formula'].strip() is '':
                self.err_messenger("Formula for sample-1 missing! Check the sample table!")
                return False
            if self.sample_info['sample_2']['md'].strip() is '':
                self.err_messenger("Mass density for sample-1 missing! Check the sample table!")
                return False
            if self.sample_info['sample_2']['radius'].strip() is '':
                self.err_messenger("Container radius for sample-1 missing! Check the sample table!")
                return False
            if self.sample_info['sample_2']['pf'].strip() is '':
                self.err_messenger("Packing fraction for sample-1 missing! Check sample table!")
                return False
        else:
            self.err_messenger("Title not found in sample table for sample-1! Check sample table!")
            return False

        return True

    def load_fod_input(self):
        _current_folder = self.parent.parent.current_folder
        [_table_file, _] = QFileDialog.getOpenFileName(
            parent=self.parent,
            caption="Input inp File",
            directory=_current_folder,
            filter=("inp files (*.inp);; All Files (*.*)"))

        if not _table_file:
            return

        try:
            fod_inputs = open(_table_file, "r")
        except IOError:
            self.err_messenger("Permission denied! Choose another input file!")
            return

        lines = fod_inputs.readlines()
        fod_inputs.close()

        for line in lines:
            try:
                if line.strip():
                    self.parameters[line.split('#')[1].strip()]=line.split('#')[0].strip()
            except IndexError:
                pass

        try:
            self.parent.ui.sample_1_title.setText(self.parameters['sample_1_title'])
            self.parent.ui.sample_2_title.setText(self.parameters['sample_2_title'])
            self.parent.ui.bkg_title.setText(self.parameters['background_title'])
            self.parent.ui.bkg_scans.setText(self.parameters['background scannrs'])
            self.parent.ui.sample_1_scans.setText(self.parameters['sample_1_scannrs'])
            self.parent.ui.sample_2_scans.setText(self.parameters['sample_2_scannrs'])
            self.parent.ui.secondary_scattering_ratio.setText(self.parameters['secondary_scattering_ratio'])
            self.parent.ui.plazcek_fit_range_min.setText(self.parameters['pla_range'].split(',')[0].strip())
            self.parent.ui.plazcek_fit_range_max.setText(self.parameters['pla_range'].split(',')[1].strip())
            if ',' in self.parameters['substitution_type']:
                self.parent.ui.subs_init.setText(self.parameters['substitution_type'].split(',')[0].strip())
                self.parent.ui.subs_rep.setText(self.parameters['substitution_type'].split(',')[1].strip())
            elif '/' in self.parameters['substitution_type']:
                self.parent.ui.subs_init.setText(self.parameters['substitution_type'].split('/')[0].strip())
                self.parent.ui.subs_rep.setText(self.parameters['substitution_type'].split('/')[1].strip())
            self.parent.ui.ft_qrange.setText(self.parameters['qrangeft'])
            self.parent.ui.ff_rrange.setText(self.parameters['fourier_range_r'])
            try:
                self.parent.ui.ff_qrange.setText(self.parameters['fourier_range_q'])
            except KeyError:
                self.parent.ui.ff_qrange.setText(self.parameters['fourier_range_Q'])

        except (IndexError, KeyError):
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText("Error in FOD input file!")
            msgBox.setWindowTitle("Error")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec_()
            return

        return

    def err_messenger(self, message):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Critical)
        msgBox.setText(message)
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
        return

    def save_fod_input(self):
        valid = self._is_table_input_valid()
        if not valid:
            return

        _current_folder = self.parent.parent.current_folder
        [_out_file, _] = QFileDialog.getSaveFileName(
            parent=self.parent,
            caption="Output inp File",
            directory=_current_folder,
            filter=("inp files (*.inp);; All Files (*.*)"))

        if not _out_file:
            return

        try:
            fod_file_contents = self.create_fod_file()
            with open(_out_file, "w") as fod_output:
                fod_output.write(fod_file_contents)
        except IOError:
            self.err_messenger("Permission denied! Choose another save target!")
            return
        return

    def save_and_run_fod_input(self):
        '''
        Save FOD .inp file and run via job monitor
        '''
        valid = self._is_table_input_valid()
        if not valid:
            return

        valid = self._is_info_in_sample_table()
        if not valid:
            return

        _current_folder = self.parent.parent.current_folder
        working_dir = QFileDialog.getExistingDirectory(
            self.parent,
            "Select Working Directory",
            _current_folder,
            QFileDialog.ShowDirsOnly)

        if not working_dir:
            return

        fod_path = os.path.join(working_dir, self._fod_filename)
        try:
            fod_file_contents = self.create_fod_file()
            with open(fod_path, "w") as fod_output:
                fod_output.write(fod_file_contents)
        except IOError:
            self.err_messenger("Permission denied! Choose another working folder!")
            return

        sample_1_title = self.parent.ui.sample_1_title.text().strip()
        sample_1_ini_path = os.path.join(working_dir, sample_1_title + '.ini')
        try:
            sample_1_ini_contents = self.create_sample_ini_file(sample_1_title, self.sample_info['sample_1'])
            with open(sample_1_ini_path, "w") as sample_1_ini_out:
                sample_1_ini_out.write(sample_1_ini_contents)
        except IOError:
            self.err_messenger("Permission denied! Choose another working folder!")
            return

        sample_2_title = self.parent.ui.sample_2_title.text().strip()
        sample_2_ini_path = os.path.join(working_dir, sample_2_title + '.ini')
        try:
            sample_2_ini_contents = self.create_sample_ini_file(sample_2_title, self.sample_info['sample_2'])
            with open(sample_2_ini_path, "w") as sample_2_ini_out:
                sample_2_ini_out.write(sample_2_ini_contents)
        except IOError:
            self.err_messenger("Permission denied! Choose another working folder!")
            return

        if not os.path.isfile(self._script):
            msg = "Unable to find run script: {}".format(self._script)
            self.err_messenger(msg)
            return

        os.chdir(working_dir)
        script_to_run = self._cmd + ' -f ' + fod_path
        main_gui = self.parent.parent
        main_gui.launch_job_manager(
            job_name="Isotope Substitution",
            script_to_run=script_to_run)
        return

    def create_fod_file(self):
        '''
        Creates FOD file input as string to write to output file handle
        :return: FOD file input to save to file handle
        :rtype: str
        '''
        out_string = (
            "{sample_one_title}  # sample_1_title\n"
            "{sample_two_title}  # sample_2_title\n"
            "{background_title}  # background_title\n"
            "{background_scans}  # background scannrs\n"
            "{sample_one_scans}  # sample_1_scannrs\n"
            "{sample_two_scans}  # sample_2_scannrs\n"
            "{sub_init} / {sub_replace}  # substitution_type\n"
            "{plazcek_type}  # pla_type\n"
            "{plazcek_min}, {plazcek_max}  # pla_range\n"
            "{qrangeft}  # qrangeft\n"
            "{fourier_range_r}  # fourier_range_r\n"
            "{fourier_range_q}  # fourier_range_Q\n"
            "{ratio}  # secondary_scattering_ratio"
        )

        kwargs = {
            "sample_one_title": self.parent.ui.sample_1_title.text(),
            "sample_two_title": self.parent.ui.sample_2_title.text(),
            "background_title": self.parent.ui.bkg_title.text(),
            "background_scans": self.parent.ui.bkg_scans.text(),
            "sample_one_scans": self.parent.ui.sample_1_scans.text(),
            "sample_two_scans": self.parent.ui.sample_2_scans.text(),
            "sub_init": self.parent.ui.subs_init.text(),
            "sub_replace": self.parent.ui.subs_rep.text(),
            "plazcek_type": str(self.parent.ui.ndeg.value()),
            "plazcek_min": self.parent.ui.plazcek_fit_range_min.text(),
            "plazcek_max": self.parent.ui.plazcek_fit_range_max.text(),
            "qrangeft": self.parent.ui.ft_qrange.text(),
            "fourier_range_r": self.parent.ui.ff_rrange.text(),
            "fourier_range_q": self.parent.ui.ff_qrange.text(),
            "ratio": self.parent.ui.secondary_scattering_ratio.text()
        }

        return out_string.format(**kwargs)

    def create_sample_ini_file(self, sample_title, sample_info):
        '''
        Creates sample ini file input as string to write to output file handle
        :return: sample ini file input to save to file handle
        :rtype: str
        '''
        out_string = (
            "{sample_title}  # sample title\n"
            "{sample_formula}  # # sample formula\n"
            "{mass_density}  # mass density\n"
            "{radius}  # radius\n"
            "{packing_fraction}  # packing fraction\n"
            "{sample_shape}  # sample shape\n"
            "{absorption_corr}  # do abskorr in IDL"
        )

        kwargs = {
            "sample_title": sample_title,
            "sample_formula": sample_info['formula'],
            "mass_density": sample_info['md'],
            "radius": sample_info['radius'],
            "packing_fraction": sample_info['pf'],
            "sample_shape": sample_info['ss'],
            "absorption_corr": sample_info['abs']
        }

        return out_string.format(**kwargs)

    def iso_rep_linker(self):
        self.parent.ui.load_fod_input_button.clicked.connect(self.load_fod_input)
        self.parent.ui.save_fod_input_button.clicked.connect(self.save_fod_input)
        self.parent.ui.save_and_run_fod_input.clicked.connect(self.save_and_run_fod_input)
        return
