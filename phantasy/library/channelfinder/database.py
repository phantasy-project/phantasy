"""
Channel finder serice source: database (sqlite)
"""

import getpass
import logging
import os
import sqlite3
from fnmatch import fnmatch

_LOGGER = logging.getLogger(__name__)


class CFCDatabase(object):
    """Channel finder client using SQLite database as service data source.
    CFCDatabase provide uniform interface as ``ChannelFinderClient``, which
    uses real CFS as data source.

    If *db_name* is given, connection to database would be established
    automatically, if *db_name* is further changed, connection would be
    updated or rollback to last connection.

    Parameter *owner* is required by CFS (not by database), if not given,
    use the present login username.

    Parameters
    ----------
    db_name : str
        Name of SQLite database.
    owner : str
        Database owner, login username by default.

    See Also
    --------
    :class:`~channelfidner.ChannelFinderClient`
    """

    def __init__(self, db_name=None, owner=None):
        self._db_name = db_name
        self.owner = owner
        self.dbconn = None
        if db_name is not None:
            try:
                self.conn()
                self.dbconn.execute('SELECT 1 FROM pvs LIMIT 1')
            except:
                _LOGGER.error("Cannot connect to {}.".format(self._db_name))

    @property
    def owner(self):
        """Str: owner of the database."""
        return self._owner

    @owner.setter
    def owner(self, owner):
        if owner is None:
            self._owner = getpass.getuser()
        else:
            self._owner = owner

    @property
    def db_name(self):
        """Str: Filename of database."""
        return self._db_name

    @db_name.setter
    def db_name(self, n):
        try:
            new_conn = sqlite3.connect(n)
            new_conn.execute('SELECT 1 FROM pvs LIMIT 1')
            self._db_name = n
            if self.dbconn is not None:
                self.dbconn.close()
            self.dbconn = new_conn
        except:
            _LOGGER.warning("Cannot establish new connection to {}.".format(n))
            _LOGGER.warning("Rollback to previous one.")
            if os.path.isfile(n):
                os.remove(n)

    def conn(self):
        """Connect to SQLite database.
        """
        self.dbconn = sqlite3.connect(self.db_name)

    def close(self):
        """Close current SQLite db connection.
        """
        self.dbconn.close()

    def find(self, **kwargs):
        """
        Note
        ----
        More complex filter logic is provided in ``get_data_from_db`` and
        ``get_data_from_cf``.

        Keyword Arguments
        -----------------
        name : str
            Unix shell pattern of channel name, default is '*'.

        Returns
        -------
        ret : list(dict)
            List of dict, each dict element is of the format:
            {'name': PV name (str), 'owner': str,
            'properties': PV properties (list(dict)),
            'tags': PV tags (list(dict))]
        """
        if len(kwargs) == 0:
            raise Exception(
                'Incorrect usage: at least one parameter must be specified.')

        channames = kwargs.get("name", "*")
        properties = kwargs.get("property", None)
        tags = kwargs.get("tagName", None)
        sql = """SELECT * FROM pvs JOIN elements__pvs ON pvs.pv_id=elements__pvs.pv_id 
                JOIN elements ON elements__pvs.elem_id=elements.elem_id WHERE """
        querycons = []
        if channames != "*":
            first = True
            channames = channames
            for name in channames.split(","):
                querycons.append(name.replace("*", "%").replace("?", "_"))
                if first:
                    sql += """ (pv like ? """
                    first = False
                else:
                    sql += """ or pv like ? """
            sql += """ ) """
        else:
            sql += " pv like '%' "
        if properties is not None:
            sql += """ and ( """
            first = True
            for prpts in properties:
                for pts in prpts[1].split(","):
                    querycons.append(
                        pts.strip().replace("*", "%").replace("?", "_"))
                    if first:
                        first = False
                    else:
                        sql += """ or """
                    sql += """ {0} like ? """.format(prpts[0])
            sql += """ ) """
        if tags is not None:
            tags = ",".join((tag.strip() for tag in
                             tags.replace("*", "%").replace("?", "_")))
            querycons.append(tags)
            sql += """ and tags like ? """

        # print sql, querycons
        cur = self.dbconn.cursor()
        cur.execute(sql, querycons)

        properties = [prpts[0] for prpts in cur.description]

        return self.convert_data(properties, cur.fetchall(), owner=self.owner)

    @staticmethod
    def convert_data(properties, results, **kws):
        """Covnert raw data to be uniform as ChannelFinderClient

        Parameters
        ----------
        properties : list
            List of all properties, including PV name, PV properties, PV tags, etc.
        results : tuple
            Tuple of values for each properties.

        Keyword Arguments
        -----------------
        tag_delimiter : str
            Delimiter for tags string, ``';'`` by default.
        pv_name: str
            Property key name for PV name, ``'pv'`` by default.
        prop_skip: list
            List of properties to skip, ``['pv_id', 'elem_id']`` by default.
        owner : str
            Required by real Channel Finder Service.
        """
        key_pv_name = kws.get('pv_name', 'pv')
        prop_skip = kws.get('prop_skip', ['pv_id', 'elem_id'])
        tag_delimiter = kws.get('tag_delimiter', ';')
        owner = kws.get('owner', getpass.getuser())

        retval = []
        for rec in results:
            pv_name = None
            pv_props = []
            pv_tags = []
            for idx, props in enumerate(properties):
                if props in prop_skip:
                    continue
                elif props == key_pv_name:
                    pv_name = rec[idx]
                elif props == "tags":
                    if rec[idx] is not None:
                        pv_tags = [{'name': t, 'owner': owner} for t in
                                   rec[idx].split(tag_delimiter)]
                elif rec[idx] is not None:
                    pv_props.append(
                        {'name': props, 'value': rec[idx], 'owner': owner})
            if pv_name is not None:
                retval.append({'name': pv_name, 'owner': owner,
                               'properties': pv_props,
                               'tags': pv_tags})

        return retval

    def findProperty(self, propertyName):
        """Searches for the property name or pattern.

        Parameters
        ----------
        propertyName : str
            Unix shell pattern for property name.

        Returns
        -------
        ret : list
            List of properties.
        """
        return [p for p in self.getAllProperties() if
                fnmatch(p['name'], propertyName)]

    def findTag(self, tagName):
        """Searches for the tag name or pattern.

        Parameters
        ----------
        tagName : str
            Unix shell pattern for tag name.

        Returns
        -------
        ret : list
            List of tags.
        """
        return [t for t in self.getAllTags() if fnmatch(t['name'], tagName)]

    def getAllTags(self, delimiter=";", **kws):
        """Get all tags.

        Parameters
        ----------
        delimiter : str
            Delimiter to separate multiple tags for one PV, ";" by default.

        Keyword Arguments
        -----------------
        name_only : True or False
            If true, only return list of tag names.

        Returns
        -------
        ret : list of dict
            dict: {'name': tag_name, 'owner': owner}
        """
        owner = self.owner
        cur = self.dbconn.cursor()
        cur.execute("SELECT tags from pvs")
        tag_set = set()
        for tag in cur.fetchall():
            if tag[0] is not None:
                [tag_set.add(str(i)) for i in tag[0].split(delimiter)]
        if kws.get('name_only', False):
            return sorted(list(tag_set))
        else:
            return [{'name': tag, 'owner': owner} for tag in tag_set]

    def getAllProperties(self, **kws):
        """Get all property definitions.

        Keyword Arguments
        -----------------
        name_only : True or False
            If true, only return list of property names.

        Returns
        -------
        ret : list of dict
            dict: {'name': property_name, 'value': None, 'owner': owner}
        """
        owner = self.owner
        cur = self.dbconn.cursor()
        cur.execute("""SELECT * FROM pvs JOIN elements__pvs ON pvs.pv_id=elements__pvs.pv_id 
                       JOIN elements ON elements__pvs.elem_id=elements.elem_id""")
        properties = [{'name': prpts[0], 'value': None, 'owner': owner} for
                      prpts in cur.description
                      if prpts[0] not in ["elem_id", "pv_id", "tags", 'pv',
                                          'elem_pvs_id']]

        if kws.get('name_only', False):
            return sorted([p['name'] for p in properties])
        else:
            return properties

    def delete(self, **kwargs):
        """Delete channel, property and tag.

        Keyword Arguments
        -----------------
        channelName : str
            Channel name string.

        Examples
        --------
        1. Delete channel by channel name
        
        >>> # delete channel of the name of 'ch1':
        >>> delete(channelName='ch1')

        2. Delete tag by tag name
        
        >>> # delete(tagName = string)
        >>> delete(tag = 'myTag')
        >>> # tag = tag name of the tag to be removed from all channels

        3. Delete property by property name

        >>> # property = property name of property to be removed from all channels
        >>> # delete(property = string)
        >>> delete(property = 'position')

        delete(tag = string, channel = string)
        >>> delete(tag='myTag', channel = 'chName')
        # delete the tag from the specified channel _chName_

        delete(tag = string ,channel = [string])
        >>> delete(tag='myTag', channel=['ch1','ch2','ch3'])
        # delete the tag from all the channels specified in the channel list

        delete(property = string ,channel = string)
        >>> delete(property = 'propName', channel = 'chName')
        # delete the property from the specified channel

        delete(property = string, channel = [string])
        >>> delete(property = 'propName', channel = ['ch1','ch2','ch3'])
        # delete the property from all the channels in the channel list
        """
        channels = kwargs.get("channel", None)
        property = kwargs.get("property", None)
        tag = kwargs.get("tag", None)

        if isinstance(property, (list, tuple)) or isinstance(tag,
                                                             (list, tuple)):
            raise Exception(
                "Handling multiple properties or tags not support yet.")

        if channels is None:
            # handle property and tags only
            if property is not None:
                # set all value to NULL to delete
                cur = self.dbconn.cursor()
                try:
                    cur.execute("BEGIN")
                    self.dbconn("UPDATE elements SET {0}=NULL".format(property))
                    self.dbconn.commit()
                except self.dbconn.Error:
                    self.dbconn.rollback()
                    cur.execute("BEGIN")
                    self.dbconn("UPDATE pvs SET {0}=NULL".format(property))
                    self.dbconn.commit()
                except self.dbconn.Error:
                    self.dbconn.rollback()
                    raise
            if tag is not None:
                # remove tag from all channel if it has the name
                cur = self.dbconn.cursor()
                self._deleteSingleChannelTag(cur, tag)
        else:
            if property is None and tag is None:
                # delete the whole row
                if isinstance(channels, (list, tuple)):
                    vals = []
                    sql = """DELETE FROM pvs WHERE pv IN ( """
                    for ch in channels:
                        sql += """?,"""
                    sql = sql[:-1] + """ )"""
                    # multiple channels
                    with self.dbconn:
                        self.dbconn.executemany(sql, channels)
                else:
                    # single channel
                    with self.dbconn:
                        self.dbconn.execute("DELETE from pvs where pv = ?",
                                            (channels,))
            else:
                # delete both property and tags of pv(s)
                if tag is None:
                    # delete a property of pv(s)
                    cur = self.dbconn.cursor()
                    if isinstance(channels, (list, tuple)):
                        for chan in channels:
                            self._deleteSingleChannelProperty(cur, property,
                                                              chan)
                    else:
                        self._deleteSingleChannelProperty(cur, property,
                                                          channels)
                if property is None:
                    # delete a tag of pv(s)
                    cur = self.dbconn.cursor()
                    if isinstance(channels, (list, tuple)):
                        for chan in channels:
                            self._deleteSingleChannelTag(cur, tag, channel=chan)
                    else:
                        # remove tag from all channel if it has the name
                        self._deleteSingleChannelTag(cur, tag, channel=channels)

    def _deleteSingleChannelTag(self, cur, tag, channel=None):
        """

        :param cur:      SQLite cursor object of connection
        :param tag:      tag name
        :param channel:  channel name
        :return:
        """
        if channel is None:
            cur.execute("SELECT pv_id, tags FROM pvs WHERE tags like ? ",
                        ("%" + tag + "%",))
            tmp = cur.fetchall()
            if len(tmp) == 0:
                # no tag found
                return
            delimiter = ";"
            new_tags = []
            for r in tmp:
                tags = [tmptag.strip() for tmptag in r.split(delimiter)]
                if tag in tags:
                    tags.remove(tag)
                    # only handle those have exact same tag name
                    new_tags.append([";".join(tags, r[0])])
            with self.dbconn:
                cur.executemany("""UPDATE pvs SET tags = ? WHERE pv_id = ? )""",
                                new_tags)
        else:
            cur.execute(
                "SELECT pv_id, tags FROM pvs WHERE tags like ? and pv = ?",
                ("%" + tag + "%", channel))
            tmp = cur.fetchall()
            if len(tmp) == 0:
                # no tag found
                return
            delimiter = ";"
            new_tags = []
            for r in tmp:
                tags = [tmptag.strip() for tmptag in r.split(delimiter)]
                if tag in tags:
                    tags.remove(tag)
                    # only handle those have exact same tag name
                    new_tags.append([";".join(tags, r[0])])
            with self.dbconn:
                cur.executemany("""UPDATE pvs SET tags = ? WHERE pv_id = ? )""",
                                new_tags)

    def _deleteSingleChannelProperty(self, cur, property, channel):
        """Delete property from a channel.

        :param cur:      SQLite cursor object of connection
        :param property: property name
        :param channel:  channel name
        :return:
        """
        cur.execute("""SELECT elem_id FROM pvs WHERE pv = ?""", (channel,))
        tmp = cur.fetchall()
        if len(tmp) == 0:
            raise Exception("Channel ({0}) name not found.".format(channel))
        elem_id = tmp[0][0]
        try:
            cur.execute("BEGIN")
            self.dbconn("UPDATE elements SET {0}=NULL WHERE elem_id = ?".format(
                property), (elem_id,))
            self.dbconn.commit()
        except self.dbconn.Error:
            self.dbconn.rollback()
            cur.execute("BEGIN")
            self.dbconn(
                "UPDATE pvs SET {0}=NULL WHERE elem_id = ?".format(property),
                (elem_id,))
            self.dbconn.commit()
        except self.dbconn.Error:
            self.dbconn.rollback()
            raise

    def update(self, **kwargs):
        """
        update(property = string, channel = string)
        >>> update(property='propValue', channel='ch1')
        # Add property to the channel with the name 'ch1'
        # without affecting the other channels using this property

        update(property = string, channel = [string])
        >>>update(property='propValue', channel=['ch1','ch2','ch3'])
        # Add Property to the channels with the names in the list channelNames
        # without affecting the other channels using this property

        update(tag = string, channel = string)
        >>> update(tag = 'myTag', channel='chName')
        # Add tag to channel with name chName
        # without affecting the other channels using this tag

        update(tag = string, channel = [string])
        >>> update(tag = 'tagName', channel=['ch1','ch2','ch3'])
        # Add tag to channels with names in the list channel names
        # without affecting the other channels using this tag

        ## RENAME OPERATIONS ##
        update(channel = string, originalChannel = string)
        >>> update(channel = 'newChannelName', originalChannel = 'oldChannelName')
        # rename the channel 'oldChannelName' to 'newChannelName'

        update(property = string, originalProperty = string)
        >>> update(property = 'newPropertyValue', originalProperty = 'oldPropertyValue')
        # rename the property 'oldPropertyName' to 'newPropertyName'
        # the channels with the old property are also updated

        update(tab = string, originalTag = string)
        >>> update(tag = 'newTagName', originalTag = 'oldTagName')
        # rename the tag 'oldTagName' to 'newTagName'
        # the channel with the old tag are also updated
        """
        channels = kwargs.get("channel", None)
        originalChannel = kwargs.get("originalChannel", None)
        originalProperty = kwargs.get("originalProperty", None)
        originalTag = kwargs.get("originalTag", None)
        tag = kwargs.get("tag", None)
        prpt_names = [k for k in kwargs.keys() if
                      k not in ['channel', "originalChannel",
                                'originalProperty', 'originalTag',
                                'tag']]

        if originalChannel is not None:
            # update old channel name to new channel name
            if channels is None or isinstance(channels, (list, tuple)):
                raise Exception(
                    "Invalid new channel name. Cannot update channel name.")
            with self.dbconn:
                self.dbconn.execute("""UPDATE pvs SET pv = ? WHERE pv = ?""",
                                    (channels, originalChannel))
        elif originalProperty is not None:
            # update old property value to new one for all channels
            if len(prpt_names) != 1:
                raise Exception(
                    "Update multiple property values not supported yet.")
            new_prpt_value = kwargs.get(prpt_names[0], None)
            if new_prpt_value is None:
                raise Exception(
                    "Invalid property value. Cannot update property value.")

            cur = self.dbconn.cursor()
            cur.execute("PRAGMA table_info(elements)")
            tbl_elements_cols = [v[1] for v in cur.fetchall()]
            cur.execute("PRAGMA table_info(pvs)")
            tbl_pvs_cols = [v[1] for v in cur.fetchall()]

            # get all property value
            delimiter = ";"
            if prpt_names[0] in tbl_elements_cols:
                cur.execute(
                    """SELECT {0}, elem_id FROM elements where {1} like ?""".format(
                        prpt_names[0]),
                    (originalProperty,))
            elif prpt_names[0] in tbl_pvs_cols:
                cur.execute(
                    """SELECT {0}, pv_id FROM pvs where {1} like ?""".format(
                        prpt_names[0]),
                    (originalProperty,))
            else:
                raise Exception("Unknown property {}".format(prpt_names[0]))

            # has format like [(id, value)]
            new_values = []
            for p in cur.fetchall():
                if delimiter in p[0]:
                    if originalProperty in p[0].split(delimiter):
                        # keep order
                        xxx = delimiter.join(
                            [new_prpt_value if x == originalProperty else x for
                             x in p[0].split(delimiter)])
                        new_values.append((xxx, p[1]))
                elif originalProperty == p[0]:
                    new_values.append((new_prpt_value, p[1]))
            if prpt_names[0] in tbl_elements_cols:
                with self.dbconn:
                    self.dbconn.executemany(
                        """UPDATE elements SET {0} = ? WHERE pv_id = ?""".format(
                            prpt_names[0]),
                        new_values)
            elif prpt_names[0] in tbl_pvs_cols:
                with self.dbconn:
                    self.dbconn.executemany(
                        """UPDATE pvs SET {0} = ? WHERE pv_id = ?""".format(
                            prpt_names[0]),
                        new_values)
        elif originalTag is not None:
            # update old tag to new tag
            if len(prpt_names) != 1:
                raise Exception(
                    "Update multiple property values not supported yet.")
            new_prpt_value = kwargs.get(prpt_names[0], None)
            if new_prpt_value is None:
                raise Exception(
                    "Invalid property value. Cannot update property value.")

            cur = self.dbconn.cursor()
            # get all property value
            delimiter = ";"
            cur.execute("""SELECT tags, pv_id FROM pvs where tags like ?""",
                        (originalTag,))

            # has format like [(id, value)]
            new_values = []
            for p in cur.fetchall():
                if delimiter in p[0]:
                    if originalProperty in p[0].split(delimiter):
                        # keep order
                        xxx = delimiter.join(
                            [new_prpt_value if x == originalProperty else x for
                             x in p[0].split(delimiter)])
                        new_values.append((xxx, p[1]))
                elif originalProperty == p[0]:
                    new_values.append((new_prpt_value, p[1]))
            with self.dbconn:
                self.dbconn.executemany(
                    """UPDATE pvs SET tags = ? WHERE pv_id = ?""", new_values)
        else:
            # update property and tag for given channel(s)
            # if property or tag does not exist, append as new
            if "tag" in kwargs:
                # update old tag to new tag
                new_tag_value = kwargs.get('tag', None)
                if new_tag_value is None:
                    # None tag, do nothing
                    return

                cur = self.dbconn.cursor()
                # get all property value
                delimiter = ";"
                if isinstance(channels, (list, tuple)):
                    sql = """SELECT tags, pv_id FROM pvs where pv in ("""
                    for _ in channels:
                        sql += "?,"
                    sql = sql[:-1] + """)"""
                    cur.execute(sql, channels)
                else:
                    cur.execute(
                        """SELECT tags, pv_id FROM pvs where pv like ?""",
                        (channels,))

                # has format like [(id, value)]
                new_values = []
                for p in cur.fetchall():
                    if delimiter in p[0]:
                        if originalTag in p[0].split(delimiter):
                            # keep order
                            xxx = delimiter.join(
                                [new_tag_value if x == originalTag else x for x
                                 in p[0].split(delimiter)])
                            new_values.append((xxx, p[1]))
                    elif originalTag == p[0]:
                        new_values.append((new_tag_value, p[1]))
                    else:
                        new_values.append(
                            (delimiter.join((p[0], new_tag_value)), p[1]))
                with self.dbconn:
                    self.dbconn.executemany(
                        """UPDATE pvs SET tags = ? WHERE pv_id = ?""",
                        new_values)
            else:
                # update old property value to new one for all channels
                if len(prpt_names) != 1:
                    raise Exception(
                        "Update multiple property values not supported yet.")
                new_prpt_value = kwargs.get(prpt_names[0], None)
                if new_prpt_value is None:
                    # None property value, do nothing
                    return

                cur = self.dbconn.cursor()
                cur.execute("PRAGMA table_info(elements)")
                tbl_elements_cols = [v[1] for v in cur.fetchall()]
                cur.execute("PRAGMA table_info(pvs)")
                tbl_pvs_cols = [v[1] for v in cur.fetchall()]

                # get all property value
                delimiter = ";"
                if prpt_names[0] in tbl_elements_cols:
                    if isinstance(channels, (list, tuple)):
                        sql = """SELECT DISTINCT {0}, elements.elem_id FROM pvs JOIN elements__pvs ON pvs.pv_id = elements__pvs.pv_id
                                 JOIN elements ON elements__pvs.elem_id = elements.elem_id
                                 WHERE pv IN (""".format(prpt_names[0])
                        for _ in channels:
                            sql += "?,"
                        sql = sql[:-1] + """)"""
                        cur.execute(sql, channels)
                    else:
                        sql = """SELECT DISTINCT {0}, elements.elem_id FROM pvs JOIN elements__pvs ON pvs.pv_id = elements__pvs.pv_id
                                 JOIN elements ON elements__pvs.elem_id = elements.elem_id
                                 WHERE pv LIKE ?""".format(prpt_names[0])
                        cur.execute(sql, (channels,))
                elif prpt_names[0] in tbl_pvs_cols:
                    if isinstance(channels, (list, tuple)):
                        sql = """SELECT {0}, pv_id FROM pvs where pv in (""".format(
                            prpt_names[0])
                        for _ in channels:
                            sql += "?,"
                        sql = sql[:-1] + """)"""
                        cur.execute(sql, channels)
                    else:
                        cur.execute(
                            """SELECT {0}, pv_id FROM pvs where pv like ?""".format(
                                prpt_names[0]),
                            (channels,))
                else:
                    raise Exception("Unknown property {}".format(prpt_names[0]))

                # has format like [(id, value)]
                new_values = []
                for p in cur.fetchall():
                    if delimiter in p[0]:
                        if originalProperty in p[0].split(delimiter):
                            # keep original order if multiple properties
                            xxx = delimiter.join(
                                [new_prpt_value if x == originalProperty else x
                                 for x in p[0].split(delimiter)])
                            new_values.append((xxx, p[1]))
                    elif originalProperty == p[0]:
                        new_values.append((new_prpt_value, p[1]))
                    else:
                        new_values.append(
                            (delimiter.join((p[0], new_prpt_value)), p[1]))
                if prpt_names[0] in tbl_elements_cols:
                    with self.dbconn:
                        self.dbconn.executemany(
                            """UPDATE elements SET {0} = ? WHERE elem_id = ?""".format(
                                prpt_names[0]),
                            new_values)
                elif prpt_names[0] in tbl_pvs_cols:
                    with self.dbconn:
                        self.dbconn.executemany(
                            """UPDATE pvs SET {0} = ? WHERE pv_id = ?""".format(
                                prpt_names[0]),
                            new_values)

    def set(self, **kwargs):
        """Add new properties/tags/channels.
        """
        ## Add new tags
        ## Add new properties
        ## Add new channels
        pass


