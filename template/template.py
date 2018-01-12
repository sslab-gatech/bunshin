#!/usr/bin/env python

import os
import re
import logging
import warnings
from enum import Enum
from collections import OrderedDict

# templates
SYSCALL_TEMPLATE = "syscall.tpl"
GROUP_H_TEMPLATE = "group_h.tpl"
GROPU_C_TEMPLATE = "group_c.tpl"

# substitution
ELEMENT_PATTERN = re.compile("\{\{(\w+)\}\}")
BLOCK_BEGIN_PATTERN = re.compile("\+\+\+ begin of \{\{(\w+)\}\} \+\+\+")
BLOCK_END_PATTERN = re.compile("\+\+\+ end of block \+\+\+")

# path related
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(ROOT, "kmvee")
SYSLIST = os.path.join(ROOT, "template", "syscall.list")

# misc
TAB_SIZE = 2

def format_line(code, prefix):
    return code.replace("\n", "\n" + prefix).expandtabs(TAB_SIZE)

def combine_valid(*args):
    stmts = []
    for arg in args:
        if arg is not None and len(arg) != 0:
            stmts.append(arg)

    if len(stmts) == 0:
        return None
    
    return "\n".join(stmts)

def generate_from_members(members, name, prefix):
    stmts = []
    for member in members:
        generated = getattr(member, "gen_%s" % name)()
        if generated is not None and len(generated) != 0:
            stmts.append(generated)

    return format_line("\n".join(stmts), prefix)

def generate_from_template(obj, path):
    code = []

    with open(path, "r") as f:
        contents = f.readlines()
        for line in contents:
            line = line.strip("\n")
            matches = ELEMENT_PATTERN.findall(line)
            for element in matches:
                target = "{{%s}}" % element
                prefix = line[0:len(line) - len(line.lstrip())]

                generated = getattr(obj, "build_%s" % element)()
                formatted = format_line(generated, prefix)

                line = line.replace(target, formatted)

            code.append(line)

    return "\n".join(code)

def generate_from_comments(groups, path):
    modified = []
    section = False

    with open(path, "r") as f:
        contents = f.readlines()
        for line in contents:
            if not section:
                modified.append(line)

            match = BLOCK_BEGIN_PATTERN.search(line)
            if match:
                section = True
                element = match.group(1)
                prefix = line[0:len(line) - len(line.lstrip())]

                stmts = []
                for group in groups:
                    generated = getattr(group, "build_%s" % element)()
                    formatted = format_line(generated, prefix)
                    stmts.append(formatted)

                modified.append("\n".join(stmts))
                modified.append("\n")

            match = BLOCK_END_PATTERN.search(line)
            if match:
                section = False
                modified.append("\n"+line)

    with open(path, "w") as f:
        f.writelines(modified)


class Flow(Enum):
    USER            = 0
    KERNEL          = 1
    BOTH            = 2


class Element(Enum):
    VALUE           = 0 # pass-by-value
    SIMPLE          = 1 # pointer of simple type
    TYPE            = 2 # size known at compile time
    STRUCT          = 3 # field-by-field comparision
    STRING          = 4 # size determined by strlen

    BUFFER          = 5 # void *, size given by var
    POLY            = 6 # struct type with var size
    IBUFFER         = 7 # void *, size given by *var
    IPOLY           = 8 # struct type with *var size
    
    VALUE_FIX       = 9 # fixed-lengh array of value type
    VALUE_VAR       = 10 # var-length array of value type
    STRUCT_FIX      = 11 # fixed-length array of struct type
    STRUCT_VAR      = 12 # var-length array of struct type


class Condition(Enum):
    IN              = 0
    NOT_IN          = 1
    IS              = 2
    IS_NOT          = 3


class Parameter:

    def __init__(self, pos, defs, name, 
            flow, base, elem, eidx=None, struct=None,
            checkin=None, compare=None, pclean=None,
            turnin=None, fetch=None, rclean=None):

        nptr = defs.count("*")

        tempvar = "temp_%s" % name
        sizevar = "size_%s" % name
        itervar = "iter_%s" % name 

        self.pos = pos
        self.defs = defs
        self.name = name

        self.nptr = nptr 

        self.tempvar = tempvar
        self.sizevar = sizevar
        self.itervar = itervar

        self.flow = flow
        self.base = base
        self.elem = elem 
        self.eidx = eidx
        self.struct = struct

        self.checkin = checkin 
        self.compare = compare 
        self.pclean = pclean

        self.turnin = turnin 
        self.fetch = fetch 
        self.rclean = rclean

        self.syscall = None

    def warn(self, msg):
        warnings.warn("[%s, %s]: %s") % \
                (self.syscall.name, self.name, msg)

    def to_def(self):
        if self.nptr > 0:
            return "%s%s" % (self.defs, self.name)
        else:
            return "%s %s" % (self.defs, self.name)

    def to_use(self):
        return "%s" % self.name

    def to_dev(self, tabs):
        raw = \
