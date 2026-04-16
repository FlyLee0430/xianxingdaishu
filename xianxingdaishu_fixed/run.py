#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""线性代数 MCP 服务启动脚本。"""

from __future__ import annotations

import argparse
import logging
import sys

from src.server import mcp

logger = logging.getLogger("LinearAlgebraMCP")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="线性代数 MCP 服务启动器")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http", "http", "sse"],
        default="stdio",
        help="传输方式，默认 stdio",
    )
    parser.add_argument(
        "--http",
        action="store_true",
        help="兼容旧参数。等价于 --transport streamable-http",
    )
    parser.add_argument("--host", default="127.0.0.1", help="HTTP 监听地址，默认 127.0.0.1")
    parser.add_argument("--port", type=int, default=8000, help="HTTP 监听端口，默认 8000")
    parser.add_argument("--path", default="/mcp", help="MCP HTTP 路径，默认 /mcp")
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="日志级别",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    transport = "streamable-http" if args.http else args.transport

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    logger.info("starting transport=%s", transport)

    try:
        if transport == "stdio":
            mcp.run(transport="stdio", show_banner=False)
        else:
            mcp.run(
                transport=transport,
                host=args.host,
                port=args.port,
                path=args.path,
                show_banner=False,
            )
    except KeyboardInterrupt:
        logger.info("server stopped by keyboard interrupt")
    except Exception as exc:  # pragma: no cover
        logger.exception("server failed: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
