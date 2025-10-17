from typing import List

def ensure_operators(ops: List[str]):
    ops = [o.strip() for o in ops if o and o.strip()]
    if len(ops) != 3:
        raise ValueError("Wymaganych jest dokładnie trzech operatorów.")
    if len(set(ops)) != 3:
        raise ValueError("Nazwy trzech operatorów muszą być unikalne.")
    return ops
