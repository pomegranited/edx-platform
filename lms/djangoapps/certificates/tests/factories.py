# Factories are self documenting
# pylint: disable=missing-docstring
from factory.django import DjangoModelFactory

from certificates.models import (
    GeneratedCertificate, CertificateStatuses, CertificateHtmlViewConfiguration, CertificateWhitelist,
)
from student.models import LinkedInAddToProfileConfiguration


class GeneratedCertificateFactory(DjangoModelFactory):

    class Meta(object):
        model = GeneratedCertificate

    course_id = None
    status = CertificateStatuses.unavailable
    mode = GeneratedCertificate.MODES.honor
    name = ''


class CertificateWhitelistFactory(DjangoModelFactory):

    class Meta(object):
        model = CertificateWhitelist

    course_id = None
    whitelist = True
    notes = None


class CertificateHtmlViewConfigurationFactory(DjangoModelFactory):

    class Meta(object):
        model = CertificateHtmlViewConfiguration

    enabled = True
    configuration = """{
            "default": {
                "accomplishment_class_append": "accomplishment-certificate",
                "platform_name": "edX",
                "company_about_url": "http://www.edx.org/about-us",
                "company_privacy_url": "http://www.edx.org/edx-privacy-policy",
                "company_tos_url": "http://www.edx.org/edx-terms-service",
                "company_verified_certificate_url": "http://www.edx.org/verified-certificate",
                "document_stylesheet_url_application": "/static/certificates/sass/main-ltr.css",
                "logo_src": "/static/certificates/images/logo-edx.png",
                "logo_url": "http://www.edx.org"
            },
            "honor": {
                "certificate_type": "Honor Code",
                "certificate_title": "Certificate of Achievement",
                "logo_url": "http://www.edx.org/honor_logo.png"
            },
            "verified": {
                "certificate_type": "Verified",
                "certificate_title": "Verified Certificate of Achievement"
            },
            "xseries": {
                "certificate_title": "XSeries Certificate of Achievement",
                "certificate_type": "XSeries"
            },
            "microsites": {
                "testmicrosite": {
                    "company_about_url": "http://www.testmicrosite.org/about-us",
                    "company_privacy_url": "http://www.testmicrosite.org/edx-privacy-policy",
                    "company_tos_url": "http://www.testmicrosite.org/edx-terms-service"
                }
            }
        }"""


class LinkedInAddToProfileConfigurationFactory(DjangoModelFactory):

    class Meta(object):
        model = LinkedInAddToProfileConfiguration

    enabled = True
    company_identifier = "0_0dPSPyS070e0HsE9HNz_13_d11_"
    trk_partner_name = 'unittest'
