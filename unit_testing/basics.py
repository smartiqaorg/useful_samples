
import pytest
from unittest.mock import MagicMock, patch

# Этот файл можно запустить через pytest - тест test_sample() должен успешно пройти
# ============================= test session starts ==============================
# collecting ... collected 1 item
#
# basics.py::test_sample PASSED                                            [100%]
#
# ============================== 1 passed in 0.06s ===============================

# Общие принципы написания unit-тестов

# Принципы
# 1. Структура теста: Arrange (Подготовка) -> Act (Действие) -> Assert (Проверка)
# 2. Желательно избегать множественных блоков Arrange / Act / Assert в одном тесте
# 3. Также желательно избегать условных операторов -> лучше положить каждую ветвь в отдельный тест
# 4. Секцию Act лучше представить одним вызовом (API должно работать так, чтобы одно действие выполнялось за вызов одного метода)
# 5. Стоит избегать больших секций Assert. Пример: имеем проверки на равенство для болього количества полей возвращаемого объекта.
# Решение: Добавить в тестовый класс дополниьельный метод для сравнения таких полей.
# 6. Договритесь о правилах именования переменных/данных в тестах.
# 7. Используйте фабричные методы для подготовки схожих структур данных для тестов.
# 8. Начинайте тестирование от самого простого метода к более сложному.
#
#
# Стили
# 1. Проверка выходных данных (вызываем метод, проверяем, что его возвращаемое значение равно ожидаемому)
# 2. Проверка состояния (вызываем метод, проверяем состояние тестируемой системы или ее зависисмостей)
# 3. Проверка взаимодействия (вызываем метод, проверяем как/сколько/каким образом происходило взаимодействие с моками)
# Первый стиль довольно простой и мощный. Он больше подходит для чистых функций - то есть функций,
# которые зависят только от входных данных и не имеет побочных эффектов - не меняет внутреннее состояние класса, не бросает исключения).
# Второй стиль довольно сильно завязан на детали реализации, и потому такие тесты хрупкие и объемные.
# Тесты третьего стиля тоже хрупкие и привязаны к имплементации. А так же самые объемные, так как требуют настройки моков.
# Вывод: самые устойчивые к рефакторингу и простые в поддержке - тесты на Проверку выходных данных (первая группа).
# Самые тяжелые по поддержке - тесты на Проверку взаимодействия (третья группа).
#
#
#




class MyClass:

    my_class_field = 'my_class_field'

    def __init__(self):
        self.my_instance_field = 'my_instance_field'

    def my_method(self, my_arg):
        return 'init_return'