def write_db(data, db_name, overwrite=False, **kwargs):
    """Write PV/channels data into SQLite database, overwrite if *db_name* is
    already exists while *overwrite* is True.

    Parameters
    ----------
    data : list(dict)
        List of dict, each dict element is of the format:
        ``{'name': PV name (str), 'owner': str, 'properties': PV properties (list[dict]), 'tags': PV tags (list[dict])}``
    db_name : str
        Filename of database.
    overwrite : bool
        Overwrite existing database file or not, False by default.
    
    Keyword Arguments
    -----------------
    tag_delimiter : str
        Delimiter for tags string, ``';'`` by default.
    use_unicode : bool
        If treat string as unicode or not, False by default.
    quite : bool
        Add log entries if False, False by default.

    See Also
    --------
    get_data_from_tb : Get PV data from spreadsheet.
    get_data_from_db : Get PV data from database.
    get_data_from_cf : Get PV data from Channel Finder Service.
    """
    if not os.path.isfile(db_name):
        # create a new database
        init_db(db_name=db_name)
    elif overwrite:
        init_db(db_name, overwrite=overwrite)
    else:
        _LOGGER.warning(
            "{} already exists, overwrite it by passing overwrite=True.".format(
                db_name))
        return None

    # delimeter to separate tags in database
    tag_delimeter = kwargs.get("tag_delimeter", ";")
    use_unicode = kwargs.get('unicode', False)
    quiet = kwargs.get("quiet", False)

    # elemName, elemType, elemIndex MUST not be None
    conn = sqlite3.connect(db_name)
    conn.text_factory = str if not use_unicode else use_unicode
    cur = conn.cursor()

    # insert entries into table 'elements' and table 'pvs',
    # as well as table 'log' if quite is False.
    elem_sets = []
    elem_sets_key = []
    pv_sets = []
    pv_sets_pvs = []
    # process elements table and pvs table
    for rec in data:
        pv_name, pv_tags = rec['name'], rec['tags']
        pv_props = {p['name']: p['value'] for p in rec['properties']}

        ukey = (
            pv_props.get("elemIndex", None),
            pv_props.get("elemType", ""),
            pv_props.get("elemName", ""),
        )

        # skip if already in the to-be-inserted list
        # deprecated: elemName has to be unique
        # elemIndex has to be unique since one element might be split into many pieces
        elem_index, elem_type, elem_name = ukey
        if elem_index and elem_index not in elem_sets_key:
            cur.execute(
                """SELECT EXISTS(SELECT * FROM elements WHERE elemIndex=? AND elemType=? AND elemName=? LIMIT 1)""",
                (elem_index, elem_type, elem_name))
            res, = cur.fetchone()
            # no need to insert if exists
            if res == 0:
                # element index does not exist yet.
                elem_sets.append(ukey)
                # avoid element index + name, which has been added already
                # elem_sets_key.append((ukey[0], ukey[1], ukey[2]))
                elem_sets_key.append(ukey)

        ukey = (
            pv_name,
            pv_props.get("elemField", ""),
            pv_props.get("elemHandle", "")
        )
        if pv_name and pv_name not in pv_sets_pvs:
            cur.execute(
                """SELECT EXISTS(SELECT * FROM pvs WHERE pv=? LIMIT 1)""",
                (pv_name,))
            res, = cur.fetchone()
            if res == 0:
                # pv name does not exist yet.
                pv_sets.append(ukey)
                # not to add the pv name again
                pv_sets_pvs.append(pv_name)

    for ielem in elem_sets:
        _LOGGER.debug("Adding new element: {0}".format(ielem))

    for ipv in pv_sets:
        _LOGGER.debug("Adding new PV: {0}".format(ipv))

    # insert new entries, distinguished by (elemIndex, elemType, elemName)
    # with conn:
    # for elem in elem_sets:
    #    print(elem)
    #    conn.execute("""INSERT INTO elements (elemIndex, elemType, elemName) VALUES (?,?,?)""", elem)

    conn.executemany(
        """INSERT INTO elements (elemIndex, elemType, elemName) VALUES (?,?,?)""",
        elem_sets)
    conn.executemany(
        """INSERT INTO pvs (pv, elemField, elemHandle) VALUES (?,?,?)""",
        pv_sets)

    _LOGGER.debug("Added {0} elements".format(len(elem_sets)))
    _LOGGER.debug("Added {0} pvs".format(len(pv_sets)))

    # update elements table
    cur.execute("BEGIN")
    cur.execute("PRAGMA table_info(elements)")
    tbl_elements_cols = [v[1] for v in cur.fetchall()]

    # add more columns if defined by schema
    for col in tbl_elements_cols:
        # element index with element name is unique 
        if col in ["elemIndex", "elemType", "elemName"]:
            continue
        vals = []
        for rec in data:
            pv_name, pv_tags = rec['name'], rec['tags']
            pv_props = {p['name']: p['value'] for p in rec['properties']}
            if col not in pv_props:
                # only update rec whose cols are defined in schema 
                continue
            try:
                vals.append((pv_props[col], pv_props["elemIndex"],
                             pv_props["elemType"], pv_props["elemName"]))
            except:
                cur.execute("""INSERT INTO log (timestamp, message) 
                        VALUES (datetime('now', 'localtime'), 'Incomplete record for pv={}')""".format(
                    pv_name))
        if len(vals) == 0:
            _LOGGER.debug(
                "Table(elements): no data for column '{0}'.".format(col))
            continue
        try:
            cur.executemany(
                "UPDATE elements SET {0}=? WHERE elemIndex=? AND elemType=? AND elemName=?".format(
                    col), vals)
        except:
            raise RuntimeError("Error at updating {0} {1}".format(col, vals))

        # conn.commit()
        _LOGGER.debug(
            "Table(elements): update column '{0}' with {1} records.".format(
                col, len(vals)))

    # update pvs table
    cur.execute("PRAGMA table_info(pvs)")
    tbl_pvs_cols = [v[1] for v in cur.fetchall()]

    # add more columns if defined by schema
    for col in tbl_pvs_cols:
        if col in ['pv', 'elemField', 'elemHandle', 'tags']:
            continue
        vals = []
        for rec in data:
            pv_name, pv_tags = rec['name'], rec['tags']
            pv_props = {p['name']: p['value'] for p in rec['properties']}
            if col not in pv_props:
                # only update rec whose cols are defined in schema 
                continue
            if ("elemField" not in pv_props) or ("elemIndex" not in pv_props):
                # print("Incomplete record for pv={0}: {1} {2}".format(
                #    pv, prpts, tags))
                cur.execute("""INSERT INTO log (timestamp, message) 
                        VALUES (datetime('now', 'localtime'), 'Incomplete record for pv={}')""".format(
                    pv_name))
                continue
            # elemGroups is a list
            vals.append((pv_props[col], pv_name, pv_props["elemField"]))

        if len(vals) == 0:
            _LOGGER.debug("Table(pvs): no data for column '{0}'.".format(col))
            continue
        cur.executemany(
            "UPDATE pvs SET {0}=? WHERE pv=? and elemField=?".format(col), vals)

        # conn.commit()
        _LOGGER.debug(
            "Table(pvs): update column '{0}' with {1} records.".format(col, len(
                vals)))

    # update tags
    vals = []
    for rec in data:
        pv_name, pv_tags = rec['name'], rec['tags']
        pv_props = {p['name']: p['value'] for p in rec['properties']}
        if pv_tags is None:
            continue
        if not pv_props.has_key("elemField") or not pv_props.has_key(
                "elemIndex"):
            # print("Incomplete record for pv={0}: {1} {2}. IGNORED".format(
            #    pv, prpts, tags))
            cur.execute("""INSERT INTO log (timestamp, message)
                    VALUES (datetime('now', 'localtime'), "Incomplete record for pv={}")""".format(
                pv_name))
            continue
        pv_tags_str = tag_delimeter.join(sorted([t['name'] for t in pv_tags]))
        vals.append((pv_tags_str, pv_name, pv_props["elemField"]))
    if len(vals) > 0:
        cur.executemany("""UPDATE pvs SET tags=? WHERE pv=? AND elemField=?""",
                        vals)
        # conn.commit()
        _LOGGER.debug(
            "Table(pvs): update tags for {0} records.".format(len(vals)))

    # write log if not *quiet*
    if not quiet:
        msg = "Local database for Channel Finder Service processed {0:<3d} records, added {1:<3d} elements and {2:<3d} PVs".format(
            len(data), len(elem_sets), len(pv_sets))
        cur.execute(
            """INSERT INTO log(timestamp, message) VALUES (datetime('now', 'localtime'), ? )""",
            (msg,))

    # update table elements__pvs
    cur.execute("DELETE FROM elements__pvs")
    pre_pv_name = ""
    pre_elem_name = ""
    pre_elem_type = ""
    pre_elem_index = 0
    pvid = 0
    elemid = 0
    values = []
    for rec in data:
        pv_name = rec['name']
        pv_props = {p['name']: p['value'] for p in rec['properties']}

        if 'elemName' not in pv_props or 'elemType' not in pv_props or 'elemIndex' not in pv_props:
            continue

        if pv_name != pre_pv_name:
            cur.execute("SELECT pv_id FROM pvs WHERE pv = ?", (pv_name,))
            pvid = cur.fetchone()
            if pvid is not None:
                pvid = pvid[0]
            else:
                raise ValueError("pv_id is None")
            pre_pv_name = pv_name
        if pre_elem_name != pv_props['elemName'] \
                or pre_elem_index != pv_props['elemIndex'] \
                or pre_elem_type != pv_props['elemType']:
            pre_elem_name = pv_props['elemName']
            pre_elem_index = pv_props['elemIndex']
            pre_elem_type = pv_props['elemType']
            cur.execute(
                "SELECT elem_id FROM elements WHERE elemName=? AND elemType=? AND elemIndex=?",
                (pre_elem_name, pre_elem_type, pre_elem_index))
            elemid = cur.fetchone()
            if elemid is None:
                raise ValueError(
                    "Cannot find elem_id for element (name: {0}, index: {1}) in elements table.".
                        format(pre_elem_name, pre_elem_index))
            else:
                elemid = elemid[0]
        values.append([pvid, elemid])

    cur.executemany("INSERT INTO elements__pvs (pv_id, elem_id) VALUES (?, ?)",
                    values)

    try:
        conn.commit()
    except conn.Error:
        conn.rollback()
    finally:
        conn.close()


