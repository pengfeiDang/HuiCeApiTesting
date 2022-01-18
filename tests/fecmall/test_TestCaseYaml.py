import pytest
from common.data_factory import TestCaseYamlFile


@pytest.mark.yaml
@pytest.mark.parametrize('file', TestCaseYamlFile.yamlFiles())
def test_FromYamlFile(runner, file):
    runner.run_path(file)