'''log_e(vcb, "SYS", __NR_%s, "deviation -> %s");
on_deviation(vcb);''' % (self.syscall.name, self.name)

        return format_line(raw, "\t" * tabs)

    def to_get(self):
        if self.elem == Element.VALUE:
            return "%s = %s;" % (self.tempvar, self.name)

        elif self.elem == Element.SIMPLE:
            return \
'''if(%s){
\t%s = vmalloc(sizeof(%s));
\tget_user(*%s, %s);
} else {
\t%s = NULL;
}''' % (self.name, 
        self.tempvar, self.base,
        self.tempvar, self.name,
        self.tempvar)

        elif self.elem == Element.TYPE:
            return \
'''if(%s){
\t%s = vmalloc(sizeof(%s));
\tcopy_from_user(%s, %s, sizeof(%s));
} else {
\t%s = NULL;
}''' % (self.name,
        self.tempvar, self.base,
        self.tempvar, self.name, self.base,
        self.tempvar)

        elif self.elem == Element.STRUCT:
            return \
'''if(%s){
\t%s = vmalloc(sizeof(%s));
\tcopy_from_user_STRUCT_%s(%s, %s);
} else {
\t%s = NULL;
}''' % (self.name,
        self.tempvar, self.base,
        self.struct, self.tempvar, self.name,
        self.tempvar)

        elif self.elem == Element.STRING:
            return \
'''if(%s){
\t%s = strlen_user(%s) + 1;
\t%s = vmalloc(%s);
\tstrncpy_from_user(%s, %s, %s);
} else {
\t%s = NULL;
}''' % (self.name,
        self.sizevar, self.name,
        self.tempvar, self.sizevar,
        self.tempvar, self.name, self.sizevar,
        self.tempvar)

        elif self.elem == Element.BUFFER:
            return \
'''if(%s && %s){
\t%s = vmalloc(%s);
\tcopy_from_user(%s, %s, %s);
} else {
\t%s = NULL;
}''' % (self.name, self.syscall.positions[self.eidx].name,
        self.tempvar, self.syscall.positions[self.eidx].name,
        self.tempvar, self.name, self.syscall.positions[self.eidx].name, 
        self.tempvar)

        elif self.elem == Element.POLY:
            return \
'''if(%s && %s){
\t%s = vmalloc(%s);
\tcopy_from_user_POLY_%s(%s, %s);
} else {
\t%s = NULL;
}''' % (self.name, self.syscall.positions[self.eidx].name,
        self.tempvar, self.syscall.positions[self.eidx].name,
        self.struct, self.tempvar, self.name,
        self.tempvar)

        elif self.elem == Element.IBUFFER:
            return \
'''get_user(%s, %s);
if(%s && %s){
\t%s = vmalloc(%s);
\tcopy_from_user(%s, %s, %s);
} else {
\t%s = NULL;
}''' % (self.sizevar, self.syscall.positions[self.eidx].name,
        self.name, self.sizevar,
        self.tempvar, self.sizevar,
        self.tempvar, self.name, self.sizevar,
        self.tempvar)

        elif self.elem == Element.IPOLY:
            return \
'''get_user(%s, %s);
if(%s && %s){
\t%s = vmalloc(%s);
\tcopy_from_user_POLY_%s(%s, %s);
} else {
\t%s = NULL;
}''' % (self.sizevar, self.syscall.positions[self.eidx].name,
        self.name, self.sizevar,
        self.tempvar, self.sizevar,
        self.struct, self.tempvar, self.name,
        self.tempvar)

        elif self.elem == Element.VALUE_FIX:
            return \
'''%s = sizeof(%s) * %d;
if(%s && %s){
\t%s = vmalloc(%s);
\tfor(%s=0; %s<%d; %s++){
\t\tget_user(%s[%s], %s + %s);
\t}
} else {
\t%s = NULL;
}''' % (self.sizevar, self.base, self.eidx,
        self.name, self.sizevar,
        self.tempvar, self.sizevar,
        self.itervar, self.itervar, self.eidx, self.itervar,
        self.tempvar, self.itervar, self.name, self.itervar,
        self.tempvar)

        elif self.elem == Element.VALUE_VAR:
            return \
'''%s = sizeof(%s) * %s;
if(%s && %s){
\t%s = vmalloc(%s);
\tfor(%s=0; %s<%s; %s++){
\t\tget_user(%s[%s], %s + %s);
\t}
} else {
\t%s = NULL;
}''' % (self.sizevar, self.base, self.syscall.positions[self.eidx].name,
        self.name, self.sizevar,
        self.tempvar, self.sizevar,
        self.itervar, self.itervar, self.syscall.positions[self.eidx].name, self.itervar,
        self.tempvar, self.itervar, self.name, self.itervar,
        self.tempvar)

        elif self.elem == Element.STRUCT_FIX:
            return \
