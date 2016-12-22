"""
Local cache for channel finder service.

:author: Guobao Shen <shen@frib.msu.edu>
"""

import os
import sqlite3
from fnmatch import fnmatch

import logging
_logger = logging.getLogger(__name__)


class ChannelFinderLocal(object):
    """
    Local channel finder service using SQLite db
    """
    def __init__(self, dbname):
        """

        :return:
        """
        self.dbname = dbname

    def conn(self):
        """

        :return: SQLite database connect object
        """
        self.dbconn = sqlite3.connect(self.dbname)

    def close(self):
        """ Close current SQLite db connection

        :return:
        """
        self.dbconn.close()


    def find(self, **kwargs):
        '''
        Method allows you to query for a channel/s based on name, properties, tags
        find(name = channelNamePattern)
        >>> find(name='*')
        >>> find(name='SR:C01*')

        find(tagName = tagNamePattern)
        >>> find(tagName = 'myTag')

        find(property = [(propertyName,propertyValuePattern)])
        >>> find(property=[('position','*')])
        >>> find(property=[('position','*'),('cell','')])

        returns a _list_ of matching Channels
        special pattern matching char
        * for multiple char
        ? for single char

        Searching with multiple parameters
        >>> find(name='SR:C01*', tagName = 'myTag', property=[('position','pattern1')])
        return all channels with name matching 'SR:C01*' AND
                            with tagName = 'mytag' AND
                            with property 'position' with value matching 'pattern1'


        For multiValued searches
        >>> find(name='pattern1,pattern2')
        will return all the channels which match either pattern1 OR pattern2

        >>> find(property=[('propA','pattern1,pattern2')])
        will return all the channels which have the property propA  and
        whose values match pattern1 OR pattern2

        >>> find(property=[('propA', 'pattern1'),('propB', 'pattern2')])
        will return all the channels which have properties
        _propA_ with value matching _pattern1_ AND _propB_ with value matching _pattern2_

        >>> find(tagName='pattern1,pattern2')
        will return all the channels which have the tags matching pattern1 AND pattern2

        To query for the existance of a tag or property use findTag and findProperty.
        '''
        if len(kwargs) == 0:
            raise Exception, 'Incorrect usage: at least one parameter must be specified'
        channames = kwargs.get("name", "*")
        properties = kwargs.get("property", None)
        tags = kwargs.get("tagName", None)
        sql = """SELECT * from pvs join elements__pvs on pvs.pv_id = elements__pvs.pv_id 
                join elements on elements__pvs.elem_id = elements.elem_id where """
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
                    querycons.append(pts.strip().replace("*", "%").replace("?", "_"))
                    if first:
                        first = False
                    else:
                        sql += """ or """
                    sql += """ {0} like ? """.format(prpts[0])
            sql += """ ) """
        if tags is not None:
            tags = ",".join((tag.strip() for tag in tags.replace("*", "%").replace("?", "_")))
            querycons.append(tags)
            sql += """ and tags like ? """

        # print sql, querycons
        cur = self.dbconn.cursor()
        cur.execute(sql, querycons)

        properties = [prpts[0] for prpts in cur.description]

        return (properties, cur.fetchall())

    def findProperty(self, propertyName):
        """Searches for the _exact_ propertyName and return a single Property object if found

        :param propertyName:
        :return:
        """
        if propertyName == "*":
            return self.getAllProperties()

        cur = self.dbconn.cursor()
        cur.execute("""SELECT * from pvs join elements__pvs on pvs.pv_id = elements__pvs.pv_id 
                        join elements on elementd__pvs.elem_id = elements.elem_id where  limit 1""")
        properties = [prpts[0] for prpts in cur.description if prpts[0] not in ["elem_id", "pv_id", "tags", 'pv', 'elem_pvs_id']]

        res = None
        for prpts in properties:
            if fnmatch(prpts, propertyName):
                # find the first property name matched
                res = prpts
                break

        return res

    def getAllTags(self, delimiter=";"):
        """
        return a list of all the Tags present - even the ones not associated w/t any channel

        :param delimiter: delimiter to separate multiple tags for one PV. ";" by default.
        """
        cur = self.dbconn.cursor()
        cur.execute("SELECT tags from pvs")
        tmp = cur.fetchall()

        results = []
        for res in tmp:
            if res is not None:
                results.extend(res.split(delimiter))

        return results

    def getAllProperties(self):
        """

        :return:
        """
        cur = self.dbconn.cursor()
        cur.execute("""SELECT * from pvs join elements__pvs on pvs.pv_id = elements__pvs.pv_id 
                        join elements on elementd__pvs.elem_id = elements.elem_id where  limit 1""")
        properties = [prpts[0] for prpts in cur.description if prpts[0] not in ["elem_id", "pv_id", "tags", 'pv', 'elem_pvs_id']]
        return properties

    def delete(self, **kwargs):
        """
        Method to delete a channel, property, tag
        delete(channel = string)
        >>> delete(channel = 'ch1')

        delete(tag = string)
        >>> delete(tag = 'myTag')
        # tag = tag name of the tag to be removed from all channels

        delete(property = string)
        >>> delete(property = 'position')
        # property = property name of property to be removed from all channels

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
        tag =  kwargs.get("tag", None)

        if isinstance(property, (list, tuple)) or isinstance(tag, (list, tuple)):
            raise Exception("Handling multiple properties or tags not support yet.")

        if channels is None:
            # handle property and tags only
            if property is not None:
                # set all value to NULL to delete
                cur=self.dbconn.cursor()
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
                        self.dbconn.execute("DELETE from pvs where pv = ?", (channels,))
            else:
                # delete both property and tags of pv(s)
                if tag is None:
                    # delete a property of pv(s)
                    cur=self.dbconn.cursor()
                    if isinstance(channels, (list, tuple)):
                        for chan in channels:
                            self._deleteSingleChannelProperty(cur, property, chan)
                    else:
                        self._deleteSingleChannelProperty(cur, property, channels)
                if property is None:
                    # delete a tag of pv(s)
                    cur=self.dbconn.cursor()
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
            cur.execute("SELECT pv_id, tags FROM pvs WHERE tags like ? ", ("%"+tag+"%",))
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
                cur.executemany("""UPDATE pvs SET tags = ? WHERE pv_id = ? )""", new_tags)
        else:
            cur.execute("SELECT pv_id, tags FROM pvs WHERE tags like ? and pv = ?", ("%"+tag+"%", channel))
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
                cur.executemany("""UPDATE pvs SET tags = ? WHERE pv_id = ? )""", new_tags)

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
            self.dbconn("UPDATE elements SET {0}=NULL WHERE elem_id = ?".format(property), (elem_id,))
            self.dbconn.commit()
        except self.dbconn.Error:
            self.dbconn.rollback()
            cur.execute("BEGIN")
            self.dbconn("UPDATE pvs SET {0}=NULL WHERE elem_id = ?".format(property), (elem_id,))
            self.dbconn.commit()
        except self.dbconn.Error:
            self.dbconn.rollback()
            raise

    #===============================================================================
    # Update methods
    #===============================================================================
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
        prpt_names = [k for k in kwargs.keys() if k not in ['channel', "originalChannel",
                                                            'originalProperty', 'originalTag',
                                                            'tag']]

        if originalChannel is not None:
            # update old channel name to new channel name
            if channels is None or isinstance(channels, (list, tuple)):
                raise Exception("Invalid new channel name. Cannot update channel name.")
            with self.dbconn:
                self.dbconn.execute("""UPDATE pvs SET pv = ? WHERE pv = ?""", (channels, originalChannel))
        elif originalProperty is not None:
            # update old property value to new one for all channels
            if len(prpt_names) != 1:
                raise Exception("Update multiple property values not supported yet.")
            new_prpt_value = kwargs.get(prpt_names[0], None)
            if new_prpt_value is None:
                raise Exception("Invalid property value. Cannot update property value.")

            cur = self.dbconn.cursor()
            cur.execute("PRAGMA table_info(elements)")
            tbl_elements_cols = [v[1] for v in cur.fetchall()]
            cur.execute("PRAGMA table_info(pvs)")
            tbl_pvs_cols = [v[1] for v in cur.fetchall()]

            # get all property value
            delimiter = ";"
            if prpt_names[0] in tbl_elements_cols:
                cur.execute("""SELECT {0}, elem_id FROM elements where {1} like ?""".format(prpt_names[0]),
                            (originalProperty,))
            elif prpt_names[0] in tbl_pvs_cols:
                cur.execute("""SELECT {0}, pv_id FROM pvs where {1} like ?""".format(prpt_names[0]),
                            (originalProperty,))
            else:
                raise Exception("Unknown property {}".format(prpt_names[0]))

            # has format like [(id, value)]
            new_values = []
            for p in cur.fetchall():
                if delimiter in p[0]:
                    if originalProperty in p[0].split(delimiter):
                        # keep order
                        xxx = delimiter.join([new_prpt_value if x == originalProperty else x for x in p[0].split(delimiter)])
                        new_values.append((xxx, p[1]))
                elif originalProperty == p[0]:
                    new_values.append((new_prpt_value, p[1]))
            if prpt_names[0] in tbl_elements_cols:
                with self.dbconn:
                    self.dbconn.executemany("""UPDATE elements SET {0} = ? WHERE pv_id = ?""".format(prpt_names[0]),
                                            new_values)
            elif prpt_names[0] in tbl_pvs_cols:
                with self.dbconn:
                    self.dbconn.executemany("""UPDATE pvs SET {0} = ? WHERE pv_id = ?""".format(prpt_names[0]),
                                            new_values)
        elif originalTag is not None:
            # update old tag to new tag
            if len(prpt_names) != 1:
                raise Exception("Update multiple property values not supported yet.")
            new_prpt_value = kwargs.get(prpt_names[0], None)
            if new_prpt_value is None:
                raise Exception("Invalid property value. Cannot update property value.")

            cur = self.dbconn.cursor()
            # get all property value
            delimiter = ";"
            cur.execute("""SELECT tags, pv_id FROM pvs where tags like ?""", (originalTag,))

            # has format like [(id, value)]
            new_values = []
            for p in cur.fetchall():
                if delimiter in p[0]:
                    if originalProperty in p[0].split(delimiter):
                        # keep order
                        xxx = delimiter.join([new_prpt_value if x == originalProperty else x for x in p[0].split(delimiter)])
                        new_values.append((xxx, p[1]))
                elif originalProperty == p[0]:
                    new_values.append((new_prpt_value, p[1]))
            with self.dbconn:
                self.dbconn.executemany("""UPDATE pvs SET tags = ? WHERE pv_id = ?""", new_values)
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
                    cur.execute("""SELECT tags, pv_id FROM pvs where pv like ?""", (channels,))

                # has format like [(id, value)]
                new_values = []
                for p in cur.fetchall():
                    if delimiter in p[0]:
                        if originalTag in p[0].split(delimiter):
                            # keep order
                            xxx = delimiter.join([new_tag_value if x == originalTag else x for x in p[0].split(delimiter)])
                            new_values.append((xxx, p[1]))
                    elif originalTag == p[0]:
                        new_values.append((new_tag_value, p[1]))
                    else:
                        new_values.append((delimiter.join((p[0], new_tag_value)), p[1]))
                with self.dbconn:
                    self.dbconn.executemany("""UPDATE pvs SET tags = ? WHERE pv_id = ?""", new_values)
            else:
                # update old property value to new one for all channels
                if len(prpt_names) != 1:
                    raise Exception("Update multiple property values not supported yet.")
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
                        sql = """SELECT {0}, pv_id FROM pvs where pv in (""".format(prpt_names[0])
                        for _ in channels:
                            sql += "?,"
                        sql = sql[:-1] + """)"""
                        cur.execute(sql, channels)
                    else:
                        cur.execute("""SELECT {0}, pv_id FROM pvs where pv like ?""".format(prpt_names[0]),
                                    (channels,))
                else:
                    raise Exception("Unknown property {}".format(prpt_names[0]))

                # has format like [(id, value)]
                new_values = []
                for p in cur.fetchall():
                    if delimiter in p[0]:
                        if originalProperty in p[0].split(delimiter):
                            # keep original order if multiple properties
                            xxx = delimiter.join([new_prpt_value if x == originalProperty else x for x in p[0].split(delimiter)])
                            new_values.append((xxx, p[1]))
                    elif originalProperty == p[0]:
                        new_values.append((new_prpt_value, p[1]))
                    else:
                        new_values.append((delimiter.join((p[0], new_prpt_value)), p[1]))
                if prpt_names[0] in tbl_elements_cols:
                    with self.dbconn:
                        self.dbconn.executemany("""UPDATE elements SET {0} = ? WHERE elem_id = ?""".format(prpt_names[0]),
                                                new_values)
                elif prpt_names[0] in tbl_pvs_cols:
                    with self.dbconn:
                        self.dbconn.executemany("""UPDATE pvs SET {0} = ? WHERE pv_id = ?""".format(prpt_names[0]),
                                                new_values)

def export_cf_localdata(dbname="cf_localdb.sqlite", **kwargs):
    """Export channel finder data from local SQLite database

    :param dbname: database file name

    - NULL/None or '' will be ignored
    - *properties*, a list of column names for properties
    - *pvcol* default 'pv', the column name for pv
    - *tagscol* default 'tags', the column name for tags
    - *tag_delimiter* default ';'

    The default properties will have all in 'elements' and 'pvs' tables except the pv and tags columns.

    tags are separated by ';'

    pv name can be duplicate (chained element).
    """
    conn = sqlite3.connect(dbname)
    # use byte string instead of the default unicode
    conn.text_factory = str
    cur = conn.cursor()
    cur.execute("select * from pvs, elements where pvs.elem_id = elements.elem_id")

    pv = kwargs.get('pv', 'pv')
    tags = kwargs.get('tags', 'tags')

    # get all column names for property names, excluding "elem_id", "pv", and "tags"
    allcols = [v[0] for v in cur.description if "elem_id" not in v and pv not in v and tags not in v]
    if len(allcols) == 0:
        raise RuntimeError("Wrong local channel finder database {0}".format(dbname))
    proplist= kwargs.get('properties', allcols)
    delimiter = kwargs.get('tag_delimiter', ';')

    cols_idx = [idx for idx in range(len(cur.description)) if cur.description[idx][0] in proplist]
    pv_idx = allcols.index(pv)
    tags_idx = allcols.index(tags)

    results= []
    for row in cur.fetchall():
        pv = row[pv_idx]
        prpts = {}
        for i in cols_idx:
            if i in [pv_idx, tags_idx]:
                # not record "pv", and "tags" columns
                continue
            if row[i] is None or row[i] == '':
                # ignore NULL and ''
                continue
            prpts[allcols[i]] = row[i]
        if not row[tags_idx]:
            tags = []
        else:
            tags = [v.strip().encode('ascii') for v in row[tags_idx].split(delimiter)]
        results.append([pv, prpts, tags])

    cur.close()
    conn.close()

    return results

def import_cf_localdata(data, dbname, overwrite=False, **kwargs):
    """Import data into SQLite local database, create a new one if overwrite is True,
    using a data set with a list of (pv, properties, tags)

    :oaram dbfname : str
    cflist :
    sep : str. ";". separate single string to a list.
    quiet : False. do not insert a log entry.

    It only updates columns which are in both DB table and data. The
    existing data will be updated and new data will be added.

    Ignore the tags if it is None.

    if pv is false, the pv part is not updated. Same as elemName part.


    :param data: list of (pv, properties, tags)
    :type data: list

    :param dbname: SQLite database name
    :type dbname:  string

    :param overwrite: create a new database if True
    :type overwrite: boolean

    :return:
    """
    if not os.path.isfile(dbname) or overwrite:
        # create a new database if overwrite is True
        create_cf_localdb(dbname=dbname, overwrite=overwrite, **kwargs)

    # delimeter to separate tags in database
    delimeter   = kwargs.get("delimeter", ";")
    quiet = kwargs.get("quiet", False)

    # elemName, elemType, system is "NOT NULL"
    conn = sqlite3.connect(dbname)
    # save byte string instead of the default unicode
    conn.text_factory = str
    cur = conn.cursor()

    # new elements and pvs need to insert
    elem_sets = []
    elem_sets_key = []
    pv_sets = []
    pv_sets_pvs = []
    # process elements table and pvs table
    for rec in data:
        pv, prpts, tags = rec
        ukey = (prpts.get("elemIndex", None),
                prpts.get("elemType", ""),
                prpts.get("elemName", ""),
                )

        # skip if already in the to-be-inserted list
        # deprecated: elemName has to be unique
        # elemIndex has to be unique since one element might be split into many pieces
        if ukey[0] and ukey not in elem_sets_key:
            cur.execute("""SELECT EXISTS(SELECT * from elements where elemIndex=? and elemType=? and elemName=? LIMIT 1)""", 
                        (ukey[0], ukey[1], ukey[2],))
            res = cur.fetchone()
            # no need to insert if exists
            if res[0] == 0:
                # element index does not exist yet.
                elem_sets.append(ukey)
                # avoid element index + name, which has been added already
                #elem_sets_key.append((ukey[0], ukey[1], ukey[2]))
                elem_sets_key.append(ukey)
        ukey = (pv,
                prpts.get("elemField", ""), 
                prpts.get("elemHandle", "")
                )
        if pv and pv not in pv_sets_pvs:
            cur.execute("""SELECT EXISTS(SELECT * from pvs where pv=? LIMIT 1)""", (pv,))
            res = cur.fetchone()
            if res[0] == 0:
                # pv does not exist yet.
                pv_sets.append(ukey)
                # not to add the pv again
                pv_sets_pvs.append(pv) 
        
    for elem in elem_sets:
        _logger.debug("adding new element: {0}".format(elem))
    for pv in pv_sets:
        _logger.debug("adding new pv: {0}".format(pv))
    with conn:
        conn.executemany("""INSERT INTO elements (elemIndex, elemType, elemName) VALUES (?,?,?)""", elem_sets)
        conn.executemany("""INSERT INTO pvs (pv, elemField, elemHandle) VALUES (?,?,?)""", pv_sets)
    _logger.debug("added {0} elements".format(len(elem_sets)))
    _logger.debug("added {0} pvs".format(len(pv_sets)))

    cur.execute("begin")
    cur.execute("PRAGMA table_info(elements)")
    tbl_elements_cols = [v[1] for v in cur.fetchall()]
    # update the elements table if data has the same column
    for col in tbl_elements_cols:
        # element index with element name is unique 
        if col in ["elemIndex", "elemType", "elemName"]:
            continue
        vals = []
        for rec in data:
            pv, prpts, tags = rec
            if col not in prpts:
                continue
            vals.append((prpts[col], prpts["elemIndex"], prpts["elemType"], prpts["elemName"]))
        if len(vals) == 0:
            _logger.debug("elements: no data for column '{0}'".format(col))
            continue
        try:
            cur.executemany("UPDATE elements set %s=? where elemIndex=? and elemType=? and elemName=?" % col, vals)
        except:
            raise RuntimeError("Error at updating {0} {1}".format(col, vals))

        # conn.commit()
        _logger.debug("elements: updated column '{0}' with {1} records".format(
                col, len(vals)))

    cur.execute("PRAGMA table_info(pvs)")
    tbl_pvs_cols = [v[1] for v in cur.fetchall()]
    for col in tbl_pvs_cols:
        if col in ['pv', 'elemField', 'elemHandle', 'tags']:
            continue
        vals = []
        for rec in data:
            pv, prpts, tags = rec
            if col not in prpts:
                continue
            if not prpts.has_key("elemField") or not prpts.has_key("elemIndex"):
                # @TODO to be convert to log instead of print to screen
                print("Incomplete record for pv={0}: {1} {2}".format(
                    pv, prpts, tags))
                continue
            # elemGroups is a list
            vals.append((prpts[col], pv, prpts["elemField"]))

        if len(vals) == 0:
        #     _logger.debug("pvs: no data for column '{0}'".format(col))
            continue
        cur.executemany("""UPDATE pvs set %s=? where pv=? and elemField=?"""% col, vals)
 
        # conn.commit()
        _logger.debug("pvs: updated column '{0}' with {1} records '{2}'".format(
                col, len(vals), [v[0] for v in vals]))

    # # update tags
    vals = []
    for rec in data:
        pv, prpts, tags = rec
        if tags is None: 
            continue
        if not prpts.has_key("elemField") or not prpts.has_key("elemIndex"):
            # @TODO to be convert to log instead of print to screen
            print("Incomplete record for pv={0}: {1} {2}. IGNORED".format(
                pv, prpts, tags))
            continue
        vals.append((delimeter.join(sorted(tags)), pv, prpts["elemField"]))
    if len(vals) > 0:
        cur.executemany("""UPDATE pvs set tags=? where pv=? and elemField=?""", vals)
        # conn.commit()
        _logger.debug("pvs: updated tags for {0} rows".format(len(vals)))

    if not quiet:
        msg = "channel finder local database updated %d records" % (len(data))
        cur.execute("""insert into log(timestamp, message) values (datetime('now'), ? )""", (msg,))

    cur.execute("DELETE FROM elements__pvs")
    pre_pv = ""
    pre_elem = ""
    pre_elem_type=""
    pre_elemIdx = 0
    pvid = 0
    elemid = 0
    values = []
    for rec in data:
        pv, prpts, _ = rec
        if pv != pre_pv:
            cur.execute("SELECT pv_id from pvs where pv = ?", (pv,))
            pvid = cur.fetchone()[0]
            pre_pv = pv
        if pre_elem != prpts['elemName'] or pre_elemIdx != prpts['elemIndex'] or pre_elem_type != prpts['elemType']:
            pre_elem = prpts['elemName']
            pre_elemIdx = prpts['elemIndex']
            pre_elem_type = prpts['elemType']
            cur.execute("SELECT elem_id from elements where elemName = ? and elemType=? and elemIndex = ?", 
                        (pre_elem, pre_elem_type, pre_elemIdx))
            elemid = cur.fetchone()
            if elemid is None:
                raise ValueError("Cannot find elem_id for element (name: {0}, index: {1}) in elements table".
                                 format(pre_elem, pre_elemIdx))
            elemid = elemid[0]
        values.append([pvid, elemid])
    cur.executemany("INSERT INTO elements__pvs (pv_id, elem_id) VALUES (?, ?)", values)
    try:
        conn.commit()
    except conn.Error:
        conn.rollback()
        conn.close()
        raise

    conn.close()

def create_cf_localdb(dbname="cf_localdb.sqlite", overwrite=False, colheads=None):
    """Create a local SQLite database for channel finder local caching purpose using SQLAlchemy library.

    It has 4 tables, which are elements, pvs, and log, and mapping table to link elements and pvs 
    since they are N:M mapping.
    The element table is to save all element information with elem_id as primary key.
    It has columns by default:
        elem_id:        integer
        elemName:       string
        elemType:       string
        system:         string
        elemPosition:   float
        elemLength:     float
        elemIndex:      integer
        elemGroup:      string
        virtual:        integer
    User could customize more columns, for example:
        cell:           string
        girder:         string
        symmetry:       string

    The pvs table is to save pv related information. It uses pv name as primary key,
    and has foreign key pointing to element table. Its columns are as below:
        devName:        string
        elemHandle:     string
        elemField:      string
        tags:           string
        hostname:       string
        iocname:        float

    The log table is to save history information, which has columns as:
        log_id:         integer
        timestamp:      time stamp
        message:        string


    Constraints:

    - elemName is unique
    - (pv,elemName,elemField) is unique
    - elemType can not be NULL


    :param dbname: string
    :param overwrite: boolean, force to overwrite existing database file, False by default.
    :return:
    """
    if os.path.isfile(dbname) and not overwrite:
        # if db file exists already and not to overwrite existing db file
        return

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
                  {0}
                  fieldPolar    INTEGER,
                  virtual       INTEGER DEFAULT 0,
                  UNIQUE (elemName, elemType, elemIndex) ON CONFLICT FAIL
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

    extra = """
    """

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

    if colheads is not None:
        for key in colheads:
            if key.upper() not in keys and key is not None and key.strip() != "":
                extra += """                  {0}          TEXT,""".format(key)

    conn = sqlite3.connect(dbname)

    # cur = conn.cursor()
    # cur.executescript(sqlcmd.format(extra))
    # cur.execute("""insert into log(timestamp, message)
    #              values (datetime('now'), "channel finder local database created")""")
    # conn.commit()
    # Use connection objects context managers that automatically commit or rollback transactions.
    # In the event of an exception, the transaction is rolled back; otherwise, the transaction is committed:
    with conn:
        conn.executescript(sqlcmd.format(extra))
        conn.execute("""insert into log(timestamp, message)
                     values (datetime('now'), "channel finder local database created")""")

    conn.close()

if __name__ == "__main__":
    # see contrib
    pass
    #from phyutil.phylib.common import read_csv
    #results = read_csv('../../../demo/impact_va.csv')
    #create_cf_localdb(dbname='example.sqlite', overwrite=True, colheads=results[0][1].keys())

    # print results

    #importCfLocalData(results, "example.sqlite", overwrite=True)
