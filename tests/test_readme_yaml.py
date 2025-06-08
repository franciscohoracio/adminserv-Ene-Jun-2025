import re
import pathlib
import pytest

try:
    import yaml
except ImportError:
    yaml = None

README_PATH = pathlib.Path(__file__).resolve().parents[1] / "README.md"

YAML_BLOCK_RE = re.compile(r"```yaml\n(.*?)```", re.DOTALL)

def test_yaml_blocks_parse():
    content = README_PATH.read_text(encoding='utf-8')
    blocks = YAML_BLOCK_RE.findall(content)
    if not blocks:
        pytest.skip("No YAML blocks found in README")
    if yaml is None:
        pytest.fail("PyYAML is not installed")
    for block in blocks:
        yaml.safe_load(block)
