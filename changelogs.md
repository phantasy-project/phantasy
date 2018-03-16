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
