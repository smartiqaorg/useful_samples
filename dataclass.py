from dataclasses import dataclass
from typing import Literal
import uuid


# Default class definition

# class Fruit:
#
#     def __init__(self, name, id=uuid.uuid4(), color='Green'):
#         self.name = name
#         self.id = id
#         self.color = color

@dataclass
class Fruit:
    name: str
    id: int = uuid.uuid4()
    color: Literal['Green', 'Red', 'Orange', 'Blue', 'Yellow', 'Black', 'White'] = 'Green'


# Тест
fruits = [
    Fruit(name='Peach', id=1, color='Orange'),
    Fruit(name='Orange', id=2, color='Orange'),
    Fruit(name='Banana', color='Yellow'),
    Fruit(name='Apple')
]

for fruit in fruits:
    print(fruit)
