Version 0.1.0
-------------

2017-02-03 [Testing]

Major changes:

- New package name, `PHANTASY`: Physics High-level Applications and Toolkits for
  Accelerator System.

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
