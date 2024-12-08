#!/usr/bin/env python3
# Created: Dec, 04, 2024 13:52:32 by Wataru Fukuda

from collections.abc import MutableMapping
from collections import OrderedDict as _default_dict, ChainMap as _ChainMap
import itertools

class program_options(MutableMapping):
  def __init__(self, dict_type=_default_dict, *, delimiters=('=', ':')):
    self._dict = dict_type
    self._sections = self._dict()
    self._proxies = self._dict()
    self._delimiters = tuple(delimiters)
  def read(self, filename):
    fread = open(filename,'r')
    cursect = None
    optname = None
    lineno = 0
    for lineno, line in enumerate(fread, start=1):
      line = line.strip()
      if not line:
        continue
      if line.startswith('[') and line.endswith(']'):
        sectname = line[1:-1].strip()
        if sectname in self._sections:
          cursect = self._sections[sectname]
        else:
          cursect = self._dict()
          self._sections[sectname] = cursect
          self._proxies[sectname] = SectionProxy(self, sectname)
        optname = None
        continue
      if '=' in line or ':' in line:
        delimiter = '=' if '=' in line else ':'
        optname, optval = map(str.strip, line.split(delimiter, 1))
        if cursect is not None:
          cursect[optname] = optval
    self._join_multiline_values()
    fread.close()
  def has_option(self, section, option):
    if section not in self._sections:
      return False
    else:
      return (option in self._sections[section])
  def _has_section(self, section):
    return section in self._sections
  def _join_multiline_values(self):
    for section, options in self._sections.items():
      for name, val in options.items():
        if isinstance(val, list):
            val = '\n'.join(val).rstrip()
        options[name] = val
  def __getitem__(self, key):
    return self._proxies[key]
  def __setitem__(self, key, value):
    if key in self._sections:
      self._sections[key].clear()
    self.read_dict({key: value})
  def __delitem__(self, key):
    self.remove_section(key)
  def __len__(self):
    return len(self._sections)
  def __iter__(self):
    return itertools.chain( self._sections.keys())

class SectionProxy(MutableMapping):
  def __init__(self, parser, name):
    self._parser = parser
    self._name = name
  def __repr__(self):
    return '<Section: {}>'.format(self._name)
  def __getitem__(self, key):
    sectiondict = self._parser._sections.get(self._name)
    return sectiondict[key]
  def __setitem__(self, key, value):
    self._parser._validate_value_types(option=key, value=value)
    return self._parser.set(self._name, key, value)
  def __delitem__(self, key):
    self.remove_section(key)
  def __len__(self):
    return len(self._options())
  def __iter__(self):
    return self._options().__iter__()

