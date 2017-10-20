# -*- coding: utf-8 -*-


from .characters import CHARACTERS
from .misc.lolcat import lolcat
from .topic import TOPICS, TOPICS_LABELS, TOPICS_LABEL_BANNER, TOPICS_COLORS, TOPICS_SUB_TITLES, MAX_TOPICS_LABEL_SIZE, TOPICS_COLORS_RANDOM_VALUES_LOOP
from .log import sprintf

VERSION = '0.4b1'

_txt_topics = u' Topics:\n%s' % ('\n'.join([' - %s (%s)' % (TOPICS_LABELS[t].ljust(MAX_TOPICS_LABEL_SIZE), TOPICS_SUB_TITLES[t]) for t in TOPICS]))

PROJECT_HOME = sprintf('https://github.com/naparuba/opsbro', color='magenta', end='')
MAIN_DEVS = 'Shinken Solutions Team (' + sprintf('https://www.shinken-enterprise.com/', color='magenta', end='') + ')'

# Generated by figlet -f isometric3 "OpsBro" -w 9999
TXT_BANNER = r'''
      ___           ___         ___                         ___           ___
     /  /\         /  /\       /  /\         _____         /  /\         /  /\
    /  /::\       /  /::\     /  /:/_       /  /::\       /  /::\       /  /::\
   /  /:/\:\     /  /:/\:\   /  /:/ /\     /  /:/\:\     /  /:/\:\     /  /:/\:\
  /  /:/  \:\   /  /:/~/:/  /  /:/ /::\   /  /:/~/::\   /  /:/~/:/    /  /:/  \:\
 /__/:/ \__\:\ /__/:/ /:/  /__/:/ /:/\:\ /__/:/ /:/\:| /__/:/ /:/___ /__/:/ \__\:\
 \  \:\ /  /:/ \  \:\/:/   \  \:\/:/~/:/ \  \:\/:/~/:/ \  \:\/:::::/ \  \:\ /  /:/
  \  \:\  /:/   \  \::/     \  \::/ /:/   \  \::/ /:/   \  \::/~~~~   \  \:\  /:/
   \  \:\/:/     \  \:\      \__\/ /:/     \  \:\/:/     \  \:\        \  \:\/:/
    \  \::/       \  \:\       /__/:/       \  \::/       \  \:\        \  \::/
     \__\/         \__\/       \__\/         \__\/         \__\/         \__\/
 Version: %s
%s
Project Home: %s
Developped by: %s
''' % (VERSION, _txt_topics, PROJECT_HOME, MAIN_DEVS)

BANNER = r'''[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;124m [48;5;124m [48;5;124m [48;5;234m [48;5;234m [48;5;234m [48;5;124m [48;5;124m [48;5;124m [48;5;16m [48;5;16m [48;5;16m [48;5;52m [48;5;88m [48;5;88m [48;5;88m [48;5;88m [48;5;88m [48;5;16m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;124m [48;5;124m [48;5;124m [48;5;234m [48;5;88m [48;5;88m [48;5;88m [48;5;16m [48;5;16m [48;5;88m [48;5;124m [48;5;124m [48;5;124m [48;5;124m [48;5;124m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;88m [48;5;88m [48;5;88m [48;5;234m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;173m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;180m [48;5;180m [48;5;180m [48;5;16m [48;5;16m [48;5;16m [48;5;131m [48;5;137m [48;5;137m [48;5;137m [48;5;137m [48;5;137m [48;5;137m [48;5;137m [48;5;52m [48;5;180m [48;5;180m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;52m [48;5;52m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;52m [48;5;180m [48;5;180m [48;5;180m [48;5;180m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;173m [48;5;173m [48;5;173m [48;5;173m [48;5;52m [48;5;52m [48;5;58m [48;5;58m [48;5;58m [48;5;58m [48;5;58m [48;5;58m [48;5;58m [48;5;58m [48;5;58m [48;5;52m [48;5;173m [48;5;173m [48;5;173m [48;5;173m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;173m [48;5;173m [48;5;173m [48;5;234m [48;5;236m [48;5;236m [48;5;237m [48;5;236m [48;5;236m [48;5;236m [48;5;234m [48;5;234m [48;5;234m [48;5;236m [48;5;236m [48;5;234m [48;5;236m [48;5;236m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;173m [48;5;173m [48;5;173m [48;5;234m [48;5;234m [48;5;234m [48;5;236m [48;5;236m [48;5;236m [48;5;236m [48;5;234m [48;5;234m [48;5;234m [48;5;236m [48;5;236m [48;5;234m [48;5;236m [48;5;236m [48;5;234m [48;5;234m [48;5;239m [48;5;239m [48;5;239m [48;5;239m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;173m [48;5;173m [48;5;173m [48;5;173m [48;5;173m [48;5;173m [48;5;234m [48;5;234m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;239m [48;5;239m [48;5;239m [48;5;173m [48;5;173m [48;5;173m [48;5;173m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;235m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;235m [48;5;235m [48;5;235m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;235m [48;5;235m [48;5;235m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;16m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [48;5;234m [0m
[0m'''

