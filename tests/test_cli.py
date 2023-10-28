from __future__ import annotations

from argparse import Namespace
from io import StringIO
from contextlib import redirect_stderr
from unittest import mock

from tests import TestCase  # Silence useless deprecation warning.

from brother_ql_web import cli
from brother_ql_web.configuration import Configuration, Font


class LogLevelTypeTestCase(TestCase):
    def test_valid(self) -> None:
        self.assertEqual(40, cli.log_level_type("ERROR"))
        self.assertEqual(40, cli.log_level_type("error"))

    def test_invalid(self) -> None:
        with self.assertRaisesRegex(
            AttributeError, "^module 'logging' has no attribute 'XYZ'$"
        ):
            cli.log_level_type("xyz")


class GetParametersTestCase(TestCase):
    def test_get_parameters(self) -> None:
        with mock.patch(
            "sys.argv",
            [
                "brother_ql_web/__main__.py",
                "--configuration",
                self.example_configuration_path,
                "--log-level",
                "INFO",
                "/dev/printer1",
            ],
        ):
            parameters = cli.get_parameters()

        self.assertEqual(
            Namespace(
                port=False,
                log_level=20,
                font_folder=False,
                default_label_size=False,
                default_orientation=False,
                model=False,
                printer="/dev/printer1",
                configuration=self.example_configuration_path,
            ),
            parameters,
        )


class ChooseDefaultFontTestCase(TestCase):
    FONTS = {
        "family1": {
            "Regular": "family1/regular.otf",
            "Italic": "family1/italic.otf",
        },
        "family2": {
            "Regular": "family2/regular.ttf",
            "Bold": "family2/bold.ttf",
        },
        "family 3": {"Italic": "family3/italic.otf"},
    }

    def assert_is_valid_font(self, font: Font | None) -> None:
        self.assertIsNotNone(font)
        self.assertIn(font.family, self.FONTS)  # type: ignore[union-attr]
        self.assertIn(font.style, self.FONTS[font.family])  # type: ignore[union-attr]

    def test_invalid_only(self) -> None:
        configuration = self.example_configuration
        invalid_font = Font(family="invalid", style="Regular")
        configuration.label.default_fonts = [invalid_font]

        stderr = StringIO()
        with redirect_stderr(stderr):
            self.assertIsNone(configuration.label.default_font)
            cli._choose_default_font(fonts=self.FONTS, configuration=configuration)
            self.assertIsNotNone(configuration.label.default_font)
            font = configuration.label.default_font
            self.assertNotEqual(invalid_font, font)
            self.assert_is_valid_font(font)

        self.assertEqual(
            (
                "Could not find any of the default fonts. Choosing a random one.\n"
                f"The default font is now set to: {font}\n"
            ),
            stderr.getvalue(),
        )

    def test_no_font_given(self) -> None:
        configuration = self.example_configuration
        configuration.label.default_fonts = []

        # Retrieving only two fonts proved to be rather unstable, as we would often
        # choose the same font both times, thus the test would not be representative.
        # By doing ten iterations and assuring that at least three different fonts have
        # been retrieved, we test the same, but in a more stable fashion. Evaluations
        # have shown the we usually get 3-5 different fonts out of ten samples.
        stderr = StringIO()
        fonts = []
        with redirect_stderr(stderr):
            self.assertIsNone(configuration.label.default_font)

            for _ in range(10):
                cli._choose_default_font(fonts=self.FONTS, configuration=configuration)
                self.assertIsNotNone(configuration.label.default_font)
                font = configuration.label.default_font
                self.assert_is_valid_font(font)
                fonts.append(font)

        self.assertGreaterEqual(len(set(fonts)), 3, fonts)

        self.assertEqual(
            "".join(
                (
                    "Could not find any of the default fonts. Choosing a random one.\n"
                    f"The default font is now set to: {font}\n"
                )
                for font in fonts
            ),
            stderr.getvalue(),
        )

    def test_first_valid_font_chosen(self) -> None:
        configuration = self.example_configuration
        configuration.label.default_fonts = [
            Font(family="invalid", style="Regular"),
            Font(family="family2", style="Bold"),
            Font(family="family1", style="Regular"),
        ]

        stderr = StringIO()
        with redirect_stderr(stderr):
            self.assertIsNone(configuration.label.default_font)
            cli._choose_default_font(fonts=self.FONTS, configuration=configuration)
            self.assertIsNotNone(configuration.label.default_font)
            font = configuration.label.default_font
            self.assert_is_valid_font(font)
            self.assertEqual(Font(family="family2", style="Bold"), font)

        self.assertEqual("", stderr.getvalue())


