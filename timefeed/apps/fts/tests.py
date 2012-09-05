"""
Functional tests.

"""

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class AdminSiteTest(LiveServerTestCase):
    """
    Contains tests for the admin app ensuring it has been setup correctly.

    """
    TEST_ADMIN_USER = 'admin'
    TEST_ADMIN_PASS = 'password'
    TEST_ADMIN_EMAIL = 'admin@timefeed.com'

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        user = User.objects.create_superuser(
                self.TEST_ADMIN_USER, 
                self.TEST_ADMIN_EMAIL, 
                self.TEST_ADMIN_PASS
                )
        user.save()

    def tearDown(self):
        self.browser.quit()

    def test_can_access_admin_and_login(self):
        """
        Checks if we can access and login to the admin app. 
        """
        login_page_title            = 'Django administration'
        login_success_page_title    = 'Site administration'
        admin_site_address          = reverse('admin:index')

        # Open the browser and check we are on the login screen.
        self.browser.get(self.live_server_url + admin_site_address) 

        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(login_page_title, body.text)

        # Enter the password and hit return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys(self.TEST_ADMIN_USER)

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys(self.TEST_ADMIN_PASS)
        password_field.send_keys(Keys.RETURN)

        # Ensure that we successfully logged in
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn(login_success_page_title, body.text)
        
    
        
    

