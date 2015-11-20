"""
Models providing Programs support for the LMS and Studio.
"""
from collections import namedtuple
from urlparse import urljoin

from django.db import models
from django.utils.translation import ugettext_lazy as _

from config_models.models import ConfigurationModel


AuthoringAppConfig = namedtuple('AuthoringAppConfig', ['js_url', 'css_url'])


class ProgramsApiConfig(ConfigurationModel):
    """
    Manages configuration for connecting to the Programs service and using its
    API.
    """
    OAUTH2_CLIENT_NAME = 'programs'

    api_version_number = models.IntegerField(verbose_name=_("API Version"))

    internal_service_url = models.URLField(verbose_name=_("Internal Service URL"))
    public_service_url = models.URLField(verbose_name=_("Public Service URL"))

    authoring_app_js_path = models.CharField(
        verbose_name=_("Path to authoring app's JS"),
        max_length=255,
        blank=True,
        null=True
    )
    authoring_app_css_path = models.CharField(
        verbose_name=_("Path to authoring app's CSS"),
        max_length=255,
        blank=True,
        null=True
    )

    enable_student_dashboard = models.BooleanField(
        verbose_name=_("Enable Student Dashboard Displays"),
        default=False
    )
    enable_studio_tab = models.BooleanField(
        verbose_name=_("Enable Studio Authoring Interface"),
        default=False
    )

    @property
    def internal_api_url(self):
        """
        Generate a URL based on internal service URL and API version number.
        """
        return urljoin(self.internal_service_url, '/api/v{}/'.format(self.api_version_number))

    @property
    def public_api_url(self):
        """
        Generate a URL based on public service URL and API version number.
        """
        return urljoin(self.public_service_url, '/api/v{}/'.format(self.api_version_number))

    @property
    def is_student_dashboard_enabled(self):
        """
        Indicates whether LMS dashboard functionality related to Programs should
        be enabled or not.
        """
        return self.enabled and self.enable_student_dashboard

    @property
    def authoring_app_config(self):
        """
        Returns a named tuple containing information required for working with the Programs
        authoring app, a Backbone app hosted by the Programs service.
        """
        js_url = urljoin(self.public_service_url, self.authoring_app_js_path)
        css_url = urljoin(self.public_service_url, self.authoring_app_css_path)

        return AuthoringAppConfig(js_url=js_url, css_url=css_url)

    @property
    def is_studio_tab_enabled(self):
        """
        Indicates whether Studio functionality related to Programs should
        be enabled or not.
        """
        return self.enabled and self.enable_studio_tab and self.authoring_app_js_path and self.authoring_app_css_path
