#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
import types

DEFAULT_BEGIN = "<<<<<<<<<<<<<<<<< "
DEFAULT_END = ">>>>>>>>>>>>>>>>> "
DEFAULT_SPACING = '  '

OBJECT_NAME_FORM = "form[]"


def dumpif(show, obj, indent_level=0, objname=None):
    if show:
        dump(obj, indent_level, objname)


def dump(obj, indent_level=0, objname=None):
    spacing = DEFAULT_SPACING

    if objname:

        print '%s%s' % (indent_level * spacing, DEFAULT_BEGIN +
                        str(objname).upper() + ": " + DEFAULT_BEGIN)

    # if the object is of type dictionary
    if type(obj) == dict:
        print '%s{' % ((indent_level) * spacing)
        for key, value in obj.items():
            if hasattr(value, '__iter__'):
                print '%s%s:' % ((indent_level + 1) * spacing, key)
                # recurse
                dump(value, indent_level + 1)
            else:
                print '%s%s: %s' % ((indent_level + 1) * spacing, key, value)
        print '%s}' % (indent_level * spacing)
    # else if the object is of type list
    elif type(obj) == list:
        print '%s[' % ((indent_level) * spacing)
        for value in obj:
            if hasattr(value, '__iter__'):
                # recurse
                dump(value, indent_level + 1)
            else:
                print '%s%s' % ((indent_level + 1) * spacing, value)
        print '%s]' % ((indent_level) * spacing)
    elif isinstance(obj, types.GeneratorType):
        for item in obj:
            print '%s%s' % ((indent_level + 1) * spacing, item)
    else:
        print '%s%s' % (indent_level * spacing, obj)

    if objname:
        print '%s%s' % (indent_level * spacing, DEFAULT_END +
                        str(objname).upper() + ": " + DEFAULT_END)


# Helper function to dump a form within a request object
def dump_form(request, indent_level=0):
    form = request.form
    if form:
        dump(form.iterlists(), indent_level, OBJECT_NAME_FORM)
    else:
        print "!!! Warning: No " + OBJECT_NAME_FORM + " found in the request."
