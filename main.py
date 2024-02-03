from sympy.abc import *
from sympy import *
from os import system
from sys import exit


class MathToolSet:
    def _welcome(self):
        print("欢迎使用QAQ0428的数学工具(\\back返回, \\quit退出)")
        for i, j in self.SELECTIONS.items():
            print(f"{i}.{j}\t", end="")
            # 每两条换行
            if i % 2 == 0:
                print()
        print()

    def _ask(self, prompt: str, filter, fun):
        # 循环输入一个值, prompt是提示词, filter用于判断输入合法性的条件, fun为合法时执行的函数
        inp = input(prompt)
        while (inp in ("\\quit", "\\back")) or (not filter(inp)):
            self._quit_or_exit(inp)
            self._cls()
            inp = input(prompt)
        fun(inp)

    def _ask_with_converter(self, prompt: str, filter, fun, converter):
        self._cls()
        inp = converter(input(prompt))

        while (not filter(inp)) or (inp in ("\\quit", "\\back")):
            self._quit_or_exit(inp)
            self._cls()
            inp = converter(input(prompt))
        self._cls()
        fun(inp)

    def _ask_for_launching(self):
        self._cls()
        self._ask("选择一个选项的序号以进行下一步: \n",
                  (lambda x: x in map(str, self.SELECTIONS)),
                  self._launch
                  )

    def _is_valid_formula(self, expr: str) -> bool:
        res = None
        try:
            res = eval(expr)
        except:
            return False
        return res is not None and isinstance(res, (int, float, Basic))

    def get_solutions(self, eq: str | Eq) -> list[float | int | Basic] | dict:
        # eq: str 格式: a*x**2 + b*x + c = 0 | y = x $ x, y
        unknowns: list[Symbol] = []
        if isinstance(eq, str):
            parts = eq.split("$")
            if eq in ("\\back", "\\quit"):
                self._quit_or_exit(eq)
            if parts == eq:
                # 不含有$
                eq = self._str_to_formula(eq)
            else:
                # 含有$
                unknowns = map(self._is_valid_symbol, parts[1].split(","))
                if any(map(lambda obj: obj is None, unknowns)):
                    return []
                else:
                    unknowns = list(unknowns)
        try:
            return solve(eq, *unknowns)
        except:
            return []

    def _is_valid_eqs(self, string: str) -> bool:
        def f(str_eq) -> bool:
            eqs = str_eq.split("|")
            if eqs == [str_eq]:
                # 是一个方程
                exprs = str_eq.split("=")
                return (all(map(self._is_valid_formula, exprs))
                        and exprs != [str_eq])  # 说明等号两边都有式子
            else:
                # 是几个方程
                return all(map(self._is_valid_eqs, eqs))
        parts = string.split("$")
        if parts == [string]:
            #说明是不含有$这个符号
            return f(string)
        else:
            #含有$
            return all(map(self._is_valid_symbol, parts[1].split(","))) and f(parts[0])
    def _is_valid_symbol(self, sym: str) -> Symbol | bool:
        #如果sym是Symbol则返回它
        try:
            sym = eval(sym)
            if isinstance(sym, Symbol):
                return sym
            else:
                return False
        except:
            return False
    def _cls(self):
        system("cls")
        self._welcome()

    def _launch(self, s):
        self.FUNCTIONS[self.SELECTIONS[int(s)]]()

    def _print_formulas(self, formulas: Basic | str | Eq | list[Eq]):
        if isinstance(formulas, list) and all(map(lambda obj: isinstance(obj, Eq), formulas)):
            # 是方程组
            is_eq_set = True
        else:
            # 是字符串或方程或代数式, 不是方程组
            is_eq_set = False
            if isinstance(formulas, str):
                formulas = self._str_to_formula(formulas)
        print("--" * 10, "\n")
        if is_eq_set:
            # 是方程组
            print(f"Python表达式: {formulas}")
            print("Unicode:")
            for i in formulas:
                print("\t", pretty(i))
            print("LaTeX:")
            for i in formulas:
                print("\t", latex(i))
        else:
            # 是单个方程
            print(
                f"Python表达式: {formulas}\n"
                f"Unicode:\n{pretty(formulas)}\n"
                f"LaTeX: {latex(formulas)}\n")
            print("\n")
        print("--" * 10, "\n")

    def _is_iterable(self, obj):
        try:
            obj.__iter__()
        except:
            return False
        return True

    def _str_to_formula(self, fml: str) -> Basic | Eq | None:
        # fml: str 格式: a*x**2 + b*x + c = 0 | y = x $ x, y
        def str_to_eq(string: str) -> Eq | None:
            # string: str 格式: a*x**2 + b*x + c = 0 | y = x $ x, y
            if self._is_valid_eqs(string):
                parts = string.split("$")
                if parts == string:
                    # 不含有$
                    return Eq(*list(map(self._str_to_formula, string.split("="))))
                else:
                    # 含有$
                    return Eq(*list(map(self._str_to_formula, parts[0].split("="))))
            return

        if self._is_valid_formula(fml):
            # 是代数式
            return eval(fml)
        elif self._is_valid_eqs(fml):
            # 是方程(组)
            return str_to_eq(fml)
        else:
            # 啥也不是
            return
    def _print_formulas_and_convert(self, formulas: Basic | str | Eq | list[Eq], converter: callable):
        #todo 要修改
        unknowns = []
        if isinstance(formulas, str):
            eqs = formulas.split("|")
            parts = formulas.split("$")
            if parts != [formulas]:
                unknowns = list(map(self._is_valid_symbol, parts[1].split(",")))
            if eqs == [formulas]:
                # formulas 是一个方程或式子
                formulas = self._str_to_formula(formulas)
            else:
                # formulas是几个方程
                formulas = list(map(self._str_to_formula, eqs))
        if converter == self.get_solutions and not any(map(lambda obj: obj is None, unknowns)):
            # 针对解方程 指定未知数的情况
            result = solve(formulas, *unknowns)
        else:
            # 一般情况
            result = converter(formulas)
        self._cls()
        print("你输入的是:")
        self._print_formulas(formulas)
        print("结果: ")
        if self._is_iterable(result):
            for i in result:
                if isinstance(result, dict):
                    self._print_formulas(Eq(i, result[i]))
                else:
                    self._print_formulas(i)
        else:
            self._print_formulas(result)

    def usables(self):
        print("标识符\t\t\t\t\t\t作用")
        for i in self.USABLES:
            print(f"{i}\t\t\t\t\t\t{self.USABLES[i]}")
        print('欲了解更多, 请查阅SymPy库相关资料, 然后在"交互环境"里使用.')
        print("注:\n1.方程求解")
        print("\t一元方程输入格式: x*(x+1)=240")
        print("\t含参方程输入格式: a*x**2 + b*x + c = 0 $ x\t($后面列出未知数.以半角逗号分割)")
        print("\t方程组输入格式: a*x + y = 1 | y = 0 $ x, y")
        system("pause")

    def solve(self):
        self._cls()
        while 1:
            self._ask("请输入一个方程\n", self._is_valid_eqs,
                      lambda fml: self._print_formulas_and_convert(fml, self.get_solutions))

    def expand(self):
        self._cls()
        while 1:
            self._ask("输入一个式子:\n", self._is_valid_formula,
                      lambda fml: self._print_formulas_and_convert(self._str_to_formula(fml), expand))

    def factor(self):
        self._cls()
        while 1:
            self._ask("输入一个式子:\n", self._is_valid_formula,
                          lambda fml: self._print_formulas_and_convert(self._str_to_formula(fml), factor))

    def _quit_or_exit(self, s):
        if s == "\\back":
            self._cls()
            while 1:
                self._ask_for_launching()
        elif s == "\\quit":
            print("按下回车以退出")
            system("pause")
            exit(0)
    def _is_valid_function(self, f: str):
        try:
            self._cls()
            return plot(self._str_to_formula(f))
        except:
            return False
    def funcdraw(self):
        self._cls()
        while 1:
            self._ask("请输入一个式子\n", self._is_valid_function, lambda obj: None)

    def simplify(self):
        self._cls()
        while 1:
            self._ask("输入一个式子:\n", self._is_valid_formula,
                      lambda fml: self._print_formulas_and_convert(self._str_to_formula(fml), simplify))

    def interactive(self):
        print("python 3.10")
        while 1:
            inp = input(">>> ")
            self._quit_or_exit(inp)
            try:
                exec(inp)
            except Exception as e:
                print(e)
    def _is_valid_int(self, number: str):
        try:
            return isinstance(eval(number), int)
        except:
            return False
    def primefactors(self):
        self._cls()
        while 1:
            self._ask("输入一个整数:\n", self._is_valid_int,
                      lambda fml: self._print_formulas_and_convert(self._str_to_formula(fml), primefactors))

    def __init__(self):
        self._vars = {}
        # 菜单选项与方法之间的对应
        self.FUNCTIONS = {
            "方程求解": self.solve,
            "因式分解": self.factor,
            "函数图像": self.funcdraw,
            "式子化简": self.simplify,
            "式子展开": self.expand,
            "分解因数": self.primefactors,
            "交互环境": self.interactive,
            "所有可用": self.usables

        }
        # 序号与选项字符串之间的对应
        self.SELECTIONS = dict(enumerate(self.FUNCTIONS, start=1))
        self.USABLES = {
            "字母a-z": "代数式中的字母",
            "希腊字母的英文拼写": "代数式中的字母(请用lamda表示lambda λ)",
            "oo": "无穷(两个o)",
            "pi": "圆周率",
            "E": "自然常数(2.718......)",
            "I": "虚数单位(I^2 = -1)",
            "floor(a)": "a向下取整的结果",
            "round(a)": "a四舍五入的结果",
            "round(a, b)": "将a四舍五入到个位的后b位(b可为负)",
            "factorial(a)": "a的阶乘a!",
            "lcm(a, b)": "a, b的最小公倍数",
            "gcd(a, b)": "a, b的最大公倍数",
            "Mod(a, b)": "a模b的结果",
            "A.evalf(n=a)": "代数式A的近似值(最终结果一共有a位)",
            "abs(a)": "|a|",
            "Rational(a, b)": "a/b",
            "log(a, b)": "以b为底a的对数",
            "ln(a)": "以e为底a的对数",
            "sqrt(a)": "a的算术平方根",
            "root(a, b)": "a的b次方根",
            "a ** b": "a^b a的b次方",
            "rad(a)": "将a°转换成a弧度",
            "三角函数名(a)": "弧度a的三角函数值 (sin, cos, tan等)"
        }
        while 1:
            self._ask_for_launching()


def main():
    MathToolSet()


if __name__ == '__main__':
    main()

