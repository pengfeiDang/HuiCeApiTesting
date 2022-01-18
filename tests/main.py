import pytest
from common.config_parser import config


pytest.main(['-s',  '-m', 'fecmall99', '--clean-alluredir', f'--alluredir={config.result_path}'])
# pytest.main(['-s', '-m', 'fecmall99'])
