from tests import TestCase  # Silence useless deprecation warning.

from brother_ql_web import cli


class LogLevelTypeTestCase(TestCase):
    def test_valid(self):
        self.assertEqual(40, cli.log_level_type("ERROR"))
        self.assertEqual(40, cli.log_level_type("error"))

    def test_invalid(self):
        with self.assertRaisesRegex(
            AttributeError, "^module 'logging' has no attribute 'XYZ'$"
        ):
            cli.log_level_type("xyz")


class GetParametersTestCase(TestCase):
    pass


class ChooseDefaultFontTestCase(TestCase):
    pass


class UpdateConfigurationFromParametersTestCase(TestCase):
    pass