class UpdateConfigurationFromParametersTestCase(TestCase):
    @staticmethod
    def dummy_choose_default_font(
        fonts: dict[str, dict[str, str]], configuration: Configuration
    ) -> Configuration:
        configuration.label.default_font = Font(family="My Family", style="Bold")
        return configuration

    @property
    def expected_configuration(self) -> Configuration:
        configuration = self.example_configuration
        configuration.label.default_font = Font(family="My Family", style="Bold")
        return configuration

    def setUp(self) -> None:
        super().setUp()

        choose_patcher = mock.patch.object(
            cli, "_choose_default_font", side_effect=self.dummy_choose_default_font
        )
        self.choose_mock = choose_patcher.start()
        self.addCleanup(choose_patcher.stop)

    def test_no_overwrites(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=False,
            log_level=False,
            font_folder=False,
            default_label_size=False,
            default_orientation=False,
            model=False,
            printer=False,
            configuration=self.example_configuration_path,
        )

        cli.update_configuration_from_parameters(
            parameters=parameters, configuration=configuration
        )
        self.choose_mock.assert_called_once()

        self.assertEqual(self.expected_configuration, configuration)

    def test_invalid_label_size(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=False,
            log_level=False,
            font_folder=False,
            default_label_size=False,
            default_orientation=False,
            model=False,
            printer=False,
            configuration=self.example_configuration_path,
        )
        configuration.label.default_size = "dummy"

        # Do not assert the label sizes, but make sure that the value list starts with
        # a number.
        with self.assertRaisesRegex(
            cli.InvalidLabelSize,
            r"^Invalid default label size\. Please choose one of the following:\n\d.+$",  # noqa: E501
        ):
            cli.update_configuration_from_parameters(
                parameters=parameters, configuration=configuration
            )

    def test_no_fonts_found(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=False,
            log_level=False,
            font_folder=False,
            default_label_size=False,
            default_orientation=False,
            model=False,
            printer=False,
            configuration=self.example_configuration_path,
        )

        with mock.patch.object(cli, "collect_fonts", return_value=[]) as collect_mock:
            with self.assertRaisesRegex(
                cli.NoFontFound,
                '^Not a single font was found on your system. Please install some or use the "--font-folder" argument.$',  # noqa: E501
            ):
                cli.update_configuration_from_parameters(
                    parameters=parameters, configuration=configuration
                )
        collect_mock.assert_called_once_with(configuration)

    def test_overwrite_port(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=1337,
            log_level=False,
            font_folder=False,
            default_label_size=False,
            default_orientation=False,
            model=False,
            printer=False,
            configuration=self.example_configuration_path,
        )

        cli.update_configuration_from_parameters(
            parameters=parameters, configuration=configuration
        )
        self.choose_mock.assert_called_once()

        expected_configuration = self.expected_configuration
        expected_configuration.server.port = 1337
        self.assertEqual(expected_configuration, configuration)

    def test_overwrite_log_level(self) -> None:
        for log_level in [20, "INFO"]:
            with self.subTest(log_level=log_level):
                self.choose_mock.reset_mock()

                configuration = self.example_configuration
                parameters = Namespace(
                    port=False,
                    log_level=log_level,
                    font_folder=False,
                    default_label_size=False,
                    default_orientation=False,
                    model=False,
                    printer=False,
                    configuration=self.example_configuration_path,
                )

                cli.update_configuration_from_parameters(
                    parameters=parameters, configuration=configuration
                )
                self.choose_mock.assert_called_once()

                expected_configuration = self.expected_configuration
                expected_configuration.server.log_level = "INFO"
                self.assertEqual(expected_configuration, configuration)

    def test_overwrite_font_folder(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=False,
            log_level=False,
            font_folder="/path/to/fonts",
            default_label_size=False,
            default_orientation=False,
            model=False,
            printer=False,
            configuration=self.example_configuration_path,
        )

        dummy_fonts = {"DejaVu Serif": {"Book": "dummy"}}
        with mock.patch(
            "brother_ql_web.utils.get_fonts", return_value=dummy_fonts
        ) as fonts_mock:
            cli.update_configuration_from_parameters(
                parameters=parameters, configuration=configuration
            )
        self.choose_mock.assert_called_once()
        fonts_mock.assert_has_calls(
            [mock.call(), mock.call("/path/to/fonts")],
            any_order=False,
        )
        self.assertEqual(2, fonts_mock.call_count, fonts_mock.call_args_list)

        expected_configuration = self.expected_configuration
        expected_configuration.server.additional_font_folder = "/path/to/fonts"
        self.assertEqual(expected_configuration, configuration)

    def test_overwrite_printer(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=False,
            log_level=False,
            font_folder=False,
            default_label_size=False,
            default_orientation=False,
            model=False,
            printer="/dev/printer42",
            configuration=self.example_configuration_path,
        )

        cli.update_configuration_from_parameters(
            parameters=parameters, configuration=configuration
        )
        self.choose_mock.assert_called_once()

        expected_configuration = self.expected_configuration
        expected_configuration.printer.printer = "/dev/printer42"
        self.assertEqual(expected_configuration, configuration)

    def test_overwrite_model(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=False,
            log_level=False,
            font_folder=False,
            default_label_size=False,
            default_orientation=False,
            model="QL-800",
            printer=False,
            configuration=self.example_configuration_path,
        )

        cli.update_configuration_from_parameters(
            parameters=parameters, configuration=configuration
        )
        self.choose_mock.assert_called_once()

        expected_configuration = self.expected_configuration
        expected_configuration.printer.model = "QL-800"
        self.assertEqual(expected_configuration, configuration)

    def test_overwrite_default_label_size(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=False,
            log_level=False,
            font_folder=False,
            default_label_size="38",
            default_orientation=False,
            model=False,
            printer=False,
            configuration=self.example_configuration_path,
        )

        cli.update_configuration_from_parameters(
            parameters=parameters, configuration=configuration
        )
        self.choose_mock.assert_called_once()

        expected_configuration = self.expected_configuration
        expected_configuration.label.default_size = "38"
        self.assertEqual(expected_configuration, configuration)

    def test_overwrite_default_orientation(self) -> None:
        configuration = self.example_configuration
        parameters = Namespace(
            port=False,
            log_level=False,
            font_folder=False,
            default_label_size=False,
            default_orientation="my_orientation",
            model=False,
            printer=False,
            configuration=self.example_configuration_path,
        )

        cli.update_configuration_from_parameters(
            parameters=parameters, configuration=configuration
        )
        self.choose_mock.assert_called_once()

        expected_configuration = self.expected_configuration
        expected_configuration.label.default_orientation = "my_orientation"
        self.assertEqual(expected_configuration, configuration)
