"""
Задача 3. Пиццерия
Объектно-ориентированная модель - пиццерия. В пиццерию приходит клиент и выбирает пиццу: Пепперони или Маргариту. Также выбирает размер пиццы: Small (25см), Medium (30см), Large(35 см).

------------
Классы
------------
(1) Класс Pizza
Содержит в себе информацию о:
 1) Доступных размерах пиццы
 2) Ингредиентах
 3) Стадии приготовления

Действия:
 1) Пиццу можно приготовить

(2) Класс Pepperoni
Содержит в себе информацию об ингредиентах для Пепперони пиццы: Салями и Сыр

(3) Класс Margarita
Содержит в себе информацию об ингредиентах для Пепперони пиццы: Томаты и Сыр

(4) Класс Worker
 Содержит в себе информацию о:
1) Наличии заказа
2) Количестве денег в кассе

Работник может:
1) Поприветствовать клиента
2) Получить заказ
3) Получить деньги за заказ
4) Обработать заказ

(5) Класс Client
Содержит в себе информацию о:
1) Имени клиента
2) Количестве доступных денег
3) Наличии пиццы для обеда

Действия:
1) Клиент может выбрать Пепперони или Маргариту
2) Клиент может выбрать размер пиццы
3) Клиент может заплатить за пиццу деньги
4) Клиент может забрать свою пиццу

-------------
Задание
-------------
Класс Pizza
1. Создайте класс Pizza
2. Создайте статические поля для хранения данных о доступных размерах пиццы(SMALL, MEDIUM, LARGE), возможной степени готовности (COOKING, READY), доступных видах пиццы (PEPPERONI, MARGARITA)
3. Создайте функцию инициализатор __init__(), которая будет принимать в качестве входных параметров список ингредиентов и размер пиццы. Внутри нее создайте динамические поля, которые будут хранить информацию о размере пиццы, ингредиентах, степени ее готовности.
4. Создайте метод cook(), который будет изменять степень готовности пиццы.

Классы Pepperoni и Margarita
1. Создайте класс Pepperoni на основе класса Pizza
2. Создайте функцию инициализатор __init__(), которая будет принимать в качестве входного параметра размер пиццы. Также она будет вызывать инициализатор родительского класса Pizza и передавать ему 1) размер пиццы и 2) список ингредиентов ['Salami', 'Cheese']
3. Аналогично создайте класс Margarita и функцию __init__(). Ингредиенты: ['Tomato', 'Cheese']

Класс Worker
1. Создайте класс Worker
2. Создайте метод __init__(), внутри которого будут инициализироваться 2 динамических поля: order (публичное поле, отвечает на содержимое заказа) и __cash (приватное поле, отвечает за количество денежных средств в кассе).
3. Создайте статический метод greet_client(), который будет по переданному имени приветствовать клиента - выводить приветствие на печать.
4. Создайте метод get_order(), который будет принимать тип пиццы и ее размер и на их основе создавать объект соответствующего класса: Pepperoni или Margarita с конкретным размером пиццы.
5. Создайте метод get_money(), который будет принимать оплату за пиццу и соответствующим образом увеличивать количество денег в кассе.
6. Создайте метод process_order(), который будет изменять степень готовности нашей пиццы (вызовет для нее метод cook() ) и вернет готовый объект пиццы

Класс Client
1. Создайте класс Client
2. Создайте статическое поле для хранения имени клиента по умолчанию.
3. Создайте функцию инициализатор __init__(), которая будет принимать в качестве входных параметров количество денег у клиента и его имя(задействуйте для него имя клиента по умолчанию). Внутри метода создайте три динамических поля: имя клиента (публичное поле), количество денег (приватное поле), сама пицца (публичное поле, на этапе инициализации равняется None)
4. Создайте статический метод choose_margarita_pizza(), который будет возвращать тип пиццы Маргарита (возможные типы были созданы в классе Pizza в статических полях PEPPERONI и MARGARITA)
5. Создайте аналогичный статический метод choose_pepperoni_pizza()
6. Создайте статический метод choose_small_size(), который также возвращать размер пиццы (возможные размеры были созданы в классе Pizza в статических полях SMALL, MEDIUM и LARGE)
7. Создайте по аналогии методы choose_medium_size() и choose_large_size()
8.Создайте метод pay_money(), который будет уменьшать количество денег у клиента на стоимость пиццы (стоимость пиццы передается в качестве входного параметра)
9. Создайте метод get_pizza(), который будет принимать объект Пиццы и присваивать его соответствующему полю клиента.

----------
Тесты
----------
После реализации функционала описанных классов у вас должна работать следующая последовательность действий:
worker = Worker()
ivan = Client(30, 'Ivan')
Worker.greet_client(ivan.name)
pizza_type = Client.choose_pepperoni_pizza()
pizza_size = Client.choose_large_size()
worker.get_order(pizza_type, pizza_size)
ivan.pay_money(10)
worker.get_money(10)
pizza = worker.process_order()
ivan.get_pizza(pizza)
"""


class Pizza:
    SMALL = 25
    MEDIUM = 30
    LARGE = 35

    COOKING = 0
    READY = 1

    PEPPERONI = 'Pepperoni'
    MARGARITA = 'Margarita'

    def __init__(self, ingredients, size=MEDIUM):
        self.size = size
        self.ingredients = ingredients
        self.state = None

    def cook(self):
        self.state = 0
        print('Pizza is being cooked...')
        self.state = 1
        print('Pizza is ready!')


class Pepperoni(Pizza):
    def __init__(self, size):
        ingredients = ['Salami', 'Cheese']
        super().__init__(ingredients, size)


class Margarita(Pizza):
    def __init__(self, size):
        ingredients = ['Tomato', 'Cheese']
        super().__init__(ingredients, size)


class Worker:
    def __init__(self):
        self.order = None
        self.__cash = 0

    @staticmethod
    def greet_client(name):
        print(f'Hello, {name}! What is your order?')

    def get_order(self, pizza_type, pizza_size):
        pizza = None
        if pizza_type == Pizza.PEPPERONI:
            pizza = Pepperoni(pizza_size)
        elif pizza_type == Pizza.MARGARITA:
            pizza = Margarita(pizza_size)
        else:
            print('No such pizza type!')

        self.order = pizza
        print('Your order is accepted')

    def get_money(self, money):
        self.__cash += money
        print(f'Got {money}$')

    def process_order(self):
        self.order.cook()
        return self.order


class Client:
    default_name = 'No name'

    def __init__(self, money, name=default_name):
        self.name = name
        self.__money = money
        self.pizza = None

    @staticmethod
    def choose_pepperoni_pizza():
        return Pizza.PEPPERONI

    @staticmethod
    def choose_margarita_pizza():
        return Pizza.MARGARITA

    @staticmethod
    def choose_small_size():
        return Pizza.SMALL

    @staticmethod
    def choose_medium_size():
        return Pizza.MEDIUM

    @staticmethod
    def choose_large_size():
        return Pizza.LARGE

    def pay_money(self, price):
        self.__money -= price

    def get_pizza(self, pizza):
        self.pizza = pizza


# Tests
worker = Worker()
ivan = Client(30, 'Ivan')

Worker.greet_client(ivan.name)

pizza_type = Client.choose_pepperoni_pizza()
pizza_size = Client.choose_large_size()

worker.get_order(pizza_type, pizza_size)
ivan.pay_money(10)
worker.get_money(10)
pizza = worker.process_order()
ivan.get_pizza(pizza)
