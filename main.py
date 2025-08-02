import pytest
from utils.handle_path import report_path

if __name__ == '__main__':
    # 执行所有用例
    # -v：显示详细信息
    # -s：显示print内容
    # --alluredir：生成allure报告目录（可选）
    pytest.main(['-vs', './testcase','--clean-alluredir', '--alluredir', report_path])
