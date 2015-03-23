"""
Local cache for channel finder service.

:author: Guobao Shen <shen@frib.msu.edu>
"""

import os
import sqlite3

import logging
_logger = logging.getLogger(__name__)


class ChannelFinderLocal:
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
        args = []
        channames = kwargs.get("name", "*")
        properties = kwargs.get("property", None)
        tags = kwargs.get("tagName", None)
        sql = """SELECT * from pvs join elements on pvs.elem_id = elements.elem_id where """
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
        # sql += """ ESCAPE "\\" """

        # print sql, querycons
        cur = self.dbconn.cursor()
        cur.execute(sql, querycons)

        properties = [prpts[0] for prpts in cur.description]

        return (properties, cur.fetchall())

#     def findProperty(self, propertyName):
#         '''
#         Searches for the _exact_ propertyName and return a single Property object if found
#         '''
#         url = self.__baseURL + self.__propertiesResource + '/' + propertyName
#         r = requests.get(url, headers=copy(self.__jsonheader), verify=False)
#         try:
#             r.raise_for_status()
#             return self.__decodeProperty(r.json())
#         except:
#             if r.status_code == 404:
#                 return None
#             else:
#                 r.raise_for_status()
#
#     def getAllTags(self):
#         '''
#         return a list of all the Tags present - even the ones not associated w/t any channel
#         '''
#         url = self.__baseURL + self.__tagsResource
#         r = requests.get(url, headers=copy(self.__jsonheader), verify=False)
#         try:
#             r.raise_for_status()
#             return self.__decodeTags(r.json())
#         except:
#             if r.status_code == 404:
#                 return None
#             else:
#                 r.raise_for_status()
#
#     def getAllProperties(self):
#         '''
#         return a list of all the Properties present - even the ones not associated w/t any channel
#         '''
#         url = self.__baseURL + self.__propertiesResource
#         r = requests.get(url, headers=copy(self.__jsonheader), verify=False)
#         try:
#             r.raise_for_status()
#             return self.__decodeProperties(r.json())
#         except:
#             if r.status_code == 404:
#                 return None
#             else:
#                 r.raise_for_status()
#
#     def delete(self, **kwds):
#         '''
#         Method to delete a channel, property, tag
#         delete(channelName = String)
#         >>> delete(channelName = 'ch1')
#
#         delete(tagName = String)
#         >>> delete(tagName = 'myTag')
#         # tagName = tag name of the tag to be removed from all channels
#
#         delete(propertyName = String)
#         >>> delete(propertyName = 'position')
#         # propertyName = property name of property to be removed from all channels
#
#         delete(tag = Tag ,channelName = String)
#         >>> delete(tag=Tag('myTag','tagOwner'), channelName = 'chName')
#         # delete the tag from the specified channel _chName_
#
#         delete(tag = Tag ,channelNames = [String])
#         >>> delete(tag=Tag('myTag','tagOwner'), channelNames=['ch1','ch2','ch3'])
#         # delete the tag from all the channels specified in the channelNames list
#
#         delete(property = Property ,channelName = String)
#         >>> delete(property = Property('propName','propOwner') ,channelName = 'chName')
#         # delete the property from the specified channel
#
#         delete(property = Property ,channelNames = [String])
#         >>> delete(property = Property('propName','propOwner') ,channelNames = ['ch1','ch2','ch3'])
#         # delete the property from all the channels in the channelNames list
#         '''
#         if len(kwds) == 1:
#             self.__handleSingleDeleteParameter(**kwds)
#         elif len(kwds) == 2:
#             self.__handleMultipleDeleteParameters(**kwds)
#         else:
#             raise Exception, 'incorrect usage: Delete a single Channel/tag/property'
#
#     def __handleSingleDeleteParameter(self, **kwds):
#         if 'channelName' in kwds:
#             url = self.__baseURL + self.__channelsResource + '/' + kwds['channelName'].strip()
#             requests.delete(url, \
#                             headers=copy(self.__jsonheader), \
#                             verify=False, \
#                             auth=self.__auth).raise_for_status()
#             pass
#         elif 'tagName' in kwds:
#             url = self.__baseURL + self.__tagsResource + '/' + kwds['tagName'].strip()
#             requests.delete(url, \
#                             verify=False, \
#                             headers=copy(self.__jsonheader), \
#                             auth=self.__auth).raise_for_status()
#             pass
#         elif 'propertyName' in kwds:
#             url = self.__baseURL + self.__propertiesResource + '/' + kwds['propertyName'].strip()
#             requests.delete(url, \
#                             headers=copy(self.__jsonheader), \
#                             verify=False, \
#                             auth=self.__auth).raise_for_status()
#             pass
#         else:
#             raise Exception, ' unkown key use channelName, tagName or proprtyName'
#
#     def __handleMultipleDeleteParameters(self, **kwds):
#         if 'tag' in kwds and 'channelName' in kwds:
#             requests.delete(self.__baseURL + self.__tagsResource + '/' + kwds['tag'].Name + '/' + kwds['channelName'].strip(), \
#                             headers=copy(self.__jsonheader), \
#                             verify=False, \
#                             auth=self.__auth).raise_for_status()
#         elif 'tag' in kwds and 'channelNames' in kwds:
#             # find channels with the tag
#             channelsWithTag = self.find(tagName=kwds['tag'].Name)
#             # delete channels from which tag is to be removed
#             channelNames = [channel.Name for channel in channelsWithTag if channel.Name not in kwds['channelNames']]
#             self.set(tag=kwds['tag'], channelNames=channelNames)
#         elif 'property' in kwds and 'channelName' in kwds:
#             requests.delete(self.__baseURL + self.__propertiesResource + '/' + kwds['property'].Name + '/' + kwds['channelName'], \
#                             headers=copy(self.__jsonheader), \
#                             verify=False, \
#                             auth=self.__auth).raise_for_status()
#         elif 'property' in kwds and 'channelNames' in kwds:
#             channelsWithProp = self.find(property=[(kwds['property'].Name, '*')])
#             channels = [channel for channel in channelsWithProp if channel.Name not in kwds['channelNames']]
#             self.set(property=kwds['property'], channels=channels)
#         else:
#             raise Exception, ' unkown keys'
#
# #===============================================================================
# # Update methods
# #===============================================================================
#     def update(self, **kwds):
#         '''
#         update(channel = Channel)
#         >>> update(channel = Channel('existingCh',
#                                      'chOwner',
#                                      properties=[
#                                         Property('newProp','propOwner','Val'),
#                                         Property('existingProp','propOwner','newVal')],
#                                      tags=[Tag('mytag','tagOwner')])
#         # updates the channel 'existingCh' with the new provided properties and tags
#         # without affecting the other tags and properties of this channel
#
#         update(property = Property, channelName = String)
#         >>> update(property=Property('propName', 'propOwner', 'propValue'),
#                                     channelName='ch1')
#         # Add Property to the channel with the name 'ch1'
#         # without affecting the other channels using this property
#
#         >>>update(property=Property('propName', 'propOwner', 'propValue'),
#                                     channelNames=['ch1','ch2','ch3'])
#         # Add Property to the channels with the names in the list channelNames
#         # without affecting the other channels using this property
#
#         update(tag = Tag, channelName = String)
#         >>> update(tag = Tag('myTag','tagOwner'), channelName='chName')
#         # Add tag to channel with name chName
#         # without affecting the other channels using this tag
#
#         update(tag = Tag, channelNames = [String])
#         >>> update(tag = Tag('tagName'), channelNames=['ch1','ch2','ch3'])
#         # Add tag to channels with names in the list channeNames
#         # without affecting the other channels using this tag
#         update(property = Property)
#         update(tag = Tag)
#
#         ## RENAME OPERATIONS ##
#         update(channel = Channel, originalChannelName = String)
#         >>> update(channel = Channel('newChannelName','channelOwner),
#                                      originalChannelName = 'oldChannelName')
#         # rename the channel 'oldChannelName' to 'newChannelName'
#
#         update(property = Property, originalPropertyName = String)
#         >>> update(property = Property('newPropertyName','propOwner'),
#                                        originalPropertyName = 'oldPropertyName')
#         # rename the property 'oldPropertyName' to 'newPropertyName'
#         # the channels with the old property are also updated
#
#         update(tab = Tag, originalTagName = String)
#         >>> update(tab = Tag('newTagName','tagOwner'), originalTagName = 'oldTagName')
#         # rename the tag 'oldTagName' to 'newTagName'
#         # the channel with the old tag are also updated
#         '''
#
#         if not self.__baseURL:
#             raise Exception, 'Olog client not configured correctly'
#         if len(kwds) == 1:
#             self.__handleSingleUpdateParameter(**kwds)
#         elif len(kwds) == 2:
#             self.__handleMultipleUpdateParameters(**kwds)
#         else:
#             raise Exception, 'incorrect usage: '
#
#     def __handleSingleUpdateParameter(self, **kwds):
#         if 'channel' in kwds:
#             ch = kwds['channel']
#             requests.post(self.__baseURL + self.__channelsResource + '/' + ch.Name, \
#                                      data=JSONEncoder().encode(self.__encodeChannel(ch)), \
#                                      headers=copy(self.__jsonheader), \
#                                      verify=False, \
#                                      auth=self.__auth).raise_for_status()
#         elif 'property' in kwds:
#             property = kwds['property']
#             requests.post(self.__baseURL + self.__propertiesResource + '/' + property.Name, \
#                                      data=JSONEncoder().encode(self.__encodeProperty(property)), \
#                                      headers=copy(self.__jsonheader), \
#                                      verify=False, \
#                                      auth=self.__auth).raise_for_status()
#         elif 'tag' in kwds:
#             tag = kwds['tag']
#             requests.post(self.__baseURL + self.__tagsResource + '/' + tag.Name, \
#                           data=JSONEncoder().encode(self.__encodeTag(tag)), \
#                           headers=copy(self.__jsonheader), \
#                           verify=False, \
#                           auth=self.__auth).raise_for_status()
#         else:
#             raise Exception, ' unkown key '
#
#     def __handleMultipleUpdateParameters(self, **kwds):
#         if 'tag' in kwds and 'channelName' in kwds:
#             tag = kwds['tag']
#             channels = [Channel(kwds['channelName'].strip(), self.__userName)]
#             requests.post(self.__baseURL + self.__tagsResource + '/' + tag.Name, \
#                           data=JSONEncoder().encode(self.__encodeTag(tag, withChannels=channels)), \
#                           headers=copy(self.__jsonheader), \
#                           verify=False, \
#                           auth=self.__auth).raise_for_status()
#         elif 'tag' in kwds and 'channelNames' in kwds:
#             tag = kwds['tag']
#             channels = []
#             for eachChannel in kwds['channelNames']:
#                 channels.append(Channel(eachChannel, self.__userName))
#             requests.post(self.__baseURL + self.__tagsResource + '/' + tag.Name, \
#                           data=JSONEncoder().encode(self.__encodeTag(tag, withChannels=channels)), \
#                           headers=copy(self.__jsonheader), \
#                           verify=False, \
#                           auth=self.__auth).raise_for_status()
#         elif 'property' in kwds and 'channelName' in kwds:
#             property = kwds['property']
#             channels = [Channel(kwds['channelName'].strip(), self.__userName, properties=[property])]
#             requests.post(self.__baseURL + self.__propertiesResource + '/' + property.Name, \
#                           data=JSONEncoder().encode(self.__encodeProperty(property, withChannels=channels)), \
#                           headers=copy(self.__jsonheader), \
#                           verify=False, \
#                           auth=self.__auth).raise_for_status()
#         elif 'property' in kwds and 'channelNames' in kwds:
#             property = kwds['property']
#             channels = []
#             for eachChannel in kwds['channelNames']:
#                 channels.append(Channel(eachChannel, self.__userName, properties=[property]))
#             requests.post(self.__baseURL + self.__propertiesResource + '/' + property.Name, \
#                           data=JSONEncoder().encode(self.__encodeProperty(property, withChannels=channels)), \
#                           headers=copy(self.__jsonheader), \
#                           verify=False, \
#                           auth=self.__auth).raise_for_status()
#         elif 'originalChannelName' in kwds and 'channel' in kwds:
#             ch = kwds['channel']
#             channelName = kwds['originalChannelName'].strip()
#             requests.post(self.__baseURL + self.__channelsResource + '/' + channelName, \
#                           data=JSONEncoder().encode(self.__encodeChannel(ch)) , \
#                           headers=copy(self.__jsonheader), \
#                           verify=False, \
#                           auth=self.__auth).raise_for_status()
#         elif 'originalPropertyName' in kwds and 'property' in kwds:
#             prop = kwds['property']
#             propName = kwds['originalPropertyName'].strip()
#             requests.post(self.__baseURL + self.__propertiesResource + '/' + propName, \
#                           data=JSONEncoder().encode(self.__encodeProperty(prop)), \
#                           headers=copy(self.__jsonheader), \
#                           verify=False, \
#                           auth=self.__auth).raise_for_status()
#         elif 'originalTagName' in kwds and 'tag' in kwds:
#             tag = kwds['tag']
#             tagName = kwds['originalTagName'].strip()
#             requests.post(self.__baseURL + self.__tagsResource + '/' + tagName, \
#                           data=JSONEncoder().encode(self.__encodeTag(tag)), \
#                           headers=copy(self.__jsonheader), \
#                           verify=False, \
#                           auth=self.__auth).raise_for_status()
#         else:
#             raise Exception, ' unkown keys'
#
# #===============================================================================
# # Methods for encoding decoding will be make private
# #===============================================================================
#     @classmethod
#     def __decodeChannels(cls, body):
#         '''
#         decode the representation of a list of channels to a list of Channel objects
#         '''
#         if not body[u'channels']:
#             return None
#         channels = []
#         # if List then Multiple channels are present in the body
#         if isinstance(body[u'channels']['channel'], list):
#             for channel in body['channels']['channel']:
#                 channels.append(cls.__decodeChannel(channel))
#         # if Dict the single channel present in the body
#         elif isinstance(body[u'channels']['channel'], dict):
#             channels.append(cls.__decodeChannel(body[u'channels']['channel']))
#         return channels
#
#     @classmethod
#     def __decodeChannel(self, body):
#         '''
#         decode the representation of a channel to the Channel object
#         '''
#         return Channel(body[u'@name'], body[u'@owner'], properties=self.__decodeProperties(body), tags=self.__decodeTags(body))
#
#     @classmethod
#     def __decodeProperties(cls, body):
#         '''
#         decode the representation of a list of properties to a list of Property object
#         '''
#         ## TODO handle the case where there is a single property dict
#         if body[u'properties'] and body[u'properties']['property']:
#             properties = []
#             if isinstance(body[u'properties']['property'], list):
#                 for validProperty in [ property for property in body[u'properties']['property'] if '@name' in property and '@owner' in property]:
#                         properties.append(cls.__decodeProperty(validProperty))
#             elif isinstance(body[u'properties']['property'], dict):
#                 properties.append(cls.__decodeProperty(body[u'properties']['property']))
#             return properties
#         else:
#             return None
#
#     @classmethod
#     def __decodeProperty(cls, propertyBody):
#         '''
#         decode the representation of a property to a Property object
#         '''
#         if '@value' in propertyBody:
#             return Property(propertyBody['@name'], propertyBody['@owner'], propertyBody['@value'])
#         else:
#             return Property(propertyBody['@name'], propertyBody['@owner'])
#
#     @classmethod
#     def __decodeTags(cls, body):
#         '''
#         decode the representation of a list of tags to a list of Tag objects
#         '''
#         ## TODO handle the case where there is a single tag dict
#         if body[u'tags'] and body[u'tags']['tag']:
#             tags = []
#             if isinstance(body[u'tags']['tag'], list):
#                 for validTag in [ tag for tag in body[u'tags']['tag'] if '@name' in tag and '@owner' in tag]:
#                     tags.append(cls.__decodeTag(validTag))
#             elif isinstance(body[u'tags']['tag'], dict):
#                 tags.append(cls.__decodeTag(body[u'tags']['tag']))
#             return tags
#         else:
#             return None
#
#     @classmethod
#     def __decodeTag(cls, tagBody):
#         '''
#         decode a representation of a tag to the Tag object
#         '''
#         return Tag(tagBody['@name'], tagBody['@owner'])
#
#     @classmethod
#     def __encodeChannels(cls, channels):
#         '''
#         encodes a list of Channels
#         '''
#         ret = {u'channels':{}}
#         if len(channels) == 1:
#             ret[u'channels'] = {u'channel':cls.__encodeChannel(channels[0])}
#         elif len (channels) > 1:
#             ret[u'channels'] = {u'channel':[]}
#             for channel in channels:
#                 if issubclass(channel.__class__, Channel):
#                     ret[u'channels'][u'channel'].append(cls.__encodeChannel(channel))
#         return ret
#
#     @classmethod
#     def __encodeChannel(cls, channel):
#         '''
#         encodes a single channel
#         '''
#         d = {}
#         d['@name'] = channel.Name
#         d['@owner'] = channel.Owner
#         if channel.Properties:
#             d['properties'] = {'property':cls.__encodeProperties(channel.Properties)}
#         if channel.Tags:
#             d['tags'] = {'tag':cls.__encodeTags(channel.Tags)}
#         return d
#
#     @classmethod
#     def __encodeProperties(cls, properties):
#         '''
#         encodes a list of properties
#         '''
#         d = []
#         for validProperty in [ property for property in properties if issubclass(property.__class__, Property)]:
#                 d.append(cls.__encodeProperty(validProperty))
#         return d
#
#     @classmethod
#     def __encodeProperty(cls, property, withChannels=None):
#         '''
#         encodes a single property
#         '''
#         if not withChannels:
#             if property.Value or property.Value is '':
#                 return {'@name':str(property.Name), '@value':property.Value, '@owner':property.Owner}
#             else:
#                 return {'@name':str(property.Name), '@owner':property.Owner}
#         else:
#             d = OrderedDict([('@name', str(property.Name)), ('@value', property.Value), ('@owner', property.Owner)])
#             d.update(cls.__encodeChannels(withChannels))
#             return d
#
#     @classmethod
#     def __encodeTags(cls, tags):
#         '''
#         encodes a list of tags
#         '''
#         d = []
#         for validTag in [ tag for tag in tags if issubclass(tag.__class__, Tag)]:
#             d.append(cls.__encodeTag(validTag))
#         return d
#
#     @classmethod
#     def __encodeTag(cls, tag, withChannels=None):
#         '''
#         encodes a single tag
#         '''
#         if not withChannels:
#             return {'@name':tag.Name, '@owner':tag.Owner}
#         else:
#             d = OrderedDict([('@name', tag.Name), ('@owner', tag.Owner)])
#             d.update(cls.__encodeChannels(withChannels))
#             return d


