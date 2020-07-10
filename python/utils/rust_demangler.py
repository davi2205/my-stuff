
import re

#
#       Rust symbol demangler
#
#       Author: Davi Villalva
#         Year: 2020
#         Desc: Name demangling utility
#
#
#       Example:
#
#       # This should print "std::rt::lang_start::_{{closure}}::h7d048bba93702107"
#       print(demangle("__ZN3std2rt10lang_start28_$u7b$$u7b$closure$u7d$$u7d$17h7d048bba93702107E"))
#
#       _input            -> the input mangled symbol
#       remove_underscore -> if True, any left underscore will be removed 
#                            (kind of useless, maybe I'll remove this later)
#

def demangle(_input: str, remove_underscore: bool=False) -> str:
    head_pat = re.compile("_*ZN")
    num_pat = re.compile("[0-9]+")
    asc_pat = re.compile("\\$([A-Z]+)\\$")
    uni_pat = re.compile("\\$u([0-9a-fA-F]+)\\$")

    asc_tbl = {
        "LT": "<",
        "GT": ">",
        "LP": "(",
        "RP": ")",
        "SP": "@",
        "C": ",",
    }

    cur = _input

    def is_header_valid() -> bool:
        nonlocal cur
        nonlocal head_pat

        m = head_pat.match(cur)

        if m:
            cur = cur[m.end():]
            return True
        else:
            return False

    def read_count() -> int:
        nonlocal cur
        nonlocal num_pat

        m = num_pat.match(cur)

        if m:
            num = int(m.group())
            cur = cur[m.end():]
            return num
        else:
            return -1

    def read_nchars(count: int) -> str:
        nonlocal cur

        ret = cur[:count]

        if len(ret) == count:
            cur = cur[count:]
            return ret
        else:
            return None

    def treat_special_chars(string: str) -> str:
        nonlocal asc_pat
        nonlocal asc_tbl
        nonlocal uni_pat
        
        def asc_repl(m):
            nonlocal asc_tbl
            return asc_tbl.get(m.group(1), "?")

        def uni_repl(m):
            return chr(int(m.group(1), base=16))
    
        string = asc_pat.sub(asc_repl, string)
        string = uni_pat.sub(uni_repl, string)
        string = string.replace("..", "::")

        return string

    if not is_header_valid():
        return None

    count = read_count()
    output = []

    if count == -1:
        return None

    while count != -1:
        raw_name = read_nchars(count)

        if raw_name is None:
            return None

        output.append(treat_special_chars(raw_name))
        count = read_count()

    output = "::".join(output)

    return output if not remove_underscore else output.lstrip("_")
