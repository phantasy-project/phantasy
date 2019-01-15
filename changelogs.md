Version 1.8.0
-------------
2019-01-14

- Fix csv stream next() compatibility with Python 3
- Create a new app: Settings Manager

Version 1.7.2
-------------
2019-01-14

- Correlation Visualizer App:
  - Fix default MPS status PV name (FRIB)
  - Fix static element name in ElementWidget display, which introduces changes to phantasy core
  - [Testing] Add routine to process DAQ when device is wire-scanner

- Wire Scanner App:
  - Refactor sync results to IOC to the method of PMData

- Core of phantasy:
  - Add 'ename' as the alias of 'name' for BaseElement class

Version 1.7.1
-------------
2019-01-14

- Correlation Visualizer App:
  - Support scan against high-level elements
  - Unified APIs for PVElement(Readonly) and CaField
  - Updated UI
- Wire Scanner App:
  - Fix DAQ when working with real devices
  - Updated UI

Version 1.7.0
-------------
2019-01-11

- Wire Scanner App:
  - Support offine data analysis, load/save data
  - Configuration file management
  - Unified data interface
  - other features
- Bug fixes and improvement

Version 1.6.5
-------------
2019-01-02

- Implement data interface for wire-scanner app (testing)

Version 1.6.4
-------------
2018-11-10

- Correlation Visualizer App:
  - Array Set: Support sorting
  - Fix app crashes by None array 

Version 1.6.3
-------------
2018-11-09

- FLAME VA: Add support for MPS status control
- VA Launcher App: Support MPS status simulation control
- Correlation Visualizer App: Support Pause scan by MPS
- Initial ORM app
- Other fixes

Version 1.6.2
-------------
2018-11-07

- FIX: Tests configuration files after re-introducing 'config' keyword
  argument to 'load_lattice' function.

Version 1.6.1
-------------
2018-11-06

- MNT: Bump up version to 1.6.1.
- MNT/CV: Bump up version to 2.2.
- ENH/CV: Array set dialog supports updating array by edit text.
- UI/CV: Array set dialog update, textEdit readonly off.
- STY: Clean up and reformat.
- UI/TV: Update frame background color.
- ENH/VA: Noise slider is synced when pv is changed externally.
- UI/VA: Set initial noise slider 0 and disable widgets.
- FIX: PV prefix for NOISE, CNT and CHARGE channels.
- ENH/VA: Implement CA localhost only option.
- UI/VA: Add checkbox to limit CA localhost only.
- ENH/VA: Implement PV prefix option of VA configuration.
- FIX: VA info crashes when switching VA.
- ENH: Update create lattice function to support pvprefix.
- ENH: Add 'prefix' key arg to MachinePortal for specified pv prefix.
- FIX: Do not prefix when prefix found from the orignal channels.
- ENH: flame VA support '--pv-prefix' to prefix channels with any string.
- ENH: Add '--pv-prefix' argument for flame-vastart.
- ENH/VA: Set PHANTASY_CONFIG_DIR if not set.
- ENH: Set PHANTASY_CONFIG_DIR for all apps if not set.
- MNT/VA: Bump up version to 1.1.
- ENH/VA: Add notebook templates for Notebook launch button.
- FIX/VA: Open ipynb file if existing.
- FIX: Make PHANTASY_CONFIG_DIR configurable during runtime.
- FIX/VA: Fix va info widget size.
- ENH/VA: Set up environment vars for va process.
- MNT: Add launcher and icon for VA launcher app.

Version 1.6.0
-------------
2018-11-02

