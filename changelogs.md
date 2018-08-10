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