def exportCfLocalData(dbname="cf_localdb.sqlite", **kwargs):
    """export channel finder data from local SQLite database

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
    delimeter = kwargs.get('tag_delimiter', ';')

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
            tags = [v.strip().encode('ascii') for v in row[tags_idx].split(delimeter)]
        results.append([pv, prpts, tags])

    cur.close()
    conn.close()

    return results

def importCfLocalData(data, dbname, overwrite=False, **kwargs):
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
    elem_sets, pv_sets = [], []
    elem_sets_key = []
    # process element table first
    for rec in data:
        pv, prpts, tags = rec
        ukey = (prpts.get("elemName", ""),
                prpts.get("elemType", ""))

        # skip if already in the to-be-inserted list
        # elemName has to be unique
        if ukey[0] and ukey[0] not in elem_sets_key:
            cur.execute("""SELECT EXISTS(SELECT * from elements where elemName=? LIMIT 1)""", (ukey[0],))
            res = cur.fetchone()
            # no need to insert if exists
            if res[0] == 0:
                # does not exist yet.
                elem_sets.append(ukey)
                elem_sets_key.append(ukey[0])
    for elem in elem_sets:
        _logger.debug("adding new element: {0}".format(elem))
    with conn:
        conn.executemany("""INSERT INTO elements (elemName, elemType) VALUES (?,?)""", elem_sets)
    _logger.debug("added {0} elements".format(len(elem_sets)))

    # handle pvs table
    elemId = {}
    for rec in data:
        pv, prpts, tags = rec
        # same as elemName, find the new pvs
        ukey = (pv, prpts.get("elemName", ""), prpts.get("elemField", ""))
        if pv and ukey not in pv_sets:
            cur.execute("""SELECT elem_id from elements where elemName=? """, (prpts.get("elemName", ""), ))
            elem_id = cur.fetchone()
            if elem_id is None:
                raise RuntimeError("Element ({0}) not found".format(prpts.get("elemName", "")))
            else:
                elem_id = elem_id[0]
                elemId ['elemName'] = elem_id
            cur.execute("""SELECT EXISTS(SELECT pvs.elem_id from pvs join elements on pvs.elem_id = elements.elem_id """
                        """ where pvs.pv=? and elements.elemName=? and pvs.elemField=?)""", ukey)
            if cur.fetchone()[0] == 0:
                pv_sets.append((pv, elem_id, prpts.get("elemField", ""), prpts.get("elemHandle", "")))

    for pv in pv_sets:
        _logger.debug("adding new pv: {0}".format(pv))
    with conn:
        conn.executemany("""INSERT INTO pvs (pv, elem_id, elemField, elemHandle) VALUES (?,?,?,?)""", pv_sets)
    _logger.debug("added {0} pvs".format(len(pv_sets)))

    cur.execute("begin")
    cur.execute("PRAGMA table_info(elements)")
    tbl_elements_cols = [v[1] for v in cur.fetchall()]
    # update the elements table if data has the same column
    for col in tbl_elements_cols:
        if col in ["elemName"]:
            continue
        vals = []
        for idx, rec in enumerate(data):
            pv, prpts, tags = rec
            if col not in prpts:
                continue
            vals.append((prpts[col], prpts["elemName"]))
        if len(vals) == 0:
            _logger.debug("elements: no data for column '{0}'".format(col))
            continue
        try:
            cur.executemany("UPDATE elements set %s=? where elemName=?" % col, vals)
        except:
            raise RuntimeError("Error at updating {0} {1}".format(col, vals))

        # conn.commit()
        _logger.debug("elements: updated column '{0}' with {1} records".format(
                col, len(vals)))

    cur.execute("PRAGMA table_info(pvs)")

    tbl_pvs_cols = [v[1] for v in cur.fetchall()]
    for col in tbl_pvs_cols:
        if col in ['pv', 'elem_id', 'elemField', 'tags']:
            continue
        vals = []
        for idx, rec in enumerate(data):
            pv, prpts, tags = rec
            if col not in prpts:
                continue
            if not prpts.has_key("elemField") or not prpts.has_key("elemName"):
                print("Incomplete record for pv={0}: {1} {2}".format(
                    pv, prpts, tags))
                continue
            # elemGroups is a list
            vals.append((prpts[col], pv, elemId["elemName"], prpts["elemField"]))

        if len(vals) == 0:
        #     _logger.debug("pvs: no data for column '{0}'".format(col))
            continue
        cur.executemany("""UPDATE pvs set %s=? where pv=? and """
                      """elem_id=? and elemField=?""" % col,
                      vals)
        # conn.commit()
        _logger.debug("pvs: updated column '{0}' with {1} records '{2}'".format(
                col, len(vals), [v[0] for v in vals]))

    # # update tags
    vals = []
    for idx,rec in enumerate(data):
        pv, prpts, tags = rec
        if tags is None: continue
        if not prpts.has_key("elemField") or not prpts.has_key("elemName"):
            print("Incomplete record for pv={0}: {1} {2}. IGNORED".format(
                pv, prpts, tags))
            continue
        vals.append((delimeter.join(sorted(tags)),
                     pv, elemId["elemName"], prpts["elemField"]))
    if len(vals) > 0:
        cur.executemany("""UPDATE pvs set tags=? where pv=? and elem_id=? and elemField=?""", vals)
        # conn.commit()
        _logger.debug("pvs: updated tags for {0} rows".format(len(vals)))

    if not quiet:
        msg = "channel finder local database updated %d records" % (len(data))
        cur.execute("""insert into log(timestamp, message) values (datetime('now'), ? )""", (msg,))

    try:
        conn.commit()
    except conn.Error:
        conn.rollback()
        conn.close()
        raise

    conn.close()

def create_cf_localdb(dbname="cf_localdb.sqlite", overwrite=False, colheads=None):
    """Create a local SQLite database for channel finder local caching purpose using SQLAlchemy library.

    It has 3 tables, which are elements, pvs, and log.
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

    CREATE TABLE log (log_id    INTEGER PRIMARY KEY,
                      timestamp TIMESTAMP NOT NULL,
                      message   TEXT);

    CREATE TABLE elements
                 (elem_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                  elemName      TEXT UNIQUE,
                  elemType      TEXT NOT NULL,
                  elemLength    REAL,
                  elemPosition  REAL,
                  elemIndex     INTEGER,
                  elemGroups    TEXT,
                  {0}
                  fieldPolar    INTEGER,
                  virtual       INTEGER DEFAULT 0);

    CREATE TABLE pvs
                 (pv_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                  pv            TEXT,
                  elem_id       TEXT,
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
                  archive INT   DEFAULT 0,
                  size    INT   DEFAULT 0,
                  epsilon REAL  DEFAULT 0.0,
                  UNIQUE (pv,elem_id, elemField) ON CONFLICT REPLACE,
                  FOREIGN KEY(elem_id) REFERENCES elements(elem_id))
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
    if __package__ is None:
        from os import sys, path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
        from common import read_csv
    else:
        from ..common import read_csv


    results = read_csv('../../../demo/impact_va.csv')
    create_cf_localdb(dbname='example.sqlite', overwrite=True, colheads=results[0][1].keys())

    # print results

    importCfLocalData(results, "example.sqlite")