'''%s = sizeof(%s) * %d;
if(%s && %s){
\t%s = vmalloc(%s);
\tfor(%s=0; %s<%d; %s++){
\t\tcopy_from_user_STRUCT_%s(%s + %s, %s + %s);
\t}
} else {
\t%s = NULL;
}''' % (self.sizevar, self.base, self.eidx,
        self.name, self.sizevar,
        self.tempvar, self.sizevar,
        self.itervar, self.itervar, self.eidx, self.itervar,
        self.struct, self.tempvar, self.itervar, self.name, self.itervar,
        self.tempvar)

        elif self.elem == Element.STRUCT_VAR:
            return \
'''%s = sizeof(%s) * %s;
if(%s && %s){
\t%s = vmalloc(%s);
\tfor(%s=0; %s<%s; %s++){
\t\tcopy_from_user_STRUCT_%s(%s + %s, %s + %s);
\t} 
} else {
\t%s = NULL;
}''' % (self.sizevar, self.base, self.syscall.positions[self.eidx].name,
        self.name, self.sizevar,
        self.tempvar, self.sizevar,
        self.itervar, self.itervar, self.syscall.positions[self.eidx].name, self.itervar,
        self.struct, self.tempvar, self.itervar, self.name, self.itervar,
        self.tempvar)

        else:
            self.warn("unknown element type")

        return None

    def to_compare(self):
        if self.elem == Element.VALUE:
            return \
'''if(%s != %s){
\t%s
}''' % (self.name, self.tempvar, 
        self.to_dev(1))

        elif self.elem == Element.SIMPLE:
            return \