- Correlation Visualizer App:
  - MNT/CV: Bump up version to 2.1.
  - UI/CV: Generate py file from ui with pyuic5 5.5.1.
  - UI/CV: Make plainText widget of Set array widget readonly.
  - UI/CV: Add chkbox to turn on/off arbitary alter array option.
  - ENH/CV: Support arbitary alter array input.
  - ENG/CV: Add implementation of extra monitors view.
  - UI/CV: Add widget for extra monitors view.
  - ENH/CV: Change delimiter to tab when saving data into csv.
  - ENH/CV: Clear the startup template curve.
  - ENH/CV: Save extra monitor data into csv table.
  - ENH/CV: Return all avg and stderr array from ScanDataModel.
  - ENH/CV: Record readings of extra monitors to scan task.
  - UI/CV: Update widgets for extra monitors.
  - ENH/CV: Implement the logic to add extra monitors.
  - ENH/CV: Add method to remove extra monitor from scan task.
  - UI/CV: Fix view_selected_pts_tbtn popup mode.
  - MNT/CV: Clean import section and manage icon size by macro.
  - UI/CV: Add text label for all tool buttons.
  - ENH/CV: Implement view_selected_pts_tbtn for RETAKE.
  - UI/CV: Add icon for show retake points tool button.
  - UI/CV: Make scan event log font bold.
  - ENH/CV: Implement RETAKE feature.
  - FIX: Include the end valule of arange when building a array.
  - FIX: Not disable element selection mode when PV mode is enabled.
  - FIX: When lattice is loaded, but not shown in elem selection widget.
  - FIX: PV connection should be checked by PV.connected attr.
  - ENH: Add keyboard shortcut ESC to close points viewer.
  - ENH: Note on_select_points slot which accepts ind,pts from lasso tool.
  - ENH: Update event log for button clicking.
  - ENH: Add color: COLOR_PRIMARY, for button clicking event log.
  - ENH: Implement update button for points viewer widget.
  - UI: Add Update button for tableWidget refreshing.
  - UI: Set buttons autodefault.
  - ENH: Adjust points view widget size.
  - ENH: Use delete toolbutton to delete selected point.
  - UI: Auto fit tableWidget size regarding contents.
  - UI: Update tab order.
  - ENH: Points for retaking could be visually selected/deselected.
  - ENH: Add widget for viewing selected points for RETAKE.
  - BUG: Fix get_save_filename crashes when nothing is selected.
  - ENH: Add 'index_array' to ScanWorker to support RETAKE.
  - BUG: Fix issues that crash app when click buttons when no scan is running.

- VA Launcher App:
  - UI/VA: Update window size.
  - ENH/VA: Make toolbuttons size as 32x32.
  - ENH/VA: Update icons for notebook and va info button.
  - UI/VA: Add widget for va info.
  - UI/VA: Update layout.
  - UI/VA: Add icon for va info btn.
  - UI/VA: Add icons for notebook run/stop.
  - ENH/VA: Implement toolbar for run/stop VA.
  - UI/VA: Update layout and use toolbar for run/stop VA.
  - FIX/VA: Capture process stop exception when shown va info.
  - ENH/VA: Add icons for run/stop toolbutton.
  - UI/VA: Add slot for clicking Notebook button.
  - ENH/VA: Add app icon for VA launcher.
  - MNT/VA: Bump up version to 1.0.
  - MNT/VA: Update about info.
  - ENH/VA: Implement noise level slider.
  - ENH/VA: Add ESC keyshort to exit vainfo widget.
  - UI/VA: Add slider to contorl VA noise level.
  - ENH/VA: New module for va info widget.
  - ENH/VA: Add more tools buttons, enhanced start/stop logic.
  - UI/VA: Update layout.
  - ENH: Add function to convert seconds to uptime string.
  - UI/VA: Update layout.
  - ENH/VA: Implement RUN and STOP button.
  - ENH: Changed moveto and set toolbutton to make use of cross-ruler.
  - MNT: Add entry point for va_launcher.
  - ENH/VA: Initial virtual accelerator launcher app.

Version 1.5.0
-------------
2018-10-23

- Correlation Visualizer 2.0:
  - Run scan work on another thread
  - Support Pause and Resume
  - Improved scan event log system
  - Improved element selection
  - Improved scan range setting
  - Features more tool buttons
  - Bugs fixed

Version 1.4.4
-------------
2018-10-19

- Applied improvements to GUI apps.
- Fixed bugs.

Version 1.4.0
-------------
2018-10-12 [Testing]

- First release for GUI apps:
  - Quad scan
  - Correlation Visualizer
- Initiate data sheet for output data
- Testing wire-scanner device class

Version 1.3.0
-------------
2018-09-26 [Testing]

- Initial a new app: 'Correlation Visualizer'
- Enhanced 'Trajectory Viewer' app with version of 1.1
  - Apply default figure style settings at start up
- Enhanced orbit correction with ORM
  - Create a new function: 'get_index_grid' to get sub matrix from ORM
- Fix matplotlib issues regarding to 1.x and 2.x incompatibilities

Version 1.2.0
-------------
2018-09-14 [Testing]

- New PyQt5 with Python 3.x apps:
  - Trajectory Viewer: first release, with system menu item
  - Lattice Viewer: initiated, WIP
- Add generated HTML documentation into source branch

Version 1.0.7
-------------
2018-08-17 [Testing]

- Python 3 compatibilities:
  - Convert dict.keys() and dict.items() to list
  - Write file with 'w' option  
