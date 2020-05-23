import string
import traceback


class Tokens:
    def __init__(self, string):
        self.tokens = list(string.replace(' ', ''))
        self._index = 0

    def check_end(self):
        """Проверить, есть ли следующий токен"""
        if self._index < len(self.tokens):
            return False
        return True

    def current(self):
        """Получить текущий токен"""
        if not self.check_end():
            return self.tokens[self._index]
        return None

    def skip(self):
        """Пропустить следующий токен"""
        if not self.check_end():
            self._index += 1
            return True
        return False

    def tokens_str(self):
        return ''.join(self.tokens[self._index:])


class StringParser:
    def __init__(self, debug_print=False):
        self.tokens = None
        self.string = None
        self.debug_print = debug_print

    def _debug_print(self, *args, **kwargs):
        if self.debug_print:
            print(str(traceback.extract_stack(None, 2)[0][2]).upper(), *args, *kwargs)

    def check_string(self, input_string):
        self._debug_print('Input string:', input_string)
        self.string = input_string
        self.tokens = Tokens(input_string)
        result = self.block()
        self._debug_print(result)
        return result

    def block(self):
        """ BLOCK -> { OP_LIST } """
        self._debug_print(self.tokens.tokens_str())
        if self.brackets(self.tokens.current()):
            if self.tokens.skip() and self.op_list() and self.brackets(self.tokens.current()):
                # Здесь выражение должно закончиться
                if self.tokens.skip() and self.tokens.check_end():
                    return True
        return False

    def op_list(self):
        """OP_LIST -> OP OP_LIST'"""
        self._debug_print(self.tokens.tokens_str())
        if self.op() and self.op_list_hatch():
            return True
        return False

    def op_list_hatch(self):
        """OP_LIST' -> ; OP OP_LIST' | eps"""
        self._debug_print(self.tokens.tokens_str())
        if self.semicolon(self.tokens.current()):
            if self.tokens.skip() and self.op() and self.op_list_hatch():
                return True
            return False
        return True

    def op(self):
        """OP -> NAME = EXPR"""
        self._debug_print(self.tokens.tokens_str())
        if self.name(self.tokens.current()) and self.tokens.skip():
            if self.assign(self.tokens.current()) and self.tokens.skip() and self.expr():
                return True
        return False

    def expr(self):
        """EXPR -> AR_EXPR REL_OP AR_EXPR"""
        self._debug_print(self.tokens.tokens_str())
        if self.ar_expr() and self.rel_op(self.tokens.current()):
            if self.tokens.skip() and self.ar_expr():
                return True
        return False

    def ar_expr(self):
        """AR_EXPR -> TERM AR_EXPR' | ADD_OP TERM AR_EXPR'"""
        self._debug_print(self.tokens.tokens_str())
        if self.add_op(self.tokens.current()):
            if self.tokens.skip() and self.term() and self.ar_expr_hatch():
                return True
        elif self.term() and self.ar_expr_hatch():
            return True
        return False

    def ar_expr_hatch(self):
        """AR_EXPR' -> ADD_OP TERM AR_EXPR' | eps"""
        self._debug_print(self.tokens.tokens_str())
        if self.add_op(self.tokens.current()):
            if self.tokens.skip() and self.term() and self.ar_expr_hatch():
                return True
            return False
        return True

    def term(self):
        """TERM -> FACTOR TERM'"""
        self._debug_print(self.tokens.tokens_str())
        if self.factor() and self.term_hatch():
            return True
        return False

    def term_hatch(self):
        """TERM' -> MUL_OP FACTOR TERM' | eps"""
        self._debug_print(self.tokens.tokens_str())
        if self.mul_op(self.tokens.current()):
            if self.tokens.skip() and self.factor() and self.term_hatch():
                return True
            return False
        return True

    def factor(self):
        """FACTOR -> PR_EXPR | FACTOR'"""
        self._debug_print(self.tokens.tokens_str())
        if self.caret(self.tokens.current()) and self.factor_hatch():
            return True
        elif self.pr_expr():
            return True
        return False

    def factor_hatch(self):
        """FACTOR' -> ^ PR_EXPR FACTOR' | eps"""
        self._debug_print(self.tokens.tokens_str())
        if self.caret(self.tokens.current()):
            if self.tokens.skip() and self.pr_expr() and self.factor_hatch():
                return True
            return False
        return True

    def pr_expr(self):
        """PR_EXPR -> NUMBER | NAME | ( AR_EXPR )"""
        self._debug_print(self.tokens.tokens_str())
        if self.number(self.tokens.current()):
            self.tokens.skip()
            return True
        elif self.name(self.tokens.current()):
            self.tokens.skip()
            return True
        elif self.parentheses(self.tokens.current()):
            if self.tokens.skip() and self.ar_expr() and self.parentheses(self.tokens.current()):
                self.tokens.skip()
                return True
        return False

    def caret(self, token):
        """CARET ->^"""
        self._debug_print(token)
        if token == '^':
            return True
        return False

    def semicolon(self, token):
        """SEMICOLON ->;"""
        self._debug_print(token)
        if token == ';':
            return True
        return False

    def assign(self, token):
        """ASSIGN ->="""
        self._debug_print(token)
        if token == '=':
            return True
        return False

    def parentheses(self, token):
        """PARENTHESES ->(|)"""
        self._debug_print(token)
        if token in ['(', ')']:
            return True
        return False

    def brackets(self, token):
        """BRACKETS ->{|}"""
        self._debug_print(token)
        if token in ['{', '}']:
            return True
        return False

    def number(self, token):
        """NUMBER -> 0|1|2...|9"""
        self._debug_print(token)
        if token.isdigit():
            return True
        return False

    def rel_op(self, token):
        """REL_OP -> <|<=|=|>=|>|<> """
        self._debug_print(token)
        if token in ['<', '<=', '=', '>=', '>', '<>']:
            return True
        return False

    def add_op(self, token):
        """ADD_OP -> +|-"""
        self._debug_print(token)
        if token in ['+', '-']:
            return True
        return False

    def mul_op(self, token):
        """MUL_OP -> %|*|/"""
        self._debug_print(token)
        if token in ['%', '*', '/']:
            return True
        return False

    def name(self, token):
        """NAME -> a|b|c|...|z"""
        self._debug_print(token)
        if token in string.ascii_lowercase:
            return True
        return False
