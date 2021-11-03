from setuptools import setup, find_packages

setup(
    name='to_pypi',
    version='1.0',
    description='py_to_pypi_test',
    license='MIT License',
    install_requires=[],
    packages=find_packages(),
    # packages=['pyenv_depend'],  # 要打包的项目文件夹
    include_package_data=True,  # 自动打包文件夹内所有数据
    author='ysh',
)