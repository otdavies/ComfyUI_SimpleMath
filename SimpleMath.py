import ast
import math
import operator as op
import random

operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Pow: op.pow,
    # ast.BitXor: op.xor,
    # ast.USub: op.neg,
    ast.Mod: op.mod,
}


class SimpleMath:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "optional": {
                "a": ("INT,FLOAT", {"default": 0.0, "step": 0.1}),
                "b": ("INT,FLOAT", {"default": 0.0, "step": 0.1}),
            },
            "required": {
                "value": ("STRING", {"multiline": False, "default": ""}),
            },
        }

    RETURN_TYPES = ("INT", "FLOAT", )
    FUNCTION = "do_math"
    CATEGORY = "utils"

    def do_math(self, value, a=0.0, b=0.0):
        def eval_(node):
            if isinstance(node, ast.Num):  # number
                return node.n
            elif isinstance(node, ast.Name):  # variable
                if node.id == "a":
                    return a
                if node.id == "b":
                    return b
            elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
                return operators[type(node.op)](eval_(node.left), eval_(node.right))
            elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
                return operators[type(node.op)](eval_(node.operand))
            else:
                return 0

        result = eval_(ast.parse(value, mode='eval').body)

        if math.isnan(result):
            result = 0.0

        return (round(result), result, )


class RandomRange:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "min_value": ("FLOAT", {"default": 0.0, "min": -1000000.0, "max": 1000000.0, "step": 0.1}),
                "max_value": ("FLOAT", {"default": 1.0, "min": -1000000.0, "max": 1000000.0, "step": 0.1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("INT", "FLOAT",)
    FUNCTION = "generate_random"
    CATEGORY = "utils"

    def generate_random(self, min_value, max_value, seed):
        random.seed(seed)
        result = random.uniform(min_value, max_value)
        return (round(result), result,)


class SixRandoms:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT", "FLOAT",)
    FUNCTION = "generate_six_randoms"
    CATEGORY = "utils"

    def generate_six_randoms(self, seed):
        random.seed(seed)

        # Generate 6 random numbers that sum to 1, with no value exceeding 0.5
        max_attempts = 100
        for _ in range(max_attempts):
            values = [random.random() for _ in range(6)]
            total = sum(values)
            normalized = [v / total for v in values]

            if all(v <= 0.5 for v in normalized):
                return tuple(normalized)

        # Fallback: create a balanced set that meets requirements
        base_values = [1/6] * 6
        for i in range(6):
            adjustment = random.uniform(-0.05, 0.05)
            base_values[i] += adjustment

        base_values = [max(v, 0.01) for v in base_values]
        total = sum(base_values)
        result = [v / total for v in base_values]

        return tuple(result)

# taken from https://github.com/pythongosssss/ComfyUI-Custom-Scripts


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any = AnyType("*")


class SimpleMathDebug:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": (any, {}),
            },
            "optional": {
                "prefix": ("STRING", {"multiline": False, "default": "Value:"})
            }
        }

    RETURN_TYPES = ()

    FUNCTION = "debug_print"

    CATEGORY = "utils"

    OUTPUT_NODE = True

    def debug_print(self, value, prefix):
        print(f"\033[96m{prefix} {value}\033[0m")

        return (None,)


NODE_CLASS_MAPPINGS = {
    "SimpleMath": SimpleMath,
    "SimpleMathDebug": SimpleMathDebug,
    "RandomRange": RandomRange,
    "SixRandoms": SixRandoms
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SimpleMath": "Math op",
    "SimpleMathDebug": "Math debug",
    "RandomRange": "Random Range",
    "SixRandoms": "Six Random Values"
}
