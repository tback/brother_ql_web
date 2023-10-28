def main() -> None:
    import logging

    from brother_ql_web import cli, utils, web
    from brother_ql_web.configuration import Configuration

    cli_parameters = cli.get_parameters()
    configuration = Configuration.from_json(cli_parameters.configuration)
    cli.update_configuration_from_parameters(
        configuration=configuration, parameters=cli_parameters
    )
    logging.basicConfig(level=configuration.server.log_level)
    web.main(
        configuration=configuration,
        fonts=utils.collect_fonts(configuration),
        label_sizes=utils.get_label_sizes(),
        backend_class=utils.get_backend_class(configuration),
    )


if __name__ == "__main__":
    main()
