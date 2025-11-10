from urllib.parse import urlparse

from django.http import HttpRequest


def get_hostname_and_port_from_request(
    request: HttpRequest,
) -> tuple[str | None, int | None]:
    try:
        hostname = request.get_host().split(":")[0]
    except KeyError:
        hostname = None

    try:
        port = request.get_port()
    except (AttributeError, KeyError):
        port = request.META.get("SERVER_PORT")

    port = int(port) if port is not None else None

    return hostname, port


def make_root_url(hostname: str, port: int) -> str:
    if port == 80:
        return f"http://{hostname}"
    elif port == 443:
        return f"https://{hostname}"
    else:
        return f"http://{hostname}:{port}"


def parse_host(host: str) -> tuple[str, int]:
    """Parse a host string and return a hostname and port."""
    if host.startswith(("http://", "https://")):
        parsed = urlparse(host)

        hostname = parsed.hostname
        if parsed.port:
            port = parsed.port
        else:
            port = 443 if parsed.scheme == "https" else 80
    elif ":" in host:
        hostname, port_str = host.rsplit(":", 1)
        port = int(port_str)
    else:
        hostname = host
        port = 80

    if not hostname:
        raise ValueError(host)

    return hostname, port
