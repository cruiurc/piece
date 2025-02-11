# Configuration file for the Sphinx documentation builder.


# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'OAKR'
copyright = '2022, cr'
author = 'cr'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
# extensions = [
# ]
# 通过配置开启graphviz插件
extensions = ['sphinx.ext.graphviz']

# 设置 graphviz_dot 路径
graphviz_dot = 'dot'
# 设置 graphviz_dot_args 的参数，这里默认了默认字体
graphviz_dot_args = ['-Gfontname=Georgia',
                     '-Nfontname=Georgia',
                     '-Efontname=Georgia']
# 输出格式，默认png，这里我用svg矢量图
graphviz_output_format = 'svg'


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bizstyle'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

language = 'zh_CN'