- Virtual accelerator (FLAME):
  - FIX: add back BPM energy field
  - ENH: add new option '-l' to `flame-vastart` to run IOC localhost only

Version 1.0.6
-------------
2018-08-16 [Testing]

- Fix the compatibility issue regarding to the unicorn data
  - For old unicorn data: xydata columns indices are 4 and 5.

Version 1.0.5
-------------
2018-08-15 [Testing]

- `unicorn_app`:
  - Add button 'Start with Browser' to 'Advance' tab
  - Add `Help` menu action

Version 1.0.4
-------------
2018-08-10 [Testing]

- Add menu entry for `unicorn_app`

Version 1.0.3
-------------
2018-08-10 [Testing]

- `unicorn_app`:
  - Default page zoom set to 100%
  - Add an icon
  - Update the about information
  - Automatic start UNICORN web service locally at random port
    between 5000-5050, and terminate at exiting
  - Add a new tab 'Advance' to Preferences for residue services clean up

Version 1.0.2
-------------
2018-08-09 [Testing]

- `unicorn_app`:
  - FIX: Always override unicorn.sqlite file
  - UI: Rename `srv_data_btn` to `srv_db_reset_btn`

Version 1.0.1
-------------
2018-08-09 [Testing]

- ENH: Add new button to initialize UNICORN SQLite data
- ENH: UI

Version 1.0.0
-------------
2018-08-09 [Testing]

- CI: Automatically test and build documentation (HTML and pdf)
- DOC: Major update
- ENH: Add new GUI app: `unicorn_app` (Python 2), `unicorn_app3` (Python 3)

Version 0.9.14
--------------
2018-07-31 [Testing]

- FIX: `lat.get_model_settings` skip element if not in current working lattice

Version 0.9.13
-------------
2018-07-26 [Testing]

- ENH: Set 'handle' with default value.
- ENH: Add 'timeout' to CaField.get() for const.

Version 0.9.12
-------------
2018-07-25 [Testing]

- ENH,API: More feature to the `CaField.get()`.
- ENH: New functions for get value from PV.

Version 0.9.11
-------------
2018-07-25 [Testing]

- PY3: Fix dict keys() compatibility.

Version 0.9.10
-------------
2018-07-25 [Testing]

- ENH:
  - `MachinePortal` instance mark the current working lattice with `*`
  - `CaField.get`: new option to return timestamp
  - Add support to model FC and BCM
  - Add `--soffset` option to `frib-channels` tool
- BUG:
  - Ensure parsed tag as list type
- Changes:
  - Remove energy field from BPM element

Version 0.9.9
-------------
2018-07-18 [Testing]

- Add command `test_phantasy` for testing
- Use `entry_points` rather than `scripts`
- Fix issue of not cleaning up after testing
- Fix issue of write permission when testing

Version 0.9.8
-------------
2018-07-17 [Testing]

- Fix Python 3.x compatibilities for Debian packaging
- Sort out the install-depends for `pip`
- Add tests folder into package

Version 0.9.7
-------------
2018-07-06 [Testing]

- Now support both Python 2.7 and Python 3.x
- Unittest can be ran by `python setup.py test`
- Bugs fixed

Version 0.9.6
-------------
2018-07-02 [Testing]

- MNT: Remove README.rst and update README.md.
- ENH: Add method 'get_model_settings' to Lattice.

Version 0.9.5
-------------
2018-06-29 [Testing]

- ENH: Rename machine example to demo_mconfig/accel.
- ENH: Install demo mach into /etc/phantasy/config.
- ENH: Make example machine config usage conditional.
- ENH: Make scan module optional.
- ENH: Make channelfinder module optional.
- FIX: Logging level issue an typo.
- FIX: Change the data path for tests.

Version 0.9.4
-------------
2018-05-23 [Testing]

- DOC: Add entries for new notebook files.
- DOC: Add notebooks.
- ENH: Add plot_orbit tool to work with FLAME model.
- ENH: Add option 'flame_cor_gauge' to corrector.
- ENH: Generate settings with physics field values.
- ENH: Add _unicorn_e2p and _unicorn_p2e to Element.
- ENH: Add methods to test field type.
- FIX: CaField duplicated PV objects.
- FIX: CaField duplicated PV names.
- ENH: Add ftype (field type) attribute to CaField.

Version 0.9.3
-------------
2018-05-15 [Testing]

