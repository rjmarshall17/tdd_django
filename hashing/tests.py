from django.test import TestCase
from django.core.exceptions import ValidationError
from .forms import HashForm
from .models import Hash
from selenium import webdriver
import hashlib
import time

LOWERCASE_HELLO_HASH = '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
BAD_LOWERCASE_HELLO_HASH = LOWERCASE_HELLO_HASH + 'ggggggggg'


class FunctionalTestCase(TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def test_there_is_homepage(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('Enter hash here:', self.browser.page_source)

    def test_hash_of_hello(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        text = self.browser.find_element_by_name('submit').click()
        self.assertIn(LOWERCASE_HELLO_HASH,self.browser.page_source)

    def test_hash_ajax(self):
        self.browser.get('http://localhost:8000')
        text = self.browser.find_element_by_id('id_text')
        text.send_keys('hello')
        time.sleep(5)  # Wait for AJAX
        self.assertIn(LOWERCASE_HELLO_HASH, self.browser.page_source)

    def tearDown(self):
        self.browser.quit()


class UnitTestCase(TestCase):
    def test_home_homepage_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'hashing/home.html')

    def test_hash_form(self):
        form = HashForm(data={'text':'hello'})
        self.assertTrue(form.is_valid())

    def test_hash_func_works(self):
        text_hash = hashlib.sha256('hello'.encode('utf-8')).hexdigest()
        self.assertEqual(LOWERCASE_HELLO_HASH, text_hash)

    def saveHash(self):
        hash = Hash()
        hash.text = 'hello'
        hash.hash = LOWERCASE_HELLO_HASH
        hash.save()
        return hash

    def test_hash_object(self):
        hash = self.saveHash()
        pulled_hash = Hash.objects.get(hash=LOWERCASE_HELLO_HASH)
        self.assertEqual(pulled_hash.text, hash.text)

    def test_viewing_hash(self):
        hash = self.saveHash()
        response = self.client.get('/hash/%s' % LOWERCASE_HELLO_HASH)
        self.assertContains(response, 'hello')

    def test_bad_data(self):
        def badHash():
            hash = Hash()
            hash.text = 'junk'
            hash.hash = BAD_LOWERCASE_HELLO_HASH
            hash.full_clean()
        self.assertRaises(ValidationError, badHash)