# Show a cool banner for our Bro
# 7 = reverse
_REVERSE = '\033[7m'
# 1 = bold
_BOLD = '\033[1m'
# 47 = white background
_WHITE_BACK = '\033[74m'
# 94 = blue
_BLUE = '\033[94m'
# 94 = blue
_MAGENTA = '\033[95m'
# 97 = white
_WHITE = '\033[97m'
# 91 = red
_RED = '\033[91m'
# 0 = reset
_RESET = '\033[0m'

# Which line to put the bro title & version
_idx = 1
banner_lines = BANNER.splitlines()
line = banner_lines[_idx].rstrip()
line_before = banner_lines[_idx - 1].rstrip()
line_after = banner_lines[_idx + 1].rstrip()


def _lolify(s):
    l = []
    chunk_size = 5
    for i in xrange(0, len(s), chunk_size):
        chunk = s[i:i + chunk_size]
        _color_idx = TOPICS_COLORS_RANDOM_VALUES_LOOP.next()
        l.append(lolcat.get_line(u'%s' % chunk, _color_idx, spread=3))
    return u''.join(l)


_OPS = '%s%s%s%sOps%s' % ('', _BOLD, '', _BLUE, _RESET)
_STAR = '%s%s%s%s*%s' % ('', _BOLD, '', _WHITE, _RESET)
_BRO = '%s%s%s%sBro%s' % ('', '', _BOLD, _RED, _RESET)

TITLE_COLOR = u'%s%s%s' % (_OPS, _STAR, _BRO)

_title = (u'%s   %s   %s   Version:%s%s%s' % (_lolify(CHARACTERS.vbar), TITLE_COLOR, _lolify(CHARACTERS.vbar), _MAGENTA, VERSION, _RESET))

before_add = (u'  %s%s%s' % (CHARACTERS.corner_top_left, CHARACTERS.hbar * 13, CHARACTERS.corner_top_right))
before_add = _lolify(before_add)
line_before += before_add
banner_lines[_idx - 1] = line_before
line += (u'  %s' % _title)
banner_lines[_idx] = line
after_add = (u'  %s%s%s' % (CHARACTERS.corner_bottom_left, CHARACTERS.hbar * 13, CHARACTERS.corner_bottom_right))
after_add = _lolify(after_add)
line_after += after_add
banner_lines[_idx + 1] = line_after

_idx_topics = 5

banner_lines[_idx_topics] += '  %sOps%s*%sBro%s goal: solve most common use cases of theses %s%s6%s Topics' % (_BLUE, _RESET, _RED, _RESET, _BOLD, _MAGENTA, _RESET)
for (i, topic) in enumerate(TOPICS):
    _color_id = TOPICS_COLORS[topic]
    topic_label = lolcat.get_line(TOPICS_LABEL_BANNER[topic].ljust(MAX_TOPICS_LABEL_SIZE), _color_id, spread=None)
    topic_sub_text = sprintf(TOPICS_SUB_TITLES[topic], color='grey', end='')
    suffix = '  %s %s %s' % (topic_label, CHARACTERS.arrow_left, topic_sub_text)
    banner_lines[_idx_topics + i + 1] += suffix

_idx_project_home = _idx_topics + len(TOPICS) + 2
_project_home_line = banner_lines[_idx_project_home]
_project_home_line += u'  Project: %s' % PROJECT_HOME
banner_lines[_idx_project_home] = _project_home_line

_idx_main_devs = _idx_project_home + 1
_project_main_devs = banner_lines[_idx_main_devs]
_project_main_devs += u'  By     : %s' % MAIN_DEVS
banner_lines[_idx_main_devs] = _project_main_devs


######### Gun RAY
'''
_idx_gun = 9

line_gun_before = banner_lines[_idx_gun - 1]
line_gun = banner_lines[_idx_gun]
line_gun_after = banner_lines[_idx_gun + 1]

gun_raw_len = 50
raw_gun_ray_before = u' ' * 3 + u''.join([CHARACTERS.higer_gun for _i in xrange(gun_raw_len - 1)])
raw_gun_ray = u' ᠁' + u''.join([CHARACTERS.middle_gun for _i in xrange(gun_raw_len)])
raw_gun_ray_after = u' ' * 3 + u''.join([CHARACTERS.lower_gun for _i in xrange(gun_raw_len - 1)])
lol_cat_idx = random.randint(0, 256)

# print 3 lines with small offset
gun_raw_lol_before = lolcat.get_line(raw_gun_ray_before, lol_cat_idx - 1)
gun_raw_lol = lolcat.get_line(raw_gun_ray, lol_cat_idx)
gun_raw_lol_after = lolcat.get_line(raw_gun_ray_after, lol_cat_idx + 1)

line_gun_before += gun_raw_lol_before
line_gun += gun_raw_lol
line_gun_after += gun_raw_lol_after

banner_lines[_idx_gun - 1] = line_gun_before
banner_lines[_idx_gun] = line_gun
banner_lines[_idx_gun + 1] = line_gun_after
'''

BANNER = u'\n'.join(banner_lines)
