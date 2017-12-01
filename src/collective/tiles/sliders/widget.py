# -*- coding: utf-8 -*-
"""Custom widgets."""

from collective.tiles.sliders.interfaces import ICollectiveTilesSlidersLayer
from z3c.form.browser.checkbox import SingleCheckBoxWidget
from z3c.form.interfaces import IFieldWidget
from zope.component import adapter
from zope.interface import implementer
from zope.schema.interfaces import IField

import z3c.form.widget


@adapter(IField, ICollectiveTilesSlidersLayer)
@implementer(IFieldWidget)
def UseQueryFieldWidget(field, request):
    widget = z3c.form.widget.FieldWidget(field, SingleCheckBoxWidget(request))
    widget.addClass('pat-dynamicform')
    return widget
