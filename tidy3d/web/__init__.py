""" imports interfaces for interacting with server """
from .synchronous.api.container import Job, Batch, BatchData
from .synchronous.cli.migrate import migrate
from .synchronous.cli.app import configure_fn as configure
from .synchronous.api.webapi import (
    run,
    upload,
    get_info,
    start,
    monitor,
    delete,
    download,
    load,
    estimate_cost,
    abort,
    get_tasks,
    delete_old,
    download_log,
    download_json,
    load_simulation,
    real_cost,
    test,
)
from .synchronous.cli import tidy3d_cli
from .synchronous.core import core_config
from ..log import log, get_logging_console
from ..version import __version__

migrate()

core_config.set_config(log, get_logging_console(), __version__)

__all__ = [
    "run",
    "upload",
    "get_info",
    "start",
    "monitor",
    "delete",
    "abort",
    "download",
    "load",
    "estimate_cost",
    "get_tasks",
    "delete_old",
    "download_json",
    "download_log",
    "load_simulation",
    "real_cost",
    "Job",
    "Batch",
    "BatchData",
    "tidy3d_cli",
    "configure",
    "test",
]
