Element with
`Channel Access <https://epics.anl.gov/base/R3-16/1-docs/CAproto/index.html>`_
support is instantiated from :class:`~phantasy.CaElement`, which in
aggregate attaches relevant information with the target device.

From the user side, interested information of the element can be reached by
referring the attributes, which are composed of static and dynamic fields,
the static fields are to represent the device properties that do not change
often, especially the attribute name itself in Python object, e.g. device
name, type, geometry length and location, etc., while the dynamic fields are
to represent the device properties regarding to Channel Access ability, that
is:

1. The attribute name is not fixed, depends on the device configuration;
2. The value of the attribute usually is not fixed, depends on the runtime;
3. Each dynamic field is instantiated from :class:`~phantasy.CaField`.
