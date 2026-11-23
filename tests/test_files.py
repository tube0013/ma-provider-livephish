"""Checks of the provider's files that need no server; the catalog refuses a release that fails them."""

import json
import re
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import pytest
from music_assistant_models.provider import ProviderManifest

from music_assistant import providers
from tests import DOMAIN, REPOSITORY

# where the community catalog and the server take the provider from: a folder named after its
# domain, provider, or providers/<domain> in a repository with several providers
FOLDERS = (REPOSITORY / DOMAIN, REPOSITORY / "provider", REPOSITORY / "providers" / DOMAIN)
FOUND = [path for path in FOLDERS if (path / "manifest.json").is_file()]
PROVIDER = FOUND[0] if FOUND else FOLDERS[0]
# a package name with optional extras and version specifiers, as the server installs them
REQUIREMENT = re.compile(
    r"[A-Za-z0-9][A-Za-z0-9._-]*(\[[A-Za-z0-9._, -]+\])?"
    r"(\s*(==|>=|<=|~=|!=|<|>)\s*[A-Za-z0-9.*+!_-]+"
    r"(\s*,\s*(==|>=|<=|~=|!=|<|>)\s*[A-Za-z0-9.*+!_-]+)*)?"
)
MAX_ICON_BYTES = 5 * 1024
SERVER_TRANSLATIONS = Path(providers.__file__).parents[1] / "translations"
SVG = "{http://www.w3.org/2000/svg}"


def test_one_provider_folder() -> None:
    """The provider is in one folder the catalog takes it from; its manifest and the CI agree."""
    found = [path.relative_to(REPOSITORY).as_posix() for path in FOUND]
    assert len(found) == 1, (
        f"expected the provider in one of {DOMAIN}, provider or providers/{DOMAIN}, found {found}"
    )
    folder = found[0]
    assert _manifest()["domain"] == DOMAIN
    ci = (REPOSITORY / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert f"folder: {folder}\n" in ci, "the folder in ci.yml is not the provider folder"


def test_domain_is_free() -> None:
    """The server has no provider of its own with this domain."""
    builtin = Path(providers.__file__).parent / DOMAIN
    assert not builtin.exists(), f"the server already has a provider named {DOMAIN}"


async def test_manifest_is_valid() -> None:
    """The manifest is plain JSON that the server parses."""
    manifest = await ProviderManifest.parse(str(PROVIDER / "manifest.json"))
    assert manifest.name.strip()
    assert manifest.description.strip()
    assert manifest.codeowners


def test_requirements_are_package_names() -> None:
    """Each requirement is a package name with version specifiers: no URL, marker or option."""
    for requirement in _manifest().get("requirements", []):
        assert requirement.isprintable(), requirement
        assert REQUIREMENT.fullmatch(requirement), requirement


def test_texts_are_valid() -> None:
    """The texts are plain JSON, translated only into languages the server has."""
    texts = _keys(_read_json(PROVIDER / "strings.json"))
    # strings.json holds the English texts; the server ignores a translations/en.json
    languages = {path.stem for path in SERVER_TRANSLATIONS.glob("*.json")} - {"en"}
    for path in (PROVIDER / "translations").glob("*.json"):
        assert path.stem in languages, f"the server has no translations into {path.stem}"
        extra = _keys(_read_json(path)) - texts
        assert not extra, f"{path.name} has texts that strings.json does not have: {extra}"


def test_icon_only_draws() -> None:
    """The icon is a small SVG without scripts, event handlers or references out of the file."""
    # a first check; the catalog checks the icon in full, see the README
    path = PROVIDER / "icon.svg"
    if not path.exists():
        pytest.skip("the provider has no icon.svg")
    content = path.read_text(encoding="utf-8")
    assert len(content.encode()) <= MAX_ICON_BYTES, "the icon is larger than 5 KB"
    assert "<!" not in content.replace("<!--", ""), "the icon holds a declaration"
    root = ET.fromstring(content)  # noqa: S314 - declarations are refused above
    assert root.tag == f"{SVG}svg"
    for element in root.iter():
        assert element.tag.startswith(SVG), f"{element.tag} is not an SVG element"
        assert element.tag.removeprefix(SVG) not in {"script", "foreignObject", "a", "animate"}
        for key, value in element.attrib.items():
            assert not key.lower().startswith("on"), f"event handler {key}"
            targets = [*re.findall(r"url\(\s*['\"]?([^'\")]*)", value)]
            if key.endswith("href"):
                targets.append(value)
            assert all(target.startswith("#") for target in targets), f"{key} refers out"


def _manifest() -> dict[str, Any]:
    """Return the content of the manifest."""
    manifest = _read_json(PROVIDER / "manifest.json")
    assert isinstance(manifest, dict)
    return manifest


def _keys(texts: Any, prefix: str = "") -> set[str]:
    """Return the keys of nested texts, joined with dots."""
    if not isinstance(texts, dict):
        return {prefix}
    return {key for name, value in texts.items() for key in _keys(value, f"{prefix}{name}.")}


def _read_json(path: Path) -> Any:
    """Return the content of a JSON file, refusing NaN, Infinity and a key that appears twice."""

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        keys = [key for key, _ in items]
        assert len(keys) == len(set(keys)), f"{path.name} has a key twice"
        return dict(items)

    def constant(value: str) -> None:
        msg = f"{path.name} holds {value}"
        raise AssertionError(msg)

    return json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=pairs, parse_constant=constant
    )
