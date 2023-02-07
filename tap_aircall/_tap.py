from typing import List, Callable, Tuple
import click

from pathlib import Path

from singer_sdk import Tap
from singer_sdk.helpers._classproperty import classproperty
from singer_sdk.tap_base import CliTestOptionValue
from singer_sdk.cli import common_options

class _Tap(Tap):
    """
    Monkeypatches the Tap.cli to accept -c arg as the same as --config
    If both are provided, --config arg is accepted first
    """
    @classproperty
    def cli(cls) -> Callable:
        """Execute standard CLI handler for taps.

        Returns:
            A callable CLI object.
        """

        @common_options.PLUGIN_VERSION
        @common_options.PLUGIN_ABOUT
        @common_options.PLUGIN_ABOUT_FORMAT
        @common_options.PLUGIN_CONFIG
        @click.option(
            "-c",
            multiple=True,
            help="Configuration file location or 'ENV' to use environment variables.",
            type=click.STRING,
            default=(),
        )
        @click.option(
            "--discover",
            is_flag=True,
            help="Run the tap in discovery mode.",
        )
        @click.option(
            "--test",
            is_flag=False,
            flag_value=CliTestOptionValue.All.value,
            default=CliTestOptionValue.Disabled,
            help=(
                "Use --test to sync a single record for each stream. "
                + "Use --test=schema to test schema output without syncing "
                + "records."
            ),
        )
        @click.option(
            "--catalog",
            help="Use a Singer catalog file with the tap.",
            type=click.Path(),
        )
        @click.option(
            "--state",
            help="Use a bookmarks file for incremental replication.",
            type=click.Path(),
        )
        @click.command(
            help="Execute the Singer tap.",
            context_settings={"help_option_names": ["--help"]},
        )
        def cli(
            version: bool = False,
            about: bool = False,
            discover: bool = False,
            test: CliTestOptionValue = CliTestOptionValue.Disabled,
            config: Tuple[str, ...] = (),
            c: Tuple[str, ...] = (),
            state: str = None,
            catalog: str = None,
            format: str = None,
        ) -> None:
            """Handle command line execution.

            Args:
                version: Display the package version.
                about: Display package metadata and settings.
                discover: Run the tap in discovery mode.
                test: Test connectivity by syncing a single record and exiting.
                format: Specify output style for `--about`.
                config: Configuration file location or 'ENV' to use environment
                    variables. Accepts multiple inputs as a tuple.
                catalog: Use a Singer catalog file with the tap.",
                state: Use a bookmarks file for incremental replication.

            Raises:
                FileNotFoundError: If the config file does not exist.
            """
            if version:
                cls.print_version()
                return

            config_to_use = config or c

            if not about:
                cls.print_version(print_fn=cls.logger.info)
            else:
                cls.print_about(format=format)
                return

            validate_config: bool = True
            if discover:
                # Don't abort on validation failures
                validate_config = False

            parse_env_config = False
            config_files: List[PurePath] = []
            for config_path in config_to_use:
                if config_path == "ENV":
                    # Allow parse from env vars:
                    parse_env_config = True
                    continue

                # Validate config file paths before adding to list
                if not Path(config_path).is_file():
                    raise FileNotFoundError(
                        f"Could not locate config file at '{config_path}'."
                        "Please check that the file exists."
                    )

                config_files.append(Path(config_path))

            tap = cls(  # type: ignore  # Ignore 'type not callable'
                config=config_files or None,
                state=state,
                catalog=catalog,
                parse_env_config=parse_env_config,
                validate_config=validate_config,
            )

            if discover:
                tap.run_discovery()
                if test == CliTestOptionValue.All.value:
                    tap.run_connection_test()
            elif test == CliTestOptionValue.All.value:
                tap.run_connection_test()
            elif test == CliTestOptionValue.Schema.value:
                tap.write_schemas()
            else:
                tap.sync_all()

        return cli
