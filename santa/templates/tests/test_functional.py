from santa.templates.tests.base import FUNCTIONAL_TESTING
from hexagonit.testing.browser import Browser
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.testing import layered
from zope.testing import renormalizing
from DateTime import DateTime

import doctest
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import transaction
import unittest2 as unittest

FLAGS = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS  # | doctest.REPORT_NDIFF | doctest.REPORT_ONLY_FIRST_FAILURE

CHECKER = renormalizing.RENormalizing([
    # Normalize the generated UUID values to always compare equal.
    (re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'), '<UUID>'),
])


def setUp(self):
    layer = self.globs['layer']
    # Update global variables within the tests.
    self.globs.update({
        'portal': layer['portal'],
        'portal_url': layer['portal'].absolute_url(),
        'browser': Browser(layer['app']),
    })

    portal = self.globs['portal']
    browser = self.globs['browser']
    portal_url = self.globs['portal_url']
    browser.setBaseUrl(portal_url)

    browser.handleErrors = True
    portal.error_log._ignored_exceptions = ()

    setRoles(portal, TEST_USER_ID, ['Manager'])

    ## Set title and description of foundation
    foundation = portal[
        portal.invokeFactory(
            'Folder',
            'foundation',
            language='',
        )
    ]
    foundation.setLayout('santa-view')
    foundation.reindexObject()
    en = foundation[
        foundation.invokeFactory(
            'Document',
            'en',
            title='Santa Claus Foundation',
            description='Save the world for kids',
            text='<p>Text of SCF.</p>',
        )
    ]
    en.reindexObject()

    # Create Inquiries Folder.
    inquiries = portal[
        portal.invokeFactory(
            'Folder',
            'inquiries',
            title='Inquiries',
            description='Description of Inquiries.',
            language='',
        )
    ]
    inquiries.setLayout('santa-view')
    inquiries.reindexObject()

    en = inquiries[
        inquiries.invokeFactory(
            'Document',
            'en',
            title='English Inquiries',
            description='Description of English Inquiries.',
            text='<p>Text of English Inquiries.</p>',
        )
    ]
    en.reindexObject()

    # Add two forms which link comes to top page.
    form01 = inquiries[
        inquiries.invokeFactory(
            'FormFolder',
            'form01',
            title='Form01',
            description='Description of Form01.',
        )
    ]
    form01.reindexObject()

    form02 = inquiries[
        inquiries.invokeFactory(
            'FormFolder',
            'form02',
            title='Form02',
            description='Description of Form02.',
        )
    ]
    form02.reindexObject()

    # Add News folder and two News Items.
    news = portal[
        portal.invokeFactory(
            'Folder',
            'news',
            title="News",
            language='',
        )
    ]
    news.setLayout('santa-view')
    news.reindexObject()
    news01 = news[
        news.invokeFactory(
            'News Item',
            'news01',
            title="News01",
            description="Description of News01."
        )
    ]
    news01.reindexObject()
    news02 = news[
        news.invokeFactory(
            'News Item',
            'news02',
            title="News02",
            description="Description of News02."
        )
    ]
    news02.reindexObject()

    # Add Events folder and two Events.
    events = portal[
        portal.invokeFactory(
            'Folder',
            'events',
            title="Events",
            language='',
        )
    ]
    events.setLayout('santa-view')
    events.reindexObject()
    now = DateTime()
    event01 = events[
        events.invokeFactory(
            'Event',
            'event01',
            title="Event01",
            description="Description of Event01.",
            startDate=now - 3,
            endDate=now - 2,
        )
    ]
    event01.reindexObject()
    event02 = events[
        events.invokeFactory(
            'Event',
            'event02',
            title="Event02",
            description="Description of Event02.",
            startDate=now - 1,
            endDate=now,
        )
    ]
    event02.reindexObject()
    event03 = events[
        events.invokeFactory(
            'Event',
            'event03',
            title="Event03",
            description="Description of Event03.",
            startDate=now + 1,
            endDate=now + 2,
        )
    ]
    event03.reindexObject()
    event04 = events[
        events.invokeFactory(
            'Event',
            'event04',
            title="Event04",
            description="Description of Event04.",
            startDate=now + 3,
            endDate=now + 4,
        )
    ]
    event04.reindexObject()

    # Add Partners folder and two partners.
    partners = portal[
        portal.invokeFactory(
            'Folder',
            'partners',
            title="Partners",
            language='',
        )
    ]
    partners.setLayout('santa-view')
    partners.reindexObject()
    partner01 = partners[
        partners.invokeFactory(
            'santa.Partner',
            'partner01',
            title="Partner01",
            description="Description of Partner01.",
            address='Street Address of Partner01',
            post_code='010101',
            country='fi',
            email=['partner01@partner01.com'],
            year='2011',
        )
    ]
    partner01.reindexObject()
    partner02 = partners[
        partners.invokeFactory(
            'santa.Partner',
            'partner02',
            title="Partner02",
            description="Description of Partner02.",
            address='Street Address of Partner02',
            post_code='020202',
            country='ja',
            email=['partner02@partner02.com'],
            year='2012',
        )
    ]
    partner02.reindexObject()

    # Add Cases Folder and Images under partner01.
    cases = portal[
        portal.invokeFactory(
            'Folder',
            'cases',
            title="Cases",
            language='',
        )
    ]
    cases.setLayout('santa-view')
    cases.reindexObject()

    image01 = partner01[
        partner01.invokeFactory(
            'Image',
            'image01',
            title="Image01",
            description="Description of Imager01.",
        )
    ]
    image01.reindexObject()
    image02 = partner01[
        partner01.invokeFactory(
            'Image',
            'image02',
            title="Image02",
            description="Description of Imager02.",
        )
    ]
    image02.reindexObject()

    transaction.commit()


def DocFileSuite(testfile, flags=FLAGS, setUp=setUp, layer=FUNCTIONAL_TESTING):
    """Returns a test suite configured with a test layer.

    :param testfile: Path to a doctest file.
    :type testfile: str

    :param flags: Doctest test flags.
    :type flags: int

    :param setUp: Test set up function.
    :type setUp: callable

    :param layer: Test layer
    :type layer: object

    :rtype: `manuel.testing.TestSuite`
    """
    m = manuel.doctest.Manuel(optionflags=flags, checker=CHECKER)
    m += manuel.codeblock.Manuel()

    return layered(
        manuel.testing.TestSuite(m, testfile, setUp=setUp, globs=dict(layer=layer)),
        layer=layer)


def test_suite():

    return unittest.TestSuite([
        DocFileSuite('functional/browser.txt'),
        ])
