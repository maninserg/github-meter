"""Modul with all settings of program github-meter

"""
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

#List for selection of languages on GitHub
list_languages = ('python',
                  'ruby',
                  'haskell',
                  'c',
                  'java',
                  'html',
                  'go',
                  'perl',
                  'javascript',
                  'r',
                  'sh',
                  'fortran',
                  'cobol',
                  'php',
                  'sql',
                  'swift',
                  'typescript',
                  'applescript')

#Settings for bar charts

my_style = LS('#333366', base_style=LCS)
my_style.tittle_font_size = 24
my_style.label_font_size = 14
my_style.major_label_font_size = 18
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.truncate_label = 15
my_config.show_y_guides = True
my_config.width = 1200
my_config.height = 600
