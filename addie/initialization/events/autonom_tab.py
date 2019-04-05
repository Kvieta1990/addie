def run(main_window=None):
    main_window.autonom_ui.select_current_folder_button.clicked.connect(main_window.select_current_folder_clicked)
    main_window.autonom_ui.manual_output_folder_field.editingFinished.connect(main_window.manual_output_folder_field_edited)
    main_window.autonom_ui.manual_output_folder.clicked.connect(main_window.output_folder_radio_buttons)
    main_window.autonom_ui.manual_output_folder_button.clicked.connect(main_window.manual_output_folder_button_clicked)
    main_window.autonom_ui.auto_manual_folder.clicked.connect(main_window.output_folder_radio_buttons)
    main_window.autonom_ui.create_folder_button.clicked['bool'].connect(main_window.create_new_autonom_folder_button_clicked)
    main_window.autonom_ui.run_autonom_script.clicked.connect(main_window.run_autonom)
    main_window.autonom_ui.pushButton_2.clicked.connect(main_window.help_button_clicked_autonom)
    main_window.autonom_ui.create_exp_ini_button.clicked.connect(main_window.create_exp_ini_clicked)
