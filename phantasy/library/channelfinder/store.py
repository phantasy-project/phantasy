# encoding: UTF-8

"""Library for using local store for channel data."""

__copyright__ = "Copyright (c) 2015, Facility for Rare Isotope Beams"

__author__ = "Dylan Maxwell"


from collections import OrderedDict


class ChannelStore(object):
    """
    Local store for channel data.

    :param owner: default owner for properties and tags
    """

    def __init__(self, owner=None):
        self.owner = owner
        self.channels = OrderedDict()


    def set(self, channel, properties={}, tags=[]):
        """
        Set the properties and tags of the specified channel or list of channels.
        Note that this method is destructive and will remove data associated
        with the specified channel. To update the channel properties use the
        ChannelStore.update() method.

        :param channel: channel name or list of channel names.
        :param properties: dictionary of property values
        :param tags: list of tags
        """

        if isinstance(channel, (tuple,list)):
            channels = channel
        elif isinstance(channel, str):
            channels = [ channel ]
        else:
            raise TypeError("Channel name must a string or list of strings")
    
        for ch in channels:
            data = CSData()
       
            for name, value in properties.iteritems():
                p = self._toProperty(name)
                data.properties[p] = value
             
            for name in tags:
                t = self._toTag(name)
                if t not in data.tags:
                    data.tags.append(t)

            self.channels[ch] = data


    def update(self, channel, properties={}, tags=[]):
        """
        Update the properties and tags of the specified channel or list of channels.

        :param channel: channel name or list of channel names.
        :param properties: dictionary of property values
        :param tags: list of tags
        """

        if isinstance(channel, (tuple,list)):
            channels = channel
        elif isinstance(channel, str):
            channels = [ channel ]
        else:
            raise TypeError("Channel name must a string or list of strings")

        for ch in channels:
            if ch in self.channels:
                data = self.channels[ch]
            else:
                data = CSData()
                self.channels[ch] = data

            for name, value in properties.iteritems():
                p = self._toProperty(name)
                data.properties[p] = value
             
            for name in tags:
                t = self._toTag(name)
                if t not in data.tags:
                    data.tags.append(t)


    def query(self, channel="*", properties={}, tags=[]):
        """
        Query this channel store with the specified expressions.

        For example: store.query("*", { "system":"REA", "device":"BPM|PM" }, [ "T1" ]) 

        :params channel: expression to match the channel
        :params properties: dictionary of property expressions to match to property values
        :params tags: list of expressions to match to tags
        :return: ChannelStore
        """
        raise NotImplementedError()


    def properties(self, channel):
        """
        Get properties for the specified channel.

        :return: dictionary of property names and values
        """
        props = {}
        for prop, value in self.channels[channel].properties.iteritems():
            props[prop.name] = value
        return props


    def tags(self, channel):
        """
        Get tags for the specified channel.
        
        :return: list of tag names
        """
        tags = []
        for tag in self.channels[channel].tags:
            tags.append(tag.name)
        return tags


    def channelSet(self):
        """
        Get a list of channels in this store.
        """
        return self.channels.keys()


    def propertySet(self):
        """
        Search channel store and return a set of property names.

        :return: set of property names
        """
        props = set()
        for data in self.channels.values():
            for prop in data.properties.iterkeys():
                props.add(prop.name)
        return props


    def tagSet(self):
        """
        Search channel store and return a set of tag names.

        :return: set of tag names
        """
        tags = set()
        for data in self.channels.values():
            for tag in data.tags:
                tags.add(tag.name)
        return tags


    def cspropertySet(self):
        """
        Search channel store and return a set of properties.

        :return: set of properties
        """
        props = set()
        for data in self.channels.values():
            for prop in data.properties.iterkeys():
                props.add(prop)
        return props


    def cstagSet(self):
        """
        Search channel store and return a set of tags.

        :returns: set of tags
        """
        tags = set()
        for data in self.channels.values():
            for tag in data.tags:
                tags.add(tag)
        return tags


    def _toProperty(self, prop):
        """
        Convert a string, tuple or CSProperty object to a CSProperty.
        """
        if isinstance(prop, CSProperty):
            return CSProperty(prop.name, prop.owner)
        
        if isinstance(prop, str):
            return CSProperty(prop)
    
        if isinstance(prop, (tuple,list)) and (len(prop) > 0):
            if len(prop) > 1:
                return CSProperty(prop[0], prop[1])
            else:
                return CSProperty(prop[0])

        raise TypeError("Cannot build CSProperty from type: {}".format(type(prop)))


    def _toTag(self, tag):
        """
        Convert a string, tuple or CSTag object to a CSTag.
        """
        if isinstance(tag, CSTag):
            return CSTag(tag.name, tag.owner)
        
        if isinstance(tag, str):
            return CSTag(tag)
    
        if isinstance(tag, (tuple,list)) and (len(tag) > 0):
            if len(tag) > 1:
                return CSTag(tag[0], tag[1])
            else:
                return CSTag(tag[0])

        raise TypeError("Cannot build CSTag from type: {}".format(type(tag)))


class CSData(object):
    
    def __init__(self):
        self.tags = []
        self.properties = {}

    def __str__(self):
        return "CSData{ properties=" + str(self.properties) + ", tags=" + str(self.tags) + "}"


class CSProperty(object):

    def __init__(self, name, owner=None):
        self.name = name
        self.owner = owner

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "('" + str(self.name) + "', '" + str(self.owner) + "')"


class CSTag(object):

    def __init__(self, name, owner=None):
        self.name = name
        self.owner = owner

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "('" + str(self.name) + "', '" + str(self.owner) + "')"