- MNT: Remove files regarding to Travis CI.
- FIX: pv_policy is a str when passing to process_pv.
- TST: Adapt the tests regarding to phantasy source.
- FIX: Use physics fields for BPM element.
- ENH: Generate settings from physics fields.
- ENH: Update VA settings from physics fields.
- ENH: Read settings from physics fields.
- ENH: Seperate into ENG and PHY fields for channels.
- FIX: If 'unicorn_file' is missing, use default law.
- FIX: Get channels according to 'elemField_eng'.
- FIX: Get unicorn functions with element name.
- ENH: Integrate unicorn policy when processing PVs.
- ENH: Update routine to integrate physics field.
- NEW: Replace elemField with elemField_eng[_phy].
- ENH: Add physics field names for each elements.
- ENH: Update 'process_pv' for element generation.
- ENH: Support 'unicorn_file' when loading lattice.
- ENH: Add unicorn decorators into package.
- ENH: decorators for pv_policy with scaling laws.

Version 0.9.2
-------------
2018-05-02 [Testing]

- FIX: Update BPM field PVs according to FRIB setup.
- ENH: Add MAG dynamic field for BPM.
- CI: Set up Circle CI.

Version 0.9.1
-------------
2018-05-01 [Testing]

- ENH: Rename x(y) -> x(y)cen and add cxy for PM.
- ENH: Add xy correlation for profile monitor.
- ENH: Update profile monitor pv names.
- DOC: Attach pdf doc.
- ENH: Support XLS lattice file dated 2018-01-25.

Version 0.9.0
-------------
2018-04-09 [Testing]

- DOC: Update index page.
- DOC: Add work_with_save_restore notebook.
- Fix caget large waveform record issue.
- ENH: Add snapshot-settings to phytool.
- ENH: Add new cmd 'snapshot-settings' to read .snp.
- ENH: Add support to read settings from snp file.
- Add support to load settings into Lattice.
- Default design/last settings: {field: None}.
- Initialize elem design_settings from settings file.
- Add keyword arguments to pv policy functions.
- Add tests for lattice load_settings.
- Add design_settings and last_settings attribute.
- Initialize design settings for all elements.
- Enable try except block.
- Fix compatibility with Python 3.
- Show warning message if wait flag is True when set.
- Set wait as default True and add ename for CaField.
- Add attributes to control put action of CaField.
- Add keyword arguments to all policy functions.
- Add set_loglevel to control level of log system.
- Add sphinx_rtd_theme as deps.
- Use rtd theme.

Version 0.8.1
-------------
2018-03-27 [Testing]

- Fix: get field from 'control' environment.

Version 0.8.0
-------------
2018-03-27 [Testing]

- New:
    - len() method for high-level lattice
    - Logging message level control
    - Property: `pvPolicy` for channels
    - CaField: new methods: `reset_policy`
    - CaField: update element to support multi-PVs for one handle
    - CaField: new attributes: `read_policy`/`write_policy`
    - Module for PV policy: `DEFAULT`, `EQUAD`, `EBEND`

- Update:
    - Implement all element config into `apply_config` method
    - Replace append with insert operation for high-level lattice class
    - Make repr of lattice more fast
    - Default `cfs_property_name` changed to be `*`
    - CaField: get() will return list instead of scalar

- Tools:
    - frib_channels: new option `--pspvfile` to generate PS channels based on given pspvfile.

- CI:
    - New docker image (tonyzhang/phantasy-ioc) as a soft-ioc container for PV testing
    - set random noise to 0 by PV: 'fac'
    - Add new deps
    - Makefile rule to start/stop phantasy-ioc container

- Config:
    - Update LEBT configuration with new channels

Test:
    - New test for generating layout from xlsx file
    - New test for CaElement/CaField  
    - New test data

Clean:
    - Remove debian directory from source branch
    - Unused functions

Version 0.7.7
-------------
2018-03-16 [Testing]

- Fix: PM type
- Fix: default machine configurations
- New: way to control logging message display level


Version 0.7.6
-------------
2018-03-15 [Testing]

- New:
  - New elements: SlitElement, ApertureElement, AttenuatorElement, DumpElement, ChopperElement
  - Drift has specific names, rule: `SYSTEM_SUBSYSTEM:DEVICE_DFT_D####_#`
- Fixed:
  - Apply effective length when switching subsystem
  - Center position when shrinking/expanding element
- Updated:
  - Virtual accelerator
  - Channel/layout generation
- Changed:
  - All features provided by 'flameutils' module is imported from another external Python package: `flame_utils`
  - Unittests for flameutils have been deleted


