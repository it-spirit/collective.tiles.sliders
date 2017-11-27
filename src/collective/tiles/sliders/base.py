# -*- coding: utf-8 -*-
"""Base tile classes."""

from collective.tiles.sliders import _
from collective.tiles.sliders.utils import get_object
from collective.tiles.sliders.utils import parse_query_from_data
from plone import api
from plone import tiles
from plone.app.z3cform.widget import QueryStringFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.autoform import directives as form
from plone.memoize import view
from plone.supermodel.model import Schema
from plone.tiles.interfaces import IPersistentTile
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IContextSourceBinder)
def image_scales(context):
    """Return custom source for image scales.

    This source also contains the original image.
    """
    values = []
    values.append(SimpleTerm('original', 'original', _(u'Original')))
    allowed_sizes = api.portal.get_registry_record(name='plone.allowed_sizes')
    for allowed_size in allowed_sizes:
        name = allowed_size.split()[0]
        values.append(SimpleTerm(name, name, allowed_size))
    return SimpleVocabulary(values)


class ISliderBase(Schema):
    """Basic Image Tile Schema."""

    use_query = schema.Bool(
        default=False,
        title=_(u'Use dynamic query'),
    )

    form.widget('images', RelatedItemsFieldWidget)
    images = schema.List(
        description=_(
            u'Select images or folders of images to display in slider'
        ),
        required=False,
        title=_(u'Images'),
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.Catalog',
        ),
    )

    form.widget('query', QueryStringFieldWidget)
    query = schema.List(
        description=_(
            u'Define the search terms for the images you want to use. '
            u'The list of results will be dynamically updated'
        ),
        required=False,
        title=_(u'Search terms'),
        value_type=schema.Dict(
            value_type=schema.Field(),
            key_type=schema.TextLine(),
        ),
    )

    sort_on = schema.TextLine(
        description=_(u'Sort on this index'),
        required=False,
        title=_(u'Sort on'),
    )

    sort_reversed = schema.Bool(
        description=_(u'Sort the results in reversed order'),
        required=False,
        title=_(u'Reversed order'),
    )

    image_scale = schema.Choice(
        default='large',
        title=_(u'Image Scale'),
        source=image_scales,
    )


class ISliderSettings(Schema):
    """Image Tile Settings Schema."""

    slideshow_speed = schema.Int(
        default=7000,
        description=_(u'Cycle speed in milliseconds.'),
        min=1,
        title=_(u'Slideshow Speed'),
    )

    animation_speed = schema.Int(
        default=600,
        description=_(u'Animation speed in milliseconds.'),
        min=1,
        title=_(u'Animation Speed'),
    )

    form.widget('autostart', RadioFieldWidget)
    autostart = schema.Bool(
        default=True,
        description=_(u'Should the slider start automatically?'),
        required=False,
        title=_(u'Autostart'),
    )

    form.widget('pager', RadioFieldWidget)
    pager = schema.Bool(
        default=True,
        description=_(u'Show the pager?'),
        required=False,
        title=_(u'Show Pager'),
    )

    form.widget('navigation', RadioFieldWidget)
    navigation = schema.Bool(
        default=True,
        description=_(u'Show the navigation?'),
        required=False,
        title=_(u'Show Navigation'),
    )

    form.widget('show_captions', RadioFieldWidget)
    show_captions = schema.Bool(
        default=False,
        description=_(
            u'Show captions for slides? It will use an image\'s description.'
        ),
        required=False,
        title=_(u'Show Captions'),
    )


class BaseTile(tiles.Tile):
    """Base tile implementation."""

    @property
    def title(self):
        return self.data.get('title', None)

    @property
    @view.memoize
    def site(self):
        return api.portal.get()

    @property
    @view.memoize
    def catalog(self):
        return api.portal.get_tool(name='portal_catalog')


@implementer(IPersistentTile)
class ContentTile(BaseTile):
    """A content tile."""

    default_display_fields = ('title', 'image', 'description')
    sort_limit = 1

    def render(self):
        return self.index()

    @property
    def content(self):
        if self.data.get('use_query') in ('True', True, 'true'):
            catalog = self.catalog
            items = catalog(**self.query)
            if len(items) > 0:
                return items[0].getObject()
        else:
            return get_object(self.data['content'][0])

    @property
    def query(self):
        parsed = parse_query_from_data(self.data, self.context)
        if self.sort_limit:
            parsed['sort_limit'] = self.sort_limit
        return parsed


@implementer(IPersistentTile)
class BaseSliderTile(ContentTile):
    """An base slider tile."""

    sort_limit = 0

    @property
    @view.memoize
    def image_sizes(self):
        values = []
        allowed_sizes = api.portal.get_registry_record(
            name='plone.allowed_sizes',
        )
        for allowed_size in allowed_sizes:
            name = allowed_size.split()[0]
            values.append(name)
        return values

    def get_image_data_from_brain(self, brain):
        base_url = brain.getURL()
        data = {
            'original': base_url,
            'title': brain.Title,
            'description': brain.Description or '',
            'link': '{0}/view'.format(base_url)
        }
        for value in self.image_sizes:
            data[value] = '{0}/@@images/image/{1}'.format(
                base_url,
                value,
            )
        return data

    def get_image_data(self, im):
        base_url = im.absolute_url()
        related = self.get_related(im) or im
        data = {
            'original': base_url,
            'title': im.Title(),
            'description': im.Description() or '',
            'link': '{0}/view'.format(related.absolute_url())
        }
        for value in self.image_sizes:
            data[value] = '{0}/@@images/image/{1}'.format(
                base_url,
                value,
            )
        return data

    def get_images_in_folder(self, brain):
        if brain.portal_type == 'Folder':
            # get contents
            folder = brain.getObject()
            images = folder.getFolderContents()
            results = []
            for image in images:
                if image.portal_type == 'Image':
                    results.append(self.get_image_data_from_brain(image))
                else:
                    obj = image.getObject()
                    if (
                        getattr(obj, 'image', None) and
                        getattr(obj.image, 'contentType', None)
                    ):
                        results.append(self.get_image_data(obj))
            return results
        else:
            return [self.get_image_data_from_brain(brain)]

    @property
    def images(self):
        if self.data.get('use_query') in ('True', True, 'true'):
            return self.query_images()
        else:
            return self.get_selected_images()

    def query_images(self):
        catalog = self.catalog
        results = []
        query = self.query
        query['hasImage'] = True
        for brain in catalog(**query):
            results.append(self.get_image_data_from_brain(brain))
        return results

    def get_selected_images(self):
        results = []
        catalog = self.catalog
        brains = list(catalog(UID=self.data.get('images', [])))
        # we need to order this since catalog results are not ordered
        for uid in self.data.get('images') or []:
            found = False
            for brain in brains:
                if brain.UID == uid:
                    found = brain
                    break
            if not found:
                continue
            brains.remove(found)
            if found.is_folderish:
                results.extend(self.get_images_in_folder(brain))
            else:
                results.append(self.get_image_data_from_brain(found))
        return results

    def get_related(self, obj):
        try:
            return obj.relatedItems[0]
        except Exception:
            return None
