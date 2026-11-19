"""Behavioral checks for Kevoro's static page, with synthetic input only.

Run through the repo's webapp-testing with_server.py helper. Browser startup
failures are errors, never skips or a reason to disable the Chromium sandbox.
"""
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import unittest
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import expect, sync_playwright

from browser_support import is_local_origin, local_only_route


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = os.environ.get('KEVORO_TEST_URL', 'http://127.0.0.1:8765')
RESULTS = Path(os.environ.get('KEVORO_TEST_RESULTS', str(ROOT / 'test-results')))
PRODUCTS = {'basilia': 'Basilia Connect', 'gestion': 'Gestión', 'medida': 'A la medida'}
HEADING = 'Menos vueltas. Más negocio.'


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.nodes = []
        self.headings = []
        self.in_h1 = False
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        self.nodes.append((tag, dict(attrs)))
        if tag == 'br' and self.in_h1:
            self.headings[-1] += ' '
        if tag == 'h1':
            self.headings.append('')
            self.in_h1 = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_h1 = False

    def handle_data(self, data):
        if self.in_h1:
            self.headings[-1] += data


class DocumentContractTests(unittest.TestCase):
    """These run before a browser is available and record the feature's RED state."""
    def setUp(self):
        self.document = Document((ROOT / 'index.html').read_text(encoding='utf-8'))

    def test_public_message_and_landmarks_exist(self):
        self.assertEqual([' '.join(h.split()) for h in self.document.headings], [HEADING])
        tags = [tag for tag, _ in self.document.nodes]
        for tag in ('header', 'main', 'footer', 'nav'):
            self.assertIn(tag, tags)

    def test_interaction_contract_exists(self):
        ids = {attrs['id'] for _, attrs in self.document.nodes if 'id' in attrs}
        self.assertTrue({'menu-toggle', 'site-nav', 'basilia', 'gestion', 'medida',
                         'contacto', 'contact-form', 'producto', 'email-draft',
                         'draft-ready', 'whatsapp-dialog'} <= ids,
                        'Missing a required navigation, product or contact control')

    def test_images_have_alt_and_assets_are_local(self):
        for tag, attrs in self.document.nodes:
            if tag == 'img':
                self.assertIn('alt', attrs)
            if tag in ('script', 'img', 'source'):
                src = attrs.get('src', '')
                self.assertFalse(src.startswith(('https:', 'http:', '//')), src)
            if tag == 'link' and attrs.get('rel') in ('stylesheet', 'preload'):
                self.assertFalse(attrs.get('href', '').startswith(('https:', 'http:', '//')))


