""" aLL Functions to build the xml"""

import datetime
import json
import re
import xml.etree.ElementTree as ET
from json import JSONEncoder, loads
from xml.etree.ElementTree import canonicalize, fromstring

import pandas as pd
from dicttoxml import dicttoxml


class SummarizeRange:
    """
    Class to summarize integers into range
    """

    def __init__(self, value: str):

        self.value = value

    def integerlst(self):
        striplst = self.value.strip()
        splitlst = striplst.split(',')
        cleantlst = list(filter(None, splitlst))  ## remove the empty strings from the list
        mylst = list(map(int, cleantlst))  ## convert the list to ints
        return mylst

    def gen_ranges(self):
        """
        Func that create join all nums in range
        :param list: list of int
        :type lst:
        """
        s = e = None
        for i in sorted(self.integerlst()):

            if s is None:
                s = e = i
            elif i == e or i == e + 1:
                e = i
            else:
                yield s, e
                s = e = i
        if s is not None:
            yield s, e

    def apply(self):
        """
        apply gen_range()
        """
        return (','.join(
            ['%d' % s if s == e else '%d-%d' % (s, e) for (s, e) in self.gen_ranges()]))


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        """

        Parameters
        ----------
        obj : datetime.date or datetime.datetime

        Returns
        -------
         ISO format date

        """
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


def convert2XML(dict_or_df=None, filename=None, mode="w", custome_root="item", item_func="item"):
    """
    - This function takes a DF (func will convert it to a dic) or a Dictionary and converts it to XML Format. Either store it as
    an XML Element(xml: <class 'xml.etree.ElementTree.Element'>) or save it as an  XML file

    Args:
        dict_or_df (): pandas dataframe or a dictionary
        filename (str): xml file name
        mode (str): Default is 'w',  W = write or a = append.
        custom_root (str): the xml table Parent tag, can be used with DF n Dic,Default is 'item' to be removed
        item_func (str):the xml table Child tag, mainly used with dic data,Default is 'item' to be removed

    Returns:
        xml element class (xml: <class 'xml.etree.ElementTree.Element'>)
        or
        xml file
    """
    if isinstance(dict_or_df, pd.DataFrame):
        json_data = dict_or_df.T.to_dict()
    else:
        json_data = dict_or_df

    def dict2xml(custome_root=custome_root, item_func=item_func):
        """
        Args:
            custome_root (str): the xml table Parent tag, can be used with DF n Dict
            item_func (str):the xml table Child tag, mainly used with dict data

        Returns:
            if filename was provided, then it saves XML file
            elas: it saves it as XML element through executing "fromstring(xml)"

        """
        unwanted_nodes = {"<item>": "", "</item>": "", "<n0>": '', "</n0>": "", "<n1>": '',
                          "</n1>": ""}  ## can take any string that need to
        # be replaces
        dictxml = dicttoxml(loads(json.dumps(json_data, indent=1, cls=DateTimeEncoder)), attr_type=False,
                            custom_root=custome_root, item_func=lambda _: item_func).decode("utf-8")
        """ dicttoxml(): Converts a python object into XML.
        Arguments:
        - root specifies whether the output is wrapped in an XML root element
          Default is True
        - custom_root allows you to specify a custom root element.
          Default is 'root' modified to 'item'
        - item_func specifies what function should generate the element name for
          items in a list.
          Default is 'item'
        """
        xml = re.sub(
            "|".join(unwanted_nodes),
            lambda match: unwanted_nodes[match.group()],
            dictxml,
        ).replace('<?xml version="1.0" encoding="UTF-8" ?>', "")
        return xml

    xml = dict2xml()
    if filename is None:
        return fromstring(xml)  # type xml: <class 'xml.etree.ElementTree.Element'>
    with open(filename, mode) as f:
        f.write(xml)


def insert_xmltree(**kwargs):
    """
    - This func is to insert XML block/single node inside another xml node, at any desired position
    - It inserts the name of subChild tag inside the name of Child tag that was given as a parameter.
    - Then it extends the SubChild tag with str_xml.
    Prams:
        - xml (type <class 'xml.etree.ElementTree.Element'>) : xml element tree, was created in 'convert2XML()'
        - myChild (type str): Tag name of the child that will take inside its subChild Tags
        - filename: xml file
        - subChild_tag (type str): Tag name that will hold the str_xml tree
    Exception:
        - To identify where to indent the xml elm,  at the root level (before the parent end tag) or after a specific node/tag
        if myChild (str):, was provided then indentation will be after the myChild tag
        else: indentation will be at the root level (before the parent end tag)

    """
    tree = ET.parse(kwargs['filename'])  # open XML file to parse it, return an ElementTree instance
    root = tree.getroot()  # get thr root elm
    # print(f"myroot name: {root.tag} and Child: {kwargs['subChild_tag']}")

    try:
        # print('exception: NOT at the root level')
        # ** indentation will be after the myChild
        myChild = root.find(kwargs['myChild'])
        subChild = ET.SubElement(myChild, kwargs['subChild_tag'])
    except:
        # ** indentation will be at the root level
        subChild = ET.SubElement(root, kwargs['subChild_tag'])
    subChild.extend(kwargs['xml'])  # str_xml : <class 'xml.etree.ElementTree.Element'>
    tree = ET.ElementTree(root)
    tree.write(kwargs['filename'])


def append_xmltree(distFile, sourceFile, mode):
    """Fun that takes a well XML format (has a parent tag) file and append it into another XMl file
    Args:
        distFile (xml file): XML file that have the table Header (tob part) of the inner tables
        sourceFile (xml file): Transitional XML, that keep writing the inner table from a loop | keep insterting each inner table under its Header in distFile.xml file
        mode (a): Default is 'a'
    """
    with open(distFile, mode="a", encoding="utf-8") as main_file:
        canonicalize(from_file=sourceFile, out=main_file)


def node_wrapper(sourceFile, distFile, parent_tag="item", end_tag="item", mode="a"):
    """
    Same as append_xmltree,
    1st opne XML file
    2nd copy and past it into another XML file wille sounding it with Parent and End tag
    Args:
        sourceFile (str): Source xml file, func will open to read
        distFile (str): destination xml file, func will past/write into it
        parent_tag (str): the Tag that will wrapp the source xml and write it into the distfile
        end_tag (str): Most of the time it will be same as parent_tag
        mode (str): w or a

    Returns:

    """
    try:
        with open(sourceFile) as f:
            # create the <Parent> node n wrap the whole xml
            wrappedxml = f"<{parent_tag}>" + f.read() + f"</{end_tag}>"
            with open(distFile, mode) as f:
                f.write(wrappedxml)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print("Script: XMLbuilder_Utilities.py")
