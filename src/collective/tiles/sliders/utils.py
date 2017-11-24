# -*- coding: utf-8 -*-
"""Utilities."""

from plone import api
from plone.app.querystring import queryparser
from plone.app.querystring.interfaces import IParsedQueryIndexModifier
from plone.app.uuid.utils import uuidToObject
from Products.ZCatalog.interfaces import ICatalogBrain
from zope.component import getUtilitiesFor


def parse_query_from_data(data, context=None):
    """Parse query from data dictionary"""
    if context is None:
        context = api.portal.get()
    query = data.get('query', {}) or {}
    try:
        parsed = queryparser.parseFormquery(context, query)
    except KeyError:
        parsed = {}

    index_modifiers = getUtilitiesFor(IParsedQueryIndexModifier)
    for name, modifier in index_modifiers:
        if name in parsed:
            new_name, query = modifier(parsed[name])
            parsed[name] = query
            # if a new index name has been returned, we need to replace
            # the native ones
            if name != new_name:
                del parsed[name]
                parsed[new_name] = query

    if data.get('sort_on'):
        parsed['sort_on'] = data['sort_on']
    if data.get('sort_reversed', False):
        parsed['sort_order'] = 'reverse'
    return parsed


def get_object(val):
    """Return the real object."""
    if ICatalogBrain.providedBy(val):
        return val.getObject()

    if not val:
        return None

    if isinstance(val, basestring):
        if val[0] == '/':
            # it's a path
            site = api.portal.get()
            return site.restrictedTraverse(val.strip('/'), None)
        else:
            # try querying catalog
            obj = uuidToObject(val)
            if obj:
                return obj
    if isinstance(val, basestring):
        return None
    return val