def test_sample():

    # Работаем со стандартной библиотекой unittest.mock.
    # Основные используемые классы: Mock, MagicMock, NonCallableMock, NonCallableMagicMock
    # Также существует библиотека pytest-mock, которая по сути представляет собой обертку над unittest.mock.
    # В примерах будем использовать класс MyClass. Обратите внимание, что у него есть:
    # 1) Классовый атрибут - поле my_class_field. Помним, что классовые атрибуты доступны сразу при создании класса.
    # 2) Атрибут экземпляра класса - поле my_instance_field. Помним, что атрибуты экземпляров доступны только после создания экземпляра.
    # 3) Метод экземпляра класса - my_method().

    # [ 1 ] Работа с объектами Mock/MagicMock
    #
    # class Mock(CallableMixin, NonCallableMock):
    #     def __init__(self, spec=None, side_effect=None, return_value=DEFAULT,
    #                  wraps=None, name=None, spec_set=None, parent=None,
    #                  _spec_state=None, _new_name='', _new_parent=None, **kwargs):
    #         ...
    #
    # class MagicMock(MagicMixin, Mock):
    #     ...
    #
    # Основные моменты:
    # 1) Основной класс Mock позволяет создавать мок объекты.
    # 2) Функционал класса MagicMock = функционал класса Mock + возможность мокать Magic методы.
    # 3) Мы будем использовать MagicMock, при этом помним, что его вызовы практически не отличаются от вызова класса Mock.
    # 4) Вызов MagicMock() возвращает объект класса MagicMock. Сам объект тоже может быть вызван (Mocks are callable),
    # при этом возвращаемым значением будет либо сам объект MagicMock, либо значение return_value, если оно было указано при создании.
    #

    # [ 1.1 ] Создание мока (spec)
    # Параметр spec задает спецификацию (описание/источник атрибутов) объекта, который мы хотим создать.
    # При попытке использовать атрибут мока, который не существует в спецификации, будет выброшена AttributeError.
    # Значение параметра spec может быть представлено списком строк, классом или экземпляром класса.
    my_class_attribs = dir(MyClass)  # [... , 'my_class_field', 'my_method']
    my_mock = MagicMock(spec=MyClass)
    # ret = my_mock.my_not_existing_attrib  # Получим AttributeError, так как имеем в спецификации MyClass, а у него нет такого атрибута

    # Мок объект получает атрибуты класса MyClass ('my_class_field' и 'my_method'), но также имеет и свои атрибуты ('assert_any_call' и т д)
    my_mock_attribs = dir(my_mock)
    # [..., 'assert_any_call', 'assert_called', 'assert_called_once', 'assert_called_once_with', 'assert_called_with', 'assert_has_calls',
    # 'assert_not_called', 'attach_mock', 'call_args', 'call_args_list', 'call_count', 'called', 'configure_mock', 'method_calls',
    # 'mock_add_spec', 'mock_calls', 'my_class_field', 'my_method', 'reset_mock', 'return_value', 'side_effect']
    is_instance = isinstance(my_mock, MyClass)  # True

    # Несмотря на то, что у мока есть атрибут my_method, по сути его нет - он вернет нам объект самого мока
    returned_my_method = my_mock.my_method()  # <MagicMock name='mock.my_method()' id='4510823424'>

    # Вывод: мок имеет атрибуты своей спецификации, но по сути эти атрибуты - пустышки, которые нужно заполнять.
    # Если мы не указываем их значения, то вместо значения атрибута возвращается еще один объект мока.

    # [ 1.2 ] Вызов мока (return_value, call_count, mock_calls)
    # my_mock = MagicMock()  # При дальнейшем вызове мока будет возвращаться сам MagicMock object, так как не указан return_value
    my_mock = MagicMock(return_value=5)  # При вызове мока далее будет возвращаться return_value (равное 5)
    ret = my_mock('my_arg1')  # 5
    ret = my_mock('my_arg2')  # 5
    ret = my_mock('my_arg3')  # 5
    calls_count = my_mock.call_count  # 3
    calls_list = my_mock.mock_calls  # [call('my_arg1'), call('my_arg2'), call('my_arg3'), call.__len__()]
    my_mock.my_attrib = 'my_attrib_value'  # Задаем значение атрибута
    my_attrib = my_mock.my_attrib  # 'my_attrib_value'

    # [ 1.3 ] Вызов дополнительного функционала при вызове мока (side_effect)
    my_mock.side_effect = KeyError('My error!')  # Сразу после вызова my_mock будет выброшено исключение
    with pytest.raises(KeyError):  # pytest перехватит ожидаемое исключение и тест пройдет успешно
        my_mock('my_arg3')

    # side_effect также может быть функцией.
    # Она будет вызываться с теми же аргументами, что и мок.
    # Ее возвращаемое значение становится возвращаемым значением мока
    def side_effect(x):
        return x * 2

    my_mock = MagicMock(side_effect=side_effect, return_value='default_return_value')
    two = my_mock(1)  # 2 (не 'default_return_value' !!!)
    hundred = my_mock(50)  # 100

    # Если мы все же хотим возвращать при вызове мока return_value, то надо вернуть его из side_affect()
    my_mock = MagicMock(return_value='default_return_value')
    def side_effect_with_return_value(*args, **kwargs):
        # return DEFAULT  # вариант 1
        return my_mock.return_value  # вариант 1

    my_mock.side_effect = side_effect_with_return_value
    two = my_mock(1)  # 'default_return_value'
    hundred = my_mock(50)  # 'default_return_value'

    # side_affect еще может быть Iterable объектом - с каждым последующим вызовом мока будет возвращаться значение из списка
    my_mock = MagicMock(side_effect=[100, KeyError, 'str'])
    hundred = my_mock()  # 100
    with pytest.raises(KeyError):
        my_mock()  # Исключение KeyError
    string = my_mock()  # 'str'

    # Убираем side_affect
    my_mock.side_effect = None

    # [ 1.4 ] Удаление атрибутов мока
    # Моки создают атрибуты на лету. Это позволяет им притворяться объектами любого типа.
    # Но иногда возникает необходимость удалить атрибут.
    my_mock = MagicMock()
    ret = hasattr(my_mock, 'my_attrib')  # True
    del my_mock.my_attrib
    ret = hasattr(my_mock, 'my_attrib')  # False

    # [ 1.5 ] Проверки (assertions)
    # Проверяем, что метод my_method() был вызван хотя бы 1 раз
    my_mock = MagicMock()
    my_mock.my_method()
    my_mock.my_method.assert_called_once()
    # Проверяем, что метод my_method() был вызван с указанным именованным параметром
    my_mock.my_method(my_arg_name='my_arg_value')
    my_mock.my_method.assert_called_with(my_arg_name='my_arg_value')
    # Аналогичные проверки:
    # assert_called()
    # assert_called_once()
    # assert_called_with(*args, **kwargs)
    # assert_called_once_with(*args, **kwargs)
    # assert_any_call(*args, **kwargs)
    # assert_has_calls(calls, any_order=False)
    # assert_not_called()
    a = 0


    # [ 2 ] Работа с патчами (Patching)
    #
    # class _patch(object):
    #     def patch(
    #         target, new=DEFAULT, spec=None, create=False,
    #         spec_set=None, autospec=None, new_callable=None, *, unsafe=False, **kwargs
    #     ):
    #
    # Основные моменты:
    # 1) Метод patch() может использоваться как декоратор метода/класса или контекстный менеджер.
    # 2) Патч работает только внутри своего скоупа. Например внутри блока with <> as <>, если мы используем его как контекстный менеджер.
    # То есть если вы делаете патч внутри одной фикстуры и затем передаете ее в другую фикстуру - во второй фикстуре патча уже не будет.
    # 3) Вызов patch() возвращает объект MagicMock или AsyncMock.
    # 4) Если patch() используется как декоратор, то созданный мок передается как дополнительный параметр декорируемой функции/класса.
    # 5) Если patch() используется как контекстный менеджер, то созданный мок возвращается контекстным менеджером.
    # 6) Обязательный параметр target представляет собой строку вида 'package.module.ClassName'. Лучше заранее убедиться, что импорт проходит успешно по указанному пути.
    # 7) По сравнению с созданием мока при патчинге добавляется новый параметр autospec.
    # autospec - более прокачанный вариант spec (обратите внимание, что одновременно передаваться они не могут).
    # При передаче autospec=True мок получит спецификацию объекта, который указан в target.
    # Все атрибуты мока также получат соответствующую спецификацию. Аргументы замоканных функций будут проверяться.
    # В какой-то мере можно сказать, что autospec работает рекурсивно.
    # 8) По умолчанию patch() не умеет на лету создавать атрибуты. Но если это необходимо, то можно использовать параметр create=True

    # [ 2.1 ] Создание патча
    # 1) Используем patch() как декоратор - создаем мок и передаем его в функцию как параметр
    # 2) Параметр autospec=True передаст атрибуты класса MyClass создаваемому моку
    # 3) Рабочий экземпляр пропатченного класса MyClass создается во внутренней функции inner_function()
    # Мы патчим класс снаружи, НЕ меняя содержимое inner_function() функции.

    def inner_function():
        my_instance = MyClass()
        ret1 = MyClass.my_class_field  # 'patched_class_field'
        ret2 = my_instance.my_class_field  # 'patched_class_field'
        ret3 = my_instance.my_instance_field  # 'patched_ins_field'
        # Если при создании патча указываем autospec=True и вызовем my_method() без аргумента, то получим TypeError: missing a required argument: 'my_arg'
        # Если при создании патча указываем spec=True и вызовем my_method() без аргумента, то получим 'patched_return' (ошибки не будет)
        # Если при создании патча НЕ указываем spec/autospec и вызовем my_method() аргумента, то получим 'patched_return' (ошибки не будет)
        # ret4 = my_instance.my_method()
        ret4 = my_instance.my_method(my_arg='my_arg')  # 'patched_return'

    @patch('basics.MyClass', autospec=True)
    def my_function(_unused_arg, mock_class):
        mock_class.my_class_field = 'patched_class_field'
        mock_class().my_class_field = 'patched_class_field'
        mock_class().my_instance_field = 'patched_ins_field'
        mock_class().my_method.return_value = 'patched_return'
        inner_function()

    my_function('my_arg')

    # [ 2.2 ] Функция patch.object()
    # patch.object(target, attribute, new=DEFAULT, spec=None, create=False, spec_set=None,
    #              autospec=None, new_callable=None, **kwargs):
    # Создает мок на атрибут (attribute) объекта (target)
    # Обратите внимание, что параметр target в данном случае это объект, а не строка для импорта как в методе patch()
    # Также обратите внимание на второй обязательный параметр - attribute
    with patch.object(target=MyClass, attribute='my_method') as my_mock_method:
        MyClass().my_method(100)
        my_mock_method.assert_called_with(100)  # Error (100,) != (3,)






    # Вопросы/советы

    # 1. Когда лучше использовать Mock(), а когда patch()?
    # В целом использование Mock является более предпочтительным, т к делает замену более наглядно.
    # Как правило, он хорошо подходит для случаев, когда нужно подменить интерфейсные элементы (например аргументы) объекта тестирования.
    # Пример - создаем мок и передаем его аргументом в тестируемую функцию.
    # Что касается патча, то его лучше использовать для замены внутренних вызовов объектов или импортируемых модулей внутри объекта тестирования.
    # В целом если необходимо подменять класс и потом работать с его экзмпляром и его атрибутами, то лучше делать patch.
    # Пример - если тестируемая функция внутри себя создает экземпляр класса, то нужно пропатчить этот класс вне этой функции.
    # К моменту вызова - класс уже будет подменен. В целом это логично, так как мы не можем менять код тестируемой функции.

    # Итог: мок существует сам по себе (а значит изменения более изолированы и предсказуемы), а патч меняет существующий объект (например класс).



    # 2. Когда нужно задавать спецификацию (передавать параметры spec/autospec)?
    # Без спецификации мок НЕ имеет атрибутов оригинального объекта.
    # Старайтесь всегда задавать спецификацию. Это поможет отследить некорректные обращения к атрибутам.
    # Например, если атрибут не существует в изначальном классе, или если в метод не был передан обязательный параметр.

    # 3. В чем разница между использованием параметров spec и autospec?
    # Параметр spec задает спецификацию только на уровне конкретного создаваемого мока.
    # Например, если изначальный класс имеет какой-то метод и этот метод будет вызван для мока,
    # то возвращаемым значением будет еще один сгенерированный мок, но он уже будет БЕЗ спецификации.
    # В свою очередь autospec рекурсивно передает спецификацию порождаемым мокам.
    # То есть если подытожить:
    # 1) Без spec и autospec мок не имеет атрибутов оригинального объекта.
    # 2) Со spec=True мок имеет атрибуты оригинального объекта, но тип этих атрибутов - просто объект Mock/MagicMock БЕЗ спецификации.
    # 3) С autospec=True мок имеет атрибуты оригинального объекта + тип этих атрибутов Mock/MagicMock со спецификациями.

    # 4. В чем разница между функциями patch.object() и patch()?
    # Функция patch() принимает в качестве аргумента строку вида 'package.module.ClassName'.
    # Это значит, что импорт произойдет прямо в момент патчинга.
    # Функция patch().object() принимает в качестве аргумента непосредственно сам объект.
    # Это значит, что объект уже должен существовать/быть импортирован перед патчем.


    a = 0


a = 0


