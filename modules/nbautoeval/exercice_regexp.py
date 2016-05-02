# -*- coding: utf-8 -*-

from __future__ import print_function

import re

from .exercice_function import ExerciceFunction

class ExerciceRegexp(ExerciceFunction):
    """
    With these exercices the students are asked to write a regexp
    which is transformed into a function that essentially
    takes an input string and returns a boolean
    that says if the *whole* string matches or not
    """
    @staticmethod
    def regexp_to_solution(regexp, match_mode):
        def solution(string):
            if match_mode in ('match', 'search'):
                if match_mode == 'match':
                    match = re.match(regexp, string)
                else:
                    match = re.search(regexp, string)
                if not match:
                    return False
                else:
                    return match.group(0) == string
            # findall returns strings, while finditer returns match instances
            elif match_mode == 'findall':
                return re.findall(regexp, string)
            elif match_mode == 'finditer':
                return [ match.span() for match in re.finditer(regexp, string)]
        return solution

    def __init__(self, name, regexp, inputs, match_mode='match', *args, **keywords):
        """
        a regexp exercice is made with
        . a user-friendly name
        . a regexp string for the solution
        . a list of inputs on which to run the regexp
        . match_mode is either 'match', 'search' or 'findall' 
        . additional settings from ExerciceFunction
        """
        solution = ExerciceRegexp.regexp_to_solution(regexp, match_mode)
        ExerciceFunction.__init__(self, solution, inputs, *args, **keywords)
        self.regexp = regexp
        self.name = name
        self.match_mode = match_mode
        self.render_name = False

    def correction(self, student_regexp):
        student_solution = ExerciceRegexp.regexp_to_solution(student_regexp, self.match_mode)
        return ExerciceFunction.correction(self, student_solution)

##############################
class ExerciceRegexpGroups(ExerciceFunction):
    """
    With these exercices the students are asked to write a regexp
    with a set of specified named groups
    a list of these groups needs to be passed to construct the object

    the regexp is then transformed into a function that again
    takes an input string and either a list of tuples 
    (groupname, found_substring) 
    or None if no match occurs
    """

    @staticmethod
    def extract_group(match, group):
        try:        return group, match.group(group)
        except:     return group, "Undefined"

    @staticmethod
    def regexp_to_solution(regexp, groups, match_mode):
        if match_mode != 'match':
            # only tested with 'match' so far
            print("WARNING: ExerciceRegexpGroups : match_mode {} not yet implemented"
                  .format(match_mode))
        def solution(string):
            if match_mode in ('match', 'search'):
                if match_mode == 'match':
                    match = re.match(regexp, string)
                else:
                    match = re.search(regexp, string)
                return match and [ExerciceRegexpGroups.extract_group(match, group)
                                  for group in groups]
            # findall returns strings, while finditer returns match instances
            elif match_mode == 'findall':
                return re.findall(regexp, string)
            elif match_mode == 'finditer':
                matches = re.finditer(regexp, string)
                return [ [ExerciceRegexpGroups.extract_group(match, group)
                          for group in groups] for match in matches ]
        return solution

    def __init__(self, name, regexp, groups, inputs, match_mode='match', *args, **keywords):
        solution = ExerciceRegexpGroups.regexp_to_solution(regexp, groups, self.match_mode)
        ExerciceFunction.__init__(self, solution, inputs, *args, **keywords)
        self.name = name
        self.regexp = regexp
        self.groups = groups
        self.match_mode = match_mode
        self.render_name = False

    def correction(self, student_regexp):
        student_solution = ExerciceRegexpGroups.regexp_to_solution(student_regexp, self.groups,
                                                                   match_mode=self.match_mode)
        return ExerciceFunction.correction(self, student_solution)