Version 0.7.2-0.7.5
-------------
2018-02-27 [Testing]

- Fix channel names
- Add LEBT tag to machine configuration
- Support effective length for solenoid and equad


Version 0.7.1
-------------
2017-12-21 [Testing]

- Update default machine configurations


Version 0.7.0
-------------
2017-10-27 [Testing]

- Fix bugs.
- New changes to generate machine configuration for real FRIB LINAC.
- New moduel for default machine configuration within package.
- New support for 'Generic' type cavity [FLAME].
- New configurable feature to mask device as drift.


Version 0.6.0
-------------
2017-05-31 [Testing]

- Fix docstrings after API changes.
- Fix FLAME settings for sextupole element.
- Fix 'fields' is attribute instead of method now.
- New physics module: orm for orbit correction.
- New attribute 'orm', correct orbit by orm method.
- Fix bugs.


Version 0.5.1
-------------
2017-05-24 [Testing]

- New put() and get() for CaField.
- New Unitests for element/lattice,machine config.
- New Refactor methods from MachinePortal.
- New Keyword 'pv_data' for element initialization.
- New Keyword 'sort' to create_lattice.
- Fix Compatibility.
- Fix 'simplify_data' supports single PV record.
- New CFS fields: *physicsName* and *physicsType*.
- Refactor CaElement.
- Refactor element module with CA support.
- API changed:
  - CaElement: fields() -> fields


Version 0.4.0
-------------
2017-05-08 [Testing]

- Support sextupole modeling in FLAME VA.
- Fix PM incorrect field values for XY and XYRMS.


Version 0.3.0
-------------
2017-04-18 [Testing]

- Support wire-scanner modeling and data analysis.
- Application utilities are included in 'phantasy.apps',
however provided by another package called 'python-phantasy-apps'.


Version 0.2.0
-------------
2017-02-22 [Testing]

- Support modeling LEBT segment of front-end of FRIB linac.
- New configurations from "FRIB_FE", which is in "machines" repo.


Version 0.1.0
-------------
2017-02-03 [Testing]

- New package name, `PHANTASY`: Physics High-level Applications and Toolkits for Accelerator System.
- Refactoring the codebase of previously known as `phyhlc` and `phyapps`.
- Uniformed PV channel data source:
  - Uniformed interface provided by `phantasy.pv.DataSource`;
  - Support source types: `CFS`, `SQLite`, `CSV`
  - New version of tool: `cfutil-export` could be used to convert data source
    between any two of these types.
- Update of options of machine configuration file: `phyutil.ini`:
  - Created new modules to build facility-specific configuration file, in
    `phantasy.facility` subpackage, `phyutil.ini` can also be any other names;
  - Option names changed:
    - `submachines` -> `segments`
    - `default_submachine` -> `default_segment`
    - `output_dir` -> `root_data_dir` (directory structure of all the data may
    generated from phantasy is re-organized, now this option does not support
    setting from environment variable.)
  - New option names:
    - `model_data_dir`: directory for model data
    - `cfs_property_names`: Unix shell pattern of property names to get from CFS
- Redefined package/module import rules:
  - Now after `import phantasy`, everything could be reached by `phantasy`;
  - Import different library as standalone namespace, by `from phantasy import
  <lib-name>`, then get regarding classes/funcs by within the namespace of
  `<lib-name>`.
- Created more funcs/classes for the `operation` library, which now can handle
  more high-level lattice related machine tunning tasks, e.g.:
  - Synchronize devices` settings between model (code) and machine (control);
  - Export lattice file directly from high-level lattice, let users to study
    the lattice file, then high-level lattice can take back into the final
    lattice file as new settings to update machine.
  - Roll back to certain set history now is supported.
- Established general interface between machine and physics modeling ecosystem,
  arbitary manipulation is allowed at the model-based tunning stage.
- Scan client is now inherited from ScanClient of scan module
  - Created new datautil to handle data generated from Scan clients.
- Added more scripts (most likely could be found in `phytool`):
  - cfs_start: start channel finder service
  - cfs_stop: stop channel finder service
  - cfs_empty_index: empty index of channel finder service data
  - cfs_build_index: rebuild index of channel finder service data
  - plot_orbit: plot particle orbit from FLAME lattice file
  - correct_orbit: correct beam orbit in a pretty easy way (FLAME lattice file)
- Fixed bugs
- Added docstrings for legacy code
- Added unittests
- Added demo scripts and jupyter notebooks
- Published documentation at https://controls.frib.msu.edu/phantasy/