class BrowserSessionMixin:
    viewport = None

    @classmethod
    def setUpClass(cls):
        if not is_local_origin(BASE_URL, BASE_URL):
            raise ValueError('KEVORO_TEST_URL must be an HTTP localhost/127.0.0.1 origin')
        RESULTS.mkdir(parents=True, exist_ok=True)
        cls.playwright = sync_playwright().start()
        cls.addClassCleanup(cls.playwright.stop)
        cls.browser = cls.playwright.chromium.launch(headless=True, chromium_sandbox=True)
        cls.addClassCleanup(cls.browser.close)

    def setUp(self):
        self.blocked = []
        self.console_errors = []
        self.page_errors = []
        self.requests = []
        self.context = self.browser.new_context(
            viewport=self.viewport, locale='es-CO', service_workers='block',
            reduced_motion='reduce', is_mobile=self.viewport['width'] < 600,
            has_touch=self.viewport['width'] < 600,
        )
        self.addCleanup(self.context.close)
        self.context.route('**/*', lambda route: local_only_route(route, BASE_URL, self.blocked))
        def block_socket(route):
            self.blocked.append(route.url)
            route.close(code=1008, reason='No sockets in static-page tests')
        self.context.route_web_socket('**/*', block_socket)
        self.context.on('request', lambda request: self.requests.append(request.url))
        self.context.tracing.start(screenshots=True, snapshots=True, sources=False)
        self.page = self.context.new_page()
        self.page.on('pageerror', lambda error: self.page_errors.append(str(error)))
        self.page.on('console', lambda message: self.console_errors.append(message.text) if message.type == 'error' else None)
        self.addCleanup(self.finish_evidence)

    def record_evidence(self):
        name = self.id().replace('.', '-')
        try:
            if not self.page.is_closed():
                self.page.screenshot(path=str(RESULTS / f'{name}.png'), full_page=True)
            self.context.tracing.stop(path=str(RESULTS / f'{name}.zip'))
        finally:
            (RESULTS / f'{name}.json').write_text(json.dumps({
                'test': self.id(), 'viewport': self.viewport, 'url': BASE_URL,
                'blocked_requests': self.blocked, 'requests': self.requests,
                'console_errors': self.console_errors, 'page_errors': self.page_errors,
            }, ensure_ascii=False, indent=2), encoding='utf-8')

    def finish_evidence(self):
        # Screenshot/trace capture can deliver late browser events. Assert only
        # after capturing them, including when the test itself failed earlier.
        self.record_evidence()
        self.assertEqual(self.page_errors, [], 'Uncaught JavaScript errors')
        self.assertEqual(self.console_errors, [], 'Browser console errors')
        self.assertEqual(self.blocked, [], 'The page tried to use external network resources')

    def assert_no_horizontal_overflow(self):
        sizes = self.page.evaluate('''() => ({viewport: innerWidth,
            document: document.documentElement.scrollWidth, body: document.body.scrollWidth})''')
        self.assertLessEqual(max(sizes['document'], sizes['body']), sizes['viewport'] + 1,
                             f'Horizontal overflow at {self.viewport["width"]}px: {sizes}')


