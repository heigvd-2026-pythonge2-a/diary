"""
>>> donald = Duck('Trump')
>>> donald.sleep()
Trump is sleeping... ZZZzzzzzZZZzzz
```

1. Définissez la classe avec `class Duck:`.
2. Dans `__init__(self, name)`, stockez le nom : `self.name = name`.
3. Chaque méthode prend `self` en premier paramètre, ce qui permet d'accéder à `self.name`.
4. Utilisez une f-string pour l'affichage : `print(f"{self.name} is sleeping...")`.
5. Pour tester, placez votre code de démonstration sous `if __name__ == "__main__":`.
"""

class Duck:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Duck({self.name})"

    __repr__ = __str__

    def sleep(self):
        print(f"{self.name} is sleeping... ZZZzzzZZZ")

if __name__ == "__main__":
    donald = Duck('Trump')
    donald.sleep()