
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'pair_groupDIGIT LETTER SEMI pair : LETTER DIGIT SEMI  pair_group : pair_group pair\n                   | pair\n    '
    
_lr_action_items = {'LETTER':([0,1,2,4,6,],[3,3,-3,-2,-1,]),'$end':([1,2,4,6,],[0,-3,-2,-1,]),'DIGIT':([3,],[5,]),'SEMI':([5,],[6,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'pair_group':([0,],[1,]),'pair':([0,1,],[2,4,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> pair_group","S'",1,None,None,None),
  ('pair -> LETTER DIGIT SEMI','pair',3,'p_letter_digit_pair','parse_lex.py',24),
  ('pair_group -> pair_group pair','pair_group',2,'p_pair_group','parse_lex.py',28),
  ('pair_group -> pair','pair_group',1,'p_pair_group','parse_lex.py',29),
]
