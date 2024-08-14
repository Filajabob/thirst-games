class Player:
    def __init__(self, given_name: str, surname: str, stats: dict, age: int):
        self.given_name = given_name
        self.surname = surname
        self.stats = stats
        self.age = age

        self.full_name = f"{self.given_name} {self.surname}"

    def serialize(self):
        return {
            "given_name": self.given_name,
            "surname": self.surname,
            "stats": self.stats,
            "age": self.age
        }
