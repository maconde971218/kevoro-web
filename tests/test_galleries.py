"""The review galleries work locally without saving or publishing anything."""
import re
import unittest

from playwright.sync_api import expect

from test_site import BASE_URL, BrowserSessionMixin, HEADING


class GalleryFlowMixin(BrowserSessionMixin):
    def assert_gallery_structure(self):
        expect(self.page.get_by_role('main')).to_have_count(1)
        expect(self.page.get_by_role('heading', level=1)).to_have_count(1)
        expect(self.page.get_by_role('banner')).to_have_count(1)
        expect(self.page.get_by_role('contentinfo')).to_have_count(1)
        expect(self.page.locator('img:not([alt])')).to_have_count(0)
        self.assert_no_horizontal_overflow()

    def load_images(self):
        # Trigger lazy images and verify actual decoding before recording a page.
        for image in self.page.locator('img').all():
            image.scroll_into_view_if_needed()
            expect(image).to_have_js_property('complete', True)
            self.assertGreater(image.evaluate('(element) => element.naturalWidth'), 0)
        self.page.evaluate('scrollTo(0, 0)')

    def test_brand_choices_are_temporary_and_do_not_publish(self):
        self.page.goto(BASE_URL + '/marca/', wait_until='domcontentloaded')
        expect(self.page.get_by_role('heading', level=1)).to_have_text(
            'Tres maneras de ser Kevoro.', use_inner_text=True)
        self.assert_gallery_structure()
        expect(self.page.locator('article.direction')).to_have_count(3)
        choices = self.page.locator('button[data-choice]')
        for name in ('Pulso', 'Claro', 'Cercano'):
            button = self.page.get_by_role('button', name='Me interesa ' + name, exact=True)
            button.click()
            expect(button).to_have_attribute('aria-pressed', 'true')
            expect(self.page.locator('button[data-choice][aria-pressed="true"]')).to_have_count(1)
            expect(self.page.get_by_role('status')).to_contain_text(name)
            expect(self.page.get_by_role('status')).to_contain_text('No se ha guardado, enviado ni aprobado')
        self.assertEqual(self.page.evaluate('localStorage.length + sessionStorage.length'), 0)
        self.page.reload(wait_until='domcontentloaded')
        for button in choices.all():
            expect(button).to_have_attribute('aria-pressed', 'false')
        self.load_images()
        self.assert_gallery_structure()

    def test_instagram_filters_details_and_local_artwork(self):
        self.page.goto(BASE_URL + '/instagram/', wait_until='domcontentloaded')
        expect(self.page.locator('#load-status')).to_contain_text('Contenido local cargado')
        expect(self.page.get_by_role('heading', level=1)).to_have_text('La primera conversación.')
        self.assert_gallery_structure()
        for name, panel_id, content, count in (
            ('9 posts', 'panel-posts', '#posts-grid article.post', 9),
            ('6 Reels', 'panel-reels', '#reel-grid article.reel', 6),
            ('Stories', 'panel-stories', '#story-grid article.story', 9),
            ('30 días', 'panel-calendario', '#calendar-list article.day', 30),
        ):
            button = self.page.get_by_role('button', name=name, exact=True)
            button.focus()
            button.press('Enter')
            expect(button).to_have_attribute('aria-pressed', 'true')
            expect(button).to_have_attribute('aria-controls', panel_id)
            expect(self.page.locator('.filters button[aria-pressed="true"]')).to_have_count(1)
            panel = self.page.locator('#' + panel_id)
            expect(panel).to_be_visible()
            expect(self.page.locator('.panel:not([hidden])')).to_have_count(1)
            expect(self.page.locator(content)).to_have_count(count)
            if panel_id in ('panel-posts', 'panel-reels'):
                details = panel.locator('details').first
                details.locator('summary').click()
                expect(details).to_have_attribute('open', '')
                expect(details.locator('.detail-body')).to_be_visible()
            self.assert_no_horizontal_overflow()
        self.page.get_by_role('button', name='9 posts', exact=True).click()
        for artwork in self.page.locator('#posts-grid [role="img"]').all():
            expect(artwork).to_have_accessible_name(re.compile(r'.+'))
        self.load_images()
        self.assert_gallery_structure()
        expect(self.page.locator('body')).to_contain_text('No hay una cuenta conectada')
        expect(self.page.locator('#revision')).to_contain_text('no publica ni conecta cuentas')

    def test_gallery_links_and_keyboard_skip_return_to_local_page(self):
        self.page.goto(BASE_URL + '/instagram/', wait_until='domcontentloaded')
        expect(self.page.locator('#load-status')).to_contain_text('Contenido local cargado')
        self.page.keyboard.press('Tab')
        skip = self.page.get_by_role('link', name='Saltar al contenido', exact=True)
        expect(skip).to_be_focused()
        expect(skip).to_be_visible()
        self.assertTrue(self.page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches"))
        self.page.get_by_role('navigation').get_by_role('link', name='Marca', exact=True).click()
        expect(self.page).to_have_url(BASE_URL + '/marca/')
        self.page.get_by_role('link', name='Ver propuesta web', exact=True).click()
        expect(self.page.get_by_role('heading', level=1)).to_have_text(HEADING, use_inner_text=True)
        self.assert_no_horizontal_overflow()


class GalleryDesktopTests(GalleryFlowMixin, unittest.TestCase):
    viewport = {'width': 1440, 'height': 1000}


class GalleryMobileTests(GalleryFlowMixin, unittest.TestCase):
    viewport = {'width': 390, 'height': 844}


class GalleryNarrowMobileTests(GalleryFlowMixin, unittest.TestCase):
    viewport = {'width': 320, 'height': 740}


if __name__ == '__main__':
    unittest.main()