class SiteFlowMixin(BrowserSessionMixin):
    def setUp(self):
        super().setUp()
        self.page.goto(BASE_URL, wait_until='domcontentloaded')
        expect(self.page.get_by_role('heading', level=1)).to_have_text(HEADING, use_inner_text=True)

    def test_layout_and_accessible_structure(self):
        expect(self.page.get_by_role('main')).to_have_count(1)
        expect(self.page.get_by_role('banner')).to_have_count(1)
        expect(self.page.get_by_role('contentinfo')).to_have_count(1)
        expect(self.page.get_by_role('heading', level=1)).to_have_count(1)
        expect(self.page.locator('img:not([alt])')).to_have_count(0)
        self.assert_no_horizontal_overflow()
        self.page.evaluate("() => window.scrollTo({top: 0, left: 0, behavior: 'instant'})")
        self.page.screenshot(path=str(RESULTS / f'web-{self.viewport["width"]}-viewport.png'),
                             full_page=False)
        for product in PRODUCTS:
            expect(self.page.locator(f'article#{product}')).to_be_visible()

    def test_axe_accessibility_on_page_and_open_dialog(self):
        # Local audit dependency only; no remote script or certification claim.
        self.page.add_script_tag(path=str(ROOT / 'node_modules/axe-core/axe.min.js'))
        self.page.evaluate('() => document.fonts.ready.then(() => true)')
        expect(self.page.get_by_role('textbox', name='Tu nombre (opcional)', exact=True)).to_be_visible()
        expect(self.page.get_by_role('combobox', name='¿Qué te interesa?', exact=True)).to_be_visible()
        expect(self.page.get_by_role('textbox', name='Cuéntanos un poco', exact=True)).to_be_visible()
        reports = []
        tags = ['wcag2a', 'wcag2aa', 'wcag21aa', 'wcag22aa']
        try:
            for state in ('page-with-contact-form', 'open-whatsapp-dialog'):
                if state == 'open-whatsapp-dialog':
                    self.page.locator('article#basilia button[data-whatsapp]').click()
                    expect(self.page.get_by_role('dialog', name='Sigamos por correo.', exact=True)).to_be_visible()
                reports.append(self.page.evaluate('''async ({state, tags}) => {
                    const result = await axe.run(document, {
                        runOnly: {type: 'tag', values: tags}
                    });
                    const summarize = entries => entries.map(entry => ({
                        id: entry.id, impact: entry.impact, help: entry.help,
                        nodes: entry.nodes.map(node => ({
                            target: node.target, summary: node.failureSummary || null
                        }))
                    }));
                    return {state, version: axe.version, tags,
                        violations: summarize(result.violations),
                        incomplete: summarize(result.incomplete)};
                }''', {'state': state, 'tags': tags}))
        finally:
            name = self.id().replace('.', '-')
            (RESULTS / f'{name}-axe.json').write_text(json.dumps({
                'test': self.id(), 'viewport': self.viewport, 'reports': reports,
                'scope': 'Automated checks only; incomplete results require manual review.',
            }, ensure_ascii=False, indent=2), encoding='utf-8')
        violations = [{'state': report['state'], 'id': violation['id'],
                       'targets': [node['target'] for node in violation['nodes']]}
                      for report in reports for violation in report['violations']]
        self.assertEqual(violations, [], 'axe accessibility violations: ' + json.dumps(violations, ensure_ascii=False))

    def test_navigation_works_at_each_viewport(self):
        nav = self.page.locator('#site-nav')
        toggle = self.page.get_by_role('button', name='Menú', exact=True)
        if self.viewport['width'] < 600:
            expect(toggle).to_be_visible()
            expect(toggle).to_have_attribute('aria-expanded', 'false')
            expect(nav).not_to_be_visible()
            toggle.click()
            expect(toggle).to_have_attribute('aria-expanded', 'true')
            expect(nav).to_be_visible()
        else:
            expect(nav).to_be_visible()
        nav.locator('a[href="#productos"]').click()
        expect(self.page).to_have_url(re.compile(r'#productos$'))
        expect(self.page.locator('#productos')).to_be_visible()

    def test_tabs_have_panels_and_support_keyboard(self):
        tabs = [self.page.get_by_role('tab', name=name, exact=True)
                for name in ('Agenda', 'Gestión', 'A tu medida')]
        for tab in tabs:
            tab.click()
            expect(tab).to_have_attribute('aria-selected', 'true')
            panel_id = tab.get_attribute('aria-controls')
            self.assertTrue(panel_id, 'Every tab must identify its panel')
            panel = self.page.locator(f'#{panel_id}')
            expect(panel).to_have_attribute('role', 'tabpanel')
            expect(panel).to_be_visible()
            tab_id = tab.get_attribute('id')
            self.assertTrue(tab_id, 'The tab needs an ID so its panel has an accessible label')
            self.assertEqual(panel.get_attribute('aria-labelledby'), tab_id)
            expect(self.page.get_by_role('tab', selected=True)).to_have_count(1)
        tabs[0].focus()
        tabs[0].press('ArrowRight')
        expect(tabs[1]).to_be_focused()
        tabs[1].press('Enter')
        expect(tabs[1]).to_have_attribute('aria-selected', 'true')

    def test_demo_links_choose_the_product(self):
        for identifier, value in PRODUCTS.items():
            link = self.page.locator(f'article#{identifier} a[data-demo]')
            expect(link).to_have_accessible_name('Solicitar demo')
            expect(link).to_have_attribute('href', '#contacto')
            link.click()
            expect(self.page.locator('#producto')).to_have_value(value)
            expect(self.page).to_have_url(re.compile(r'#contacto$'))

    def test_unconfigured_whatsapp_opens_local_dialog_and_returns_focus(self):
        self.assertEqual(self.page.evaluate('window.KEVORO_CONFIG.whatsappNumber'), '')
        dialog = self.page.locator('dialog#whatsapp-dialog')
        for identifier in PRODUCTS:
            button = self.page.locator(f'article#{identifier} button[data-whatsapp]')
            expect(button).to_have_accessible_name('Escríbenos por WhatsApp')
            button.click()
            expect(dialog).to_be_visible()
            self.page.keyboard.press('Escape')
            expect(dialog).not_to_be_visible()
            expect(button).to_be_focused()
        self.assertEqual(len(self.context.pages), 1, 'No WhatsApp tab may open without a configured number')

    def test_contact_requires_message_and_keeps_optional_name(self):
        form = self.page.locator('#contact-form')
        name = form.locator('input[name="nombre"]')
        message = form.locator('textarea')
        self.assertFalse(name.evaluate('(element) => element.required'))
        self.assertTrue(message.evaluate('(element) => element.required'))
        form.locator('button[type="submit"]').click()
        self.assertFalse(form.evaluate('(element) => element.checkValidity()'))
        expect(self.page.locator('#draft-ready')).not_to_be_visible()
        message.fill('Consulta ficticia: ¿podemos conversar sobre una herramienta para el negocio?')
        form.locator('button[type="submit"]').click()
        expect(self.page.locator('#draft-ready')).to_be_visible()
        expect(self.page.get_by_role('link', name='Abrir mi correo', exact=True)).to_be_visible()

    def test_email_draft_preserves_synthetic_input_and_does_not_send(self):
        form = self.page.locator('#contact-form')
        name = 'Ángela Ficticia & Equipo'
        message = 'Consulta ficticia: café & gestión + agenda?\nSin datos de pacientes. #prueba'
        form.locator('input[name="nombre"]').fill(name)
        form.locator('textarea').fill(message)
        self.page.locator('#producto').select_option('Gestión')
        before = list(self.requests)
        form.locator('button[type="submit"]').click()
        link = self.page.locator('a#email-draft')
        expect(link).to_be_visible()
        expect(link).to_have_accessible_name('Abrir mi correo')
        href = link.get_attribute('href')
        parsed = urlsplit(href)
        self.assertEqual(parsed.scheme, 'mailto')
        self.assertEqual(parsed.path, 'kevoro.company@gmail.com')
        values = parse_qs(parsed.query)
        self.assertIn('subject', values)
        self.assertIn('body', values)
        self.assertIn('Gestión', values['subject'][0] + values['body'][0])
        self.assertIn(name, values['body'][0])
        self.assertIn(message, values['body'][0])
        self.assertIn('%26', href)
        self.assertIn('%2B', href.upper())
        self.assertEqual(self.requests, before, 'Preparing the draft must not submit over HTTP')
        self.assertEqual(len(self.context.pages), 1)
        expect(self.page.locator('#contacto')).to_contain_text(re.compile('pacientes', re.I))

    def test_keyboard_focus_and_reduced_motion(self):
        self.assertTrue(self.page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches"))
        self.page.keyboard.press('Tab')
        first = self.page.locator(':focus')
        expect(first).to_be_visible()
        style = first.evaluate('''element => { const s = getComputedStyle(element);
            return {outlineStyle:s.outlineStyle, outlineWidth:parseFloat(s.outlineWidth),
                    boxShadow:s.boxShadow}; }''')
        self.assertTrue((style['outlineStyle'] != 'none' and style['outlineWidth'] >= 1)
                        or style['boxShadow'] != 'none', 'Keyboard focus needs a visible indicator')
        animations = self.page.evaluate('''() => document.getAnimations().filter(animation =>
            animation.playState === 'running').map(animation => animation.effect.getComputedTiming().duration)''')
        self.assertTrue(all(isinstance(duration, (int, float)) and duration <= 10 for duration in animations),
                        f'Reduced-motion page has long running animations: {animations}')


class DesktopTests(SiteFlowMixin, unittest.TestCase):
    viewport = {'width': 1440, 'height': 1000}


class MobileTests(SiteFlowMixin, unittest.TestCase):
    viewport = {'width': 390, 'height': 844}


class NarrowMobileTests(SiteFlowMixin, unittest.TestCase):
    viewport = {'width': 320, 'height': 740}


class EvidenceLifecycleTests(unittest.TestCase):
    def test_error_delivered_during_capture_cannot_pass(self):
        from types import SimpleNamespace
        late_errors = []
        capture = SimpleNamespace(
            record_evidence=lambda: late_errors.append('synthetic late script error'),
            page_errors=late_errors, console_errors=[], blocked=[],
            assertEqual=self.assertEqual,
        )
        with self.assertRaisesRegex(AssertionError, 'Uncaught JavaScript errors'):
            SiteFlowMixin.finish_evidence(capture)


if __name__ == '__main__':
    unittest.main()
