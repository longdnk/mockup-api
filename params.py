import argparse


def params():
    parser = argparse.ArgumentParser(description="Process some integers.")
    # Host
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host ip")
    # Port
    parser.add_argument("--port", type=int, default=9999, help="Api port number")
    # Reload
    parser.add_argument(
        "--reload", type=bool, default=False, help="Allow reload onchange"
    )
    # Worker
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes. Not work if --reload is turned on, warning !!!",
    )
    # Log level
    parser.add_argument(
        "--log_level",
        type=str,
        default="info",
        help="Set the log level. Options: 'critical', 'error', 'warning', 'info', 'debug', 'trace'. Default: 'info'",
    )
    # Limit rate
    parser.add_argument(
        "--limit_max_requests", type=int, default=1000, help="Max limit request"
    )
    # Number of connection
    parser.add_argument(
        "--limit_concurrency", type=int, default=100, help="Number of connection item"
    )
    # Backlog
    parser.add_argument(
        "--backlog",
        type=int,
        default=2048,
        help="Maximum number of connections to hold in backlog. Relevant for heavy incoming traffic.",
    )
    # SSL key file
    parser.add_argument(
        "--ssl_keyfile",
        type=str,
        default="",
        help="SSL key file config",
    )
    # SSL cert file
    parser.add_argument(
        "--ssl_certfile",
        type=str,
        default="",
        help="SSL cert file config",
    )
    return parser.parse_args()


param_compile = params()
