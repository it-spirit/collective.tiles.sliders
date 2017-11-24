# -*- coding: utf-8 -*-
"""Slider tile based on responsiveslides.js."""

from collective.tiles.sliders import _
from collective.tiles.sliders.base import BaseSliderTile
from collective.tiles.sliders.base import ISliderBase
from collective.tiles.sliders.base import ISliderLayout
from collective.tiles.sliders.base import ISliderSettings
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary


class ISliderTile(ISliderBase, ISliderSettings, ISliderLayout):
    """A tile that shows a slider."""

    namespace = schema.Choice(
        default='centered-btns',
        description=_(u'Select one of the default themes.'),
        title=_(u'Theme'),
        vocabulary=SimpleVocabulary([
            SimpleVocabulary.createTerm(
                'centered-btns',
                'centered-btns',
                _(u'Centered Buttons'),
            ),
            SimpleVocabulary.createTerm(
                'transparent-btns',
                'transparent-btns',
                _(u'Transparent Buttons'),
            ),
            SimpleVocabulary.createTerm(
                'large-btns',
                'large-btns',
                _(u'Large Buttons'),
            ),
        ]),
    )


class SliderTile(BaseSliderTile):
    """A tile that shows a slider."""