'''if(%s){
\tif(!%s || *%s != *%s){
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar, self.name, self.tempvar,
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.TYPE:
            return \
'''if(%s){
\tif(!%s || memcmp(%s, %s, sizeof(%s))){
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar, self.name, self.tempvar, self.base,
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.STRUCT:
            return \
'''if(%s){
\tif(!%s || compare_with_user_STRUCT_%s(%s, %s)){
\t\t%s
\t} 
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar, self.struct, self.name, self.tempvar,
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.STRING:
            return \
'''if(%s){
\tif(!%s || strcmp(%s, %s)){
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar, self.name, self.tempvar,
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.BUFFER:
            return \
'''if(%s){
\tif(!%s || memcmp(%s, %s, %s)){
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar, self.name, self.tempvar, self.syscall.positions[self.eidx].name,
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.POLY:
            return \
'''if(%s){
\tif(!%s || compare_with_user_POLY_%s(%s, %s)){
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar, self.struct, self.name, self.tempvar,
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.VALUE_FIX:
            return \
'''if(%s){
\tif(%s){
\t\tfor(%s=0; %s<%d; %s++){
\t\t\tif(%s[%s] != %s[%s]){
\t\t\t\t%s
\t\t\t}
\t\t}
\t} else {
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar,
        self.itervar, self.itervar, self.eidx, self.itervar,
        self.name, self.itervar, self.tempvar, self.itervar,
        self.to_dev(3),
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.VALUE_VAR:
            return \
'''if(%s){
\fif(%s){
\t\tfor(%s=0; %s<%s; %s++){
\t\t\tif(%s[%s] != %s[%s]){
\t\t\t\t%s
\t\t\t}
\t\t}
\t} else {
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar,
        self.itervar, self.itervar, self.syscall.positions[self.eidx].name, self.itervar,
        self.name, self.itervar, self.tempvar, self.itervar,
        self.to_dev(3),
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.STRUCT_FIX:
            return \
'''if(%s){
\tif(%s){
\t\tfor(%s=0; %s<%d; %s++){
\t\t\tif(compare_with_user_STRUCT_%s(%s + %s, %s + %s)){
\t\t\t\t%s
\t\t\t}
\t\t}
\t} else {
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar,
        self.itervar, self.itervar, self.eidx, self.itervar,
        self.struct, self.name, self.itervar, self.tempvar, self.itervar,
        self.to_dev(3),
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        elif self.elem == Element.STRUCT_VAR:
            return \
'''if(%s){
\tif(%s){
\t\tfor(%s=0; %s<%s; %s++){
\t\t\tif(compare_with_user_STRUCT_%s(%s + %s, %s + %s)){
\t\t\t\t%s
\t\t\t}
\t\t}
\t} else {
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar,
        self.itervar, self.itervar, self.syscall.positions[self.eidx].name, self.itervar,
        self.struct, self.name, self.itervar, self.tempvar, self.itervar,
        self.to_dev(3),
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        else:
            self.warn("unknown element type")

    def to_put(self):
        if self.elem == Element.VALUE:
            return "%s = %s;" % (self.name, self.tempvar)
        
        elif self.elem == Element.SIMPLE:
            return \
'''if(%s){
\tput_user(*%s, %s);
}''' % (self.name, 
        self.tempvar, self.name)

        elif self.elem == Element.TYPE:
            return \
'''if(%s){
\tcopy_to_user(%s, %s, sizeof(%s));
}''' % (self.name,
        self.name, self.tempvar, self.base)

        elif self.elem == Element.STRUCT:
            return \
'''if(%s){
\tcopy_to_user_STRUCT_%s(%s, %s);
}''' % (self.name,
        self.struct, self.name, self.tempvar)

        elif self.elem == Element.STRING:
            return \
'''if(%s){
\tstrncpy(%s, %s, strlen(%s) + 1);
}''' % (self.name,
        self.name, self.tempvar, self.tempvar)

        elif self.elem == Element.BUFFER:
            return \
'''if(%s){
\tcopy_to_user(%s, %s, %s);
}''' % (self.name, 
        self.name, self.tempvar, self.syscall.positions[self.eidx].name)

        elif self.elem == Element.POLY:
            return \
'''if(%s){
\tcopy_to_user_POLY_%s(%s, %s);
}''' % (self.name,
        self.struct, self.name, self.tempvar)

        elif self.elem == Element.IBUFFER:
            return \
'''if(%s){
\tcopy_to_user(%s, %s, *%s);
}''' % (self.name,
        self.name, self.tempvar, self.syscall.positions[self.eidx].tempvar)

        elif self.elem == Element.IPOLY:
            return \
'''if(%s){
\tcopy_to_user_POLY_%s(%s, %s);
}''' % (self.name,
        self.struct, self.name, self.tempvar)

        elif self.elem == Element.VALUE_FIX:
            return \
'''if(%s){
\tfor(%s=0; %s<%d; %s++){
\t\tput_user(%s[%s], %s + %s);
\t}
}''' % (self.name,
        self.itervar, self.itervar, self.eidx, self.itervar,
        self.tempvar, self.itervar, self.name, self.itervar)

        elif self.elem == Element.VALUE_VAR:
            return \
'''if(%s){
\tfor(%s=0; %s<%s; %s++){
\t\tput_user(%s[%s], %s + %s);
\t}
}''' % (self.name, 
        self.itervar, self.itervar, self.syscall.positions[self.eidx].name, self.itervar,
        self.tempvar, self.itervar, self.name, self.itervar)

        elif self.elem == Element.STRUCT_FIX:
            return \
'''if(%s){
\tfor(%s=0; %s<%d; %s++){
\t\tcopy_to_user_STRUCT_%s(%s + %s, %s + %s);
\t}
}''' % (self.name,
        self.itervar, self.itervear, self.eidx, self.itervar,
        self.struct, self.name, self.itervar, self.tempvar, self.iterver)

        elif self.elem == Element.STRUCT_VAR:
            return \
'''if(%s){
\tfor(%s=0; %s<%s; %s++){
\t\tcopy_to_user_STRUCT_%s(%s + %s, %s + %s);
\t}
}''' % (self.name, 
        self.itervar, self.itervar, self.syscall.positions[self.eidx].name, self.itervar,
        self.struct, self.name, self.itervar, self.tempvar, self.itervar)

        else:
            self.warn("unknown element type")

        return None

    def to_clean(self):
        if self.elem == Element.VALUE:
            return None

        elif self.elem in [Element.SIMPLE, Element.TYPE, Element.STRING,
                Element.BUFFER, Element.IBUFFER,
                Element.VALUE_FIX, Element.VALUE_VAR]:

            return \
'''if(%s){
\tvfree(%s);
}''' % (self.tempvar, 
        self.tempvar)

        elif self.elem == Element.STRUCT:
            return \
'''if(%s){
\tclean_STRUCT_%s(%s);
\tvfree(%s);
}''' % (self.tempvar,
        self.struct, self.tempvar,
        self.tempvar)

        elif self.elem in [Element.POLY, Element.IPOLY]:
            return \
'''if(%s){
\tclean_POLY_%s(%s);
\tvfree(%s);
}'''

        elif self.elem == Element.STRUCT_FIX:
            return \
'''if(%s){
\tfor(%s=0; %s<%d; %s++){
\t\tclean_STRUCT_%s(%s + %s);
\t}
\tvfree(%s);
}''' % (self.tempvar,
        self.itervar, self.itervar, self.eidx, self.itervar,
        self.struct, self.tempvar, self.itervar,
        self.tempvar)

        elif self.elem == Element.STRUCT_VAR:
            return \
'''if(%s){
\tfor(%s=0; %s<%s; %s++){
\t\tclean_STRUCT_%s(%s + %s);
\t}
\tvfree(%s);
}''' % (self.tempvar,
        self.itervar, self.itervar, self.syscall.positions[self.eidx].name, self.itervar,
        self.struct, self.tempvar, self.itervar,
        self.tempvar)

        else: 
            self.warn("unknown element type") 

        return None

    def to_plassign(self):
        if self.nptr > 0:
            return "pslot->params[%d].ptr = %s;" % (self.pos, self.tempvar)
        else:
            return "pslot->params[%d].val = %s;" % (self.pos, self.tempvar)

    def to_rlassign(self):
        if self.flow in [Flow.USER, Flow.BOTH]:
            return "rslot->results[%d] = %s;" % (self.pos, self.tempvar)
        elif self.flow == Flow.KERNEL:
            return None
        else:
            self.warn("unknown flow type")

        return None

    def to_pfassign(self):
        if self.nptr > 0:
            return "%s = pslot->params[%d].ptr;" % (self.tempvar, self.pos)
        else:
            return "%s = pslot->params[%d].val;" % (self.tempvar, self.pos)

    def to_rfassign(self):
        if self.flow in [Flow.USER, Flow.BOTH]:
            return "%s = rslot->results[%d];" % (self.tempvar, self.pos)
        elif self.flow == Flow.KERNEL:
            return None
        else:
            self.warn("unknown flow type")

        return None

    def gen_checkin(self):
        if self.checkin is not None:
            code = self.checkin

        elif self.flow in [Flow.KERNEL, Flow.BOTH]:
            code = self.to_get()
        
        elif self.flow == Flow.USER:
            code = "%s = %s;" % (self.tempvar, self.name)

        else:
            self.warn("unknown flow type")
            code = None

        return combine_valid(code, self.to_plassign())

    def gen_compare(self):
        if self.compare is not None:
            code = self.compare

        elif self.flow in [Flow.KERNEL, Flow.BOTH]:
            code = self.to_compare()

        elif self.flow == Flow.USER:
            code = \
'''if(%s){
\tif(!%s){
\t\t%s
\t}
} else if(%s){
\t%s
}''' % (self.name,
        self.tempvar,
        self.to_dev(2),
        self.tempvar,
        self.to_dev(1))

        else:
            self.warn("unknown flow type")
            code = None

        return combine_valid(self.to_pfassign(), code)

    def gen_turnin(self):
        if self.turnin is not None:
            code = self.turnin

        elif self.flow in [Flow.USER, Flow.BOTH]:
            code = self.to_get()

        elif self.flow == Flow.KERNEL:
            code = None

        else:
            self.warn("unknown flow type")
            code = None

        return combine_valid(code, self.to_rlassign())

    def gen_fetch(self):
        if self.fetch is not None:
            code = self.fetch

        elif self.flow in [Flow.USER, Flow.BOTH]:
            code = self.to_put()

        elif self.flow == Flow.KERNEL:
            code = None

        else:
            self.warn("unknown flow type")
            code = None

        return combine_valid(self.to_rfassign(), code) 

    def gen_pclean(self):
        if self.pclean is not None:
            return self.pclean

        elif self.flow in [Flow.KERNEL, Flow.BOTH]:
            return self.to_clean()

        elif self.flow == Flow.USER:
            return None

        else:
            self.warn("unknown flow type")

        return None

    def gen_rclean(self):
        if self.rclean is not None:
            return self.rclean

        elif self.flow in [Flow.USER, Flow.BOTH]:
            return self.to_clean()

        elif self.flow == Flow.KERNEL:
            return None

        else:
            self.warn("unknown flow type")

        return None

    def gen_vardef(self):
        stmts = []

        if self.nptr > 0:
            stmts.append("%s %s%s;" % (self.base, "*" * self.nptr, self.tempvar))
        else:
            stmts.append("%s %s;" % (self.base, self.tempvar))

        if self.elem in [Element.STRING, Element.IBUFFER, Element.IPOLY,
                Element.VALUE_FIX, Element.VALUE_VAR, 
                Element.STRUCT_FIX, Element.STRUCT_VAR]:

            stmts.append("long %s;" % self.sizevar)

        if self.elem in [Element.VALUE_FIX, Element.VALUE_VAR, 
                Element.STRUCT_FIX, Element.STRUCT_VAR]:

            stmts.append("int %s;" % self.itervar)

        return "\n".join(stmts) 


class Field(Enum):
    SIMPLE          = 0
    CHARS           = 1
    ARRAY           = 2
    EMBED           = 3
    BUFFER          = 4


class Member:

    def __init__(self, name, field, 
            fidx=None, ftype=None, fdir=None,
            get=None, put=None, compare=None, clean=None):

        self.name = name

        self.field = field
        self.fidx = fidx
        self.ftype = ftype
        self.fdir = fdir

        self.get = get
        self.put = put
        self.compare = compare
        self.clean = clean

    def gen_get(self):
        if self.get is not None:
            return self.get

        if self.field == Field.SIMPLE:
            return "kside->%s = uside->%s;" % (self.name, self.name)

        elif self.field == Field.CHARS:
            return "strncpy_from_user(kside->%s, uside->%s, %s);" % \
                    (self.name, self.name, self.fidx)

        elif self.field == Field.ARRAY:
            return \
'''for(int i=0; i<%d; i++){
\tkside->%s[i] = uside->%s[i];
}''' % (self.fidx,
        self.name, self.name)

        elif self.field == Field.EMBED:
            return "copy_from_user(&kside->%s, &uside->%s, sizeof(%s));" % \
                    (self.name, self.name, self.ftype)

        elif self.field == Field.BUFFER:
            if self.fdir in [Flow.KERNEL, Flow.BOTH]:
                return \
'''kside->%s = vmalloc(uside->%s);
copy_from_user(kside->%s, uside->%s, uside->%s);''' % \
        (self.name, self.fidx,
                self.name, self.name, self.fidx)

            elif self.fdir == Flow.USER:
                return "kside->%s = uside->%s;" % (self.name, self.name)

        return None


    def gen_put(self):
        if self.put is not None:
            return self.put

        if self.field == Field.SIMPLE:
            return "uside->%s = kside->%s;" % (self.name, self.name)

        elif self.field == Field.CHARS:
            return "strncpy(uside->%s, kside->%s, %s);" % \
                    (self.name, self.name, self.fidx)

        elif self.field == Field.ARRAY:
            return \
'''for(int i=0; i<%d; i++){
\tuside->%s[i] = kside->%s[i];
}''' % (self.fidx,
        self.name, self.name)

        elif self.field == Field.EMBED:
            return "copy_to_user(&uside->%s, &kside->%s, sizeof(%s));" % \
                    (self.name, self.name, self.ftype)

        elif self.field == Field.BUFFER:
            if self.fdir in [Flow.USER, Flow.BOTH]:
                return "copy_to_user(uside->%s, kside->%s, uside->%s);" % \
                        (self.name, self.name, self.fidx)

        return None

    def gen_compare(self):
        if self.compare is not None:
            return self.compare

        if self.field == Field.SIMPLE:
            return "(uside->%s != kside->%s)" % (self.name, self.name)

        elif self.field == Field.CHARS:
            return "strcmp(uside->%s, kside->%s)" % (self.name, self.name)

        elif self.field == Field.ARRAY:
            return "memcmp(uside->%s, kside->%s, sizeof(%s) * %d)" % \
                    (self.name, self.name, self.ftype, self.fidx)

        elif self.field == Field.EMBED:
            return "memcmp(&uside->%s, &kside->%s, sizeof(%s))" % \
                    (self.name, self.name, self.ftype)

        elif self.field == Field.BUFFER:
            if self.fdir in [Flow.KERNEL, Flow.BOTH]:
                return "memcmp(uside->%s, kside->%s, uside->%s)" % \
                        (self.name, self.name, self.fidx)
            elif self.fdir == Flow.USER:
                return "(uside->%s ? kside->%s == NULL : kside->%s != NULL)" % \
                        (self.name, self.name, self.name)

        return None

    def gen_clean(self):
        if self.clean is not None:
            return self.clean

        if self.field == Field.BUFFER:
            if self.fdir in [Flow.KERNEL, Flow.BOTH]:
                return "vfree(kside->%s);" % self.name

        return None 


class Struct:

    def __init__(self, name, base, includes):

        self.name = name 
        self.base = base
        self.includes = includes

        self.members = []
        self.syscalls = []

    def add_member(self, member):
        self.members.append(member)

    def wrapper(self, stmt):
        assert len(self.syscalls) > 0
        return \
'''#if %s
%s
#endif''' % (" || ".join("defined(__NR_%s)" % s.name for s in self.syscalls), stmt)

    def to_get(self):
        return \
'''static inline void copy_from_user_STRUCT_%s
\t(%s *kside, %s __user *uside){

\t%s
}''' % (self.name, self.base, self.base, 
        generate_from_members(self.members, "get", "\t")) 

    def to_put(self):
        return \
'''static inline void copy_to_user_STRUCT_%s
\t(%s __user *uside, %s *kside){

\t%s
}''' % (self.name, self.base, self.base,
        generate_from_members(self.members, "put", "\t"))

    def to_compare(self):
        return \
'''static inline int compare_with_user_STRUCT_%s
\t(%s __user *uside, %s *kside){

\treturn %s;
}''' % (self.name, self.base, self.base,
        generate_from_members(self.members, "compare", "\t || "))

    def to_clean(self):
        return \
'''static inline void clean_STRUCT_%s(%s *kside){
\t%s
}''' % (self.name, self.base, 
        generate_from_members(self.members, "clean", "\t"))

    def gen_struct_helper(self):
        code = \
'''%s
%s
%s
%s''' % (self.to_get(), 
        self.to_put(),
        self.to_compare(),
        self.to_clean())

        return self.wrapper(code)

class Syscall:

    def __init__(self, name, cond=None, ref=None,
            pre=None, post=None,
            lpre=None, lpost=None,
            fpre=None, fpost=None,
            exe=None, lexe=None, fexe=None,
            includes=[]):

        self.name = name

        self.cond =cond
        self.ref = ref

        self.pre = pre
        self.post = post
        self.lpre = lpre
        self.lpost = lpost
        self.fpre = fpre
        self.fpost = fpost

        self.exe = exe
        self.lexe = lexe
        self.fexe = fexe

        self.includes = includes 

        self.symbols = []
        self.structs = []
        self.params = []
        self.positions = []
        self.siblings = []

    def add_param(self, param):
        param.syscall = self
        self.params.append(param)
        self.positions.insert(param.pos, param)

    def add_symbol(self, symbol):
        symbol.syscalls.append(self)
        self.symbols.append(symbol)

    def add_struct(self, struct):
        struct.syscalls.append(self)
        self.structs.append(struct)

    def add_sibling(self, sibling):
        self.siblings.append(sibling)

    def wrapper(self, stmt):
        return \
'''#ifdef __NR_%s
%s
#endif''' % \
        (self.name, stmt)

    def build_sysname(self):
        return self.name

    def build_vardef(self):
        return generate_from_members(self.params, "vardef", "")

    def gen_checkin(self):
        if self.cond is not None:
            code = generate_from_members(self.params, "checkin", "\t")
            
            if code is None or len(code) == 0:
                return None
            
            return \
'''if(%s){
\t%s
}''' % (self.cond, code) 

        else:
            return generate_from_members(self.params, "checkin", "")

    def gen_compare(self):
        if self.cond is not None:
            code = generate_from_members(self.params, "compare", "\t")

            if code is None or len(code) == 0:
                return None

            return \
'''if(%s){
\t%s
}''' % (self.cond, code) 
        
        else:
            return generate_from_members(self.params, "compare", "")

    def gen_turnin(self):
        if self.cond is not None:
            code = generate_from_members(self.params, "turnin", "\t")

            if code is None or len(code) == 0:
                return None

            return \
'''if(%s){
\t%s
}''' % (self.cond, code)

        else:
            return generate_from_members(self.params, "turnin", "")

    def gen_fetch(self):
        if self.cond is not None:
            code = generate_from_members(self.params, "fetch", "\t")

            if code is None or len(code) == 0:
                return None

            return \
'''if(%s){
\t%s
}''' % (self.cond, code) 

        else:
            return generate_from_members(self.params, "fetch", "")

    def gen_pclean(self):
        if self.cond is not None:
            code = generate_from_members(self.params, "pclean", "\t")

            if code is None or len(code) == 0:
                return None

            return \
'''if(%s){
\t%s
}''' % (self.cond, code)

        else:
            return generate_from_members(self.params, "pclean", "")

    def gen_rclean(self):
        if self.cond is not None:
            code = generate_from_members(self.params, "rclean", "\t")

            if code is None or len(code) == 0:
                return None

            return \
'''if(%s){
\t%s
}''' % (self.cond, code)

        else:
            return generate_from_members(self.params, "rclean", "")

    def build_checkin(self):
        if len(self.siblings) != 0:
            return generate_from_members(self.siblings, "checkin", "")
        else:
            return self.gen_checkin()

    def build_compare(self):
        if len(self.siblings) != 0:
            return generate_from_members(self.siblings, "compare", "")
        else:
            return self.gen_compare()

    def build_turnin(self):
        if len(self.siblings) != 0:
            return generate_from_members(self.siblings, "turnin", "")
        else:
            return self.gen_turnin()

    def build_fetch(self):
        if len(self.siblings) != 0:
            return generate_from_members(self.siblings, "fetch", "")
        else:
            return self.gen_fetch()

    def build_pclean(self):
        if len(self.siblings) != 0:
            return generate_from_members(self.siblings, "pclean", "")
        else:
            return self.gen_pclean()

    def build_rclean(self):
        if len(self.siblings) != 0:
            return generate_from_members(self.siblings, "rclean", "")
        else:
            return self.gen_rclean()

    def to_param_defs(self):
        stmts = []
        for param in self.positions:
            stmt = param.to_def()
            if stmt is not None and len(stmt) > 0:
                stmts.append(stmt)

        if len(stmts) > 0:
            return ", \n\t".join(stmts)
        else:
            return "void"

    def to_param_uses(self):
        stmts = []
        for param in self.positions:
            stmt = param.to_use()
            if stmt is not None and len(stmt) > 0:
                stmts.append(stmt)

        if len(stmts) > 0:
            return ", ".join(stmts)
        else:
            return ""

    def build_def_ref_syscall(self):
        return "asmlinkage long (*ref_SYS_%s) \n\t(%s)" % \
                (self.name, self.to_param_defs())

    def build_def_new_syscall(self):
        return "asmlinkage long new_SYS_%s \n\t(%s)" % \
                (self.name, self.to_param_defs())

    def build_use_ref_syscall(self):
        if self.ref is not None:
            return self.ref

        return "ref_SYS_%s(%s)" % \
                (self.name, self.to_param_uses())
 
    def build_ref(self):
        if self.ref is not None:
            return self.ref

        return "return %s;" % \
                (self.build_use_ref_syscall())

    def build_exe(self):
        if self.exe is not None:
            return self.exe

        return "retval = %s;" % \
                (self.build_use_ref_syscall())

    def build_lexe(self):
        if self.lexe is not None:
            return self.lexe

        return ""

    def build_fexe(self):
        if self.fexe is not None:
            return self.fexe

        return ""

    def build_pre(self):
        if self.pre is not None:
            return self.pre

        return ""

    def build_post(self):
        if self.post is not None:
            return self.post

        return ""
                                                                                
    def build_lpre(self):
        if self.lpre is not None:
            return self.lpre

        return ""

    def build_lpost(self):
        if self.lpost is not None:
            return self.lpost

        return ""
                                                                                
    def build_fpre(self):
        if self.fpre is not None:
            return self.fpre

        return ""

    def build_fpost(self):
        if self.fpost is not None:
            return self.fpost

        return ""

    def build_struct_helper(self):
        return generate_from_members(self.structs, "struct_helper", "")

    def gen_variable(self):
        stmt = "%s;" % self.build_def_ref_syscall()
        return self.wrapper(stmt)

    def gen_hook(self):
        stmt = "HOOK_SYS(%s);" % self.name
        return self.wrapper(stmt)

    def gen_unhook(self):
        stmt = "UNHOOK_SYS(%s);" % self.name
        return self.wrapper(stmt)

    def gen_header(self):
        stmt = \
'''extern %s;
%s;''' % \
        (self.build_def_ref_syscall(),
                self.build_def_new_syscall())

        return self.wrapper(stmt)

    def gen_body(self):
        stmt = generate_from_template(self, SYSCALL_TEMPLATE)
        return self.wrapper(stmt)


class Group:

    def __init__(self, name):
        self.name = name
        self.syscalls = []

    def add_syscall(self, syscall):
        self.syscalls.append(syscall)

    def build_group(self):
        return self.name

    def build_syscall_includes(self):
        includes = set()
        for syscall in self.syscalls:
            for struct in syscall.structs:
                for include in struct.includes:
                    includes.add(include)
            for include in syscall.includes:
                includes.add(include)

        includes = sorted(includes)
        stmts = []
        for include in includes:
            stmts.append("#include <%s>" % include)

        return "\n".join(stmts)

    def build_struct_helpers(self):
        structs = set()
        for syscall in self.syscalls:
            for struct in syscall.structs:
                structs.add(struct)

        structs = sorted(structs)
        return generate_from_members(structs, "struct_helper", "")

    def build_syscall_headers(self):
        return generate_from_members(self.syscalls, "header", "")

    def build_syscall_bodies(self):
        return generate_from_members(self.syscalls, "body", "")
 
    def build_syscall_variables(self):
        stmts = []
        stmts.append("\n/* group %s */" % self.name)
        for syscall in self.syscalls:
            stmts.append("%s" % syscall.gen_variable())

        return "\n".join(stmts)

    def build_syscall_hooks(self):
        stmts = []
        stmts.append("\n/* group %s */" % self.name)
        for syscall in self.syscalls:
            stmts.append("%s" % syscall.gen_hook())

        return "\n".join(stmts)

    def build_syscall_unhooks(self):
        stmts = []
        stmts.append("\n/* group %s */" % self.name)
        for syscall in self.syscalls:
            stmts.append("%s" % syscall.gen_unhook())

        return "\n".join(stmts)

    def build_group_include(self):
        return "#include \"stub_%s.h\"" % self.name

    def output_header(self):
        fname = "%s/stub_%s.h" % (SOURCE, self.name)
        with open(fname, "w+") as f:
            f.write(generate_from_template(self, GROUP_H_TEMPLATE))

    def output_source(self):
        fname = "%s/stub_%s.c" % (SOURCE, self.name)
        with open(fname, "w+") as f:
            f.write(generate_from_template(self, GROPU_C_TEMPLATE))

    def output_all(self):
        self.output_header()
        self.output_source()