def init_db(db_name, overwrite=False, extra_cols=None):
    """Initialize SQLite database schema for channels data.

    Four tables will be initialized:
        * elements
        * pvs
        * log
        * elements__pvs: mapping table to link elements and pvs (N:M mapping)

    The *element* table is to store all element information with *elem_id* as
    primary key.
    Columns defined by default are:

        +--------------+---------+
        | elem_id      | integer |
        +--------------+---------+
        | elemName     | string  |
        +--------------+---------+
        | elemType     | string  |
        +--------------+---------+
        | elemLength   | float   |
        +--------------+---------+
        | elemPosition | float   |
        +--------------+---------+
        | elemIndex    | integer |
        +--------------+---------+
        | elemGroups   | string  |
        +--------------+---------+
        | fieldPolar   | integer |
        +--------------+---------+
        | virtual      | integer |
        +--------------+---------+

    User could customize more columns (defined by *extra_cols*), for example,
    ``extra_cols=['cell', 'girder', 'symmetry']`` will add the following
    columns:

        +--------------+---------+
        | cell         | string  |
        +--------------+---------+
        | girder       | string  |
        +--------------+---------+
        | symmetry     | string  |
        +--------------+---------+

    The *pvs* table is to store PV related information. It uses pv name as
    primary key, and has foreign key pointing to element table.
    Columns defined by default are:
 
        +--------------+---------+
        | pv_id        | integer |
        +--------------+---------+
        | pv           | string  | 
        +--------------+---------+
        | elemHandle   | string  |
        +--------------+---------+
        | elemField    | string  |
        +--------------+---------+
        | hostname     | string  |
        +--------------+---------+
        | devName      | string  |
        +--------------+---------+
        | iocname      | float   |
        +--------------+---------+
        | tags         | string  |
        +--------------+---------+
        | speed        | float   |
        +--------------+---------+
        | hlaHigh      | float   |
        +--------------+---------+
        | hlaLow       | float   |
        +--------------+---------+
        | hlaStepsize  | float   |
        +--------------+---------+
        | hlaValRef    | float   |
        +--------------+---------+
        | archive      | integer |
        +--------------+---------+
        | size         | integer |
        +--------------+---------+
        | epsilon      | float   |
        +--------------+---------+

    The *log* table is to save history information.
    Columns defined by default are:

        +--------------+---------+
        | log_id       | integer |
        +--------------+---------+
        | timestamp    |timestamp|
        +--------------+---------+
        | message      | string  |
        +--------------+---------+

    Constraints:

    - elemName is unique
    - (pv,elemName,elemField) is unique
    - elemType can not be NULL

    Parameters
    ----------
    db_name : str
        Filename of database.
    overwrite : bool
        Overwrite existing database file or not, False by default.
    extra_cols : list(str)
        List of extra column names for *elements* table, which are user-defined
        element properties.

    Returns
    -------
    ret : str
        If database initialization is successful, return the database name,
        or None.
    """
    if os.path.isfile(db_name) and not overwrite:
        _LOGGER.warning(
            "{} already exists, overwrite it by pass overwrite=True.".format(
                db_name))
        return db_name

    sqlcmd = """DROP TABLE IF EXISTS log;
    DROP TABLE IF EXISTS elements;
    DROP TABLE IF EXISTS pvs;
    DROP TABLE IF EXISTS elements__pvs;

    CREATE TABLE log (log_id    INTEGER PRIMARY KEY,
                      timestamp TIMESTAMP NOT NULL,
                      message   TEXT);

    CREATE TABLE elements
                 (elem_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                  elemName      TEXT NOT NULL,
                  elemType      TEXT NOT NULL,
                  elemLength    REAL,
                  elemPosition  REAL,
                  elemIndex     INTEGER NOT NULL,
                  elemGroups    TEXT,
                  {}
                  fieldPolar    INTEGER,
                  virtual       INTEGER DEFAULT 0,
                  UNIQUE (elemName, elemType, elemIndex) ON CONFLICT IGNORE 
                  );
                  
    CREATE TABLE elements__pvs 
                 (elem_pvs_id          INTEGER PRIMARY KEY AUTOINCREMENT,
                  elem_id              INTEGER,
                  pv_id                INTEGER,
                  FOREIGN KEY(elem_id) REFERENCES elements(elem_id),
                  FOREIGN KEY(pv_id)   REFERENCES pvs(pv_id),
                  UNIQUE (elem_id, pv_id) ON CONFLICT REPLACE
                 );

    CREATE TABLE pvs
                 (pv_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                  pv            TEXT NOT NULL UNIQUE,
                  elemHandle    TEXT,
                  elemField     TEXT,
                  hostName      TEXT,
                  devName       TEXT,
                  iocName       TEXT,
                  tags          TEXT,
                  speed         REAL,
                  hlaHigh       REAL,
                  hlaLow        REAL,
                  hlaStepsize   REAL,
                  hlaValRef     REAL,
                  archive       INT   DEFAULT 0,
                  size          INT   DEFAULT 0,
                  epsilon       REAL  DEFAULT 0.0
                  );
    """

    extra = '\n'

    keys = [key.upper() for key in ['elemName',
                                    'elemType',
                                    'elemLength',
                                    'elemPosition',
                                    'elemIndex',
                                    'elemGroups',
                                    'fieldPolar',
                                    'virtual',
                                    'pv',
                                    'elem_id',
                                    'elemHandle',
                                    'elemField',
                                    'hostName',
                                    'devName',
                                    'iocName',
                                    'tags',
                                    'speed',
                                    'hlaHigh',
                                    'hlaLow',
                                    'hlaStepsize',
                                    'hlaValRef',
                                    'archive',
                                    'size',
                                    'epsilon']]

    if extra_cols is not None:
        for key in extra_cols:
            if key.upper() not in keys and key is not None and key.strip() != "":
                extra += """{0:<18s}{1:<13s} TEXT,\n""".format(' ', key)

    try:
        with sqlite3.connect(db_name) as conn:
            conn.executescript(sqlcmd.format(extra))
            conn.execute("""INSERT INTO log (timestamp, message)
                         VALUES (datetime('now', 'localtime'), "Local database for Channel Finder Service is created.")""")
        return db_name
    except:
        _LOGGER.error("Database initialization failed.")
        return None


if __name__ == "__main__":
    # see contrib
    pass
