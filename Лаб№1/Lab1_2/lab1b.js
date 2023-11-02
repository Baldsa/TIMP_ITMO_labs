(() => { // Начало самовызывающейся функции для изоляции кода от глобальной области видимости

    let simpleHash = function (s) { // Объявление функции simpleHash для вычисления хэша строки
        var a = 1, c = 0, h, o; // Инициализация переменных a, c, h и o
        if (s) { // Проверка, что строка s существует
            a = 0; // Если строка существует, инициализируем переменную a нулем
            for (h = s.length - 1; h >= 0; h--) { // Цикл, итерирующийся по символам строки справа налево
                o = s.charCodeAt(h); // Получаем числовое представление символа
                a = (a << 6 & 268435455) + o + (o << 14); // Обновляем значение хэша 'a'
                c = a & 266338304; // Вычисляем значение 'c' с использованием побитовой операции И
                a = c !== 0 ? a ^ c >> 21 : a; // Обновляем значение 'a' с использованием побитовых операций
            }
        }
        return a; // Возвращаем рассчитанный хэш 'a'
    };

    var access = false; // Объявление переменной 'access' и инициализация ее значением false (переменная для проверки доступа)

    let noselect = () => access; // Создание функции noselect, которая возвращает значение переменной 'access'

    let antiDebug = setInterval(() => { // Создание интервала для запрета дебага JavaScript-кода
        debugger; // Вызывает отладчик JavaScript
    }, 10);

    document.ondragstart = noselect; // Запрещаем выделять текст при перетаскивании
    document.onselectstart = noselect; // Запрещаем выделять текст при выделении
    document.oncontextmenu = noselect; // Запрещаем контекстное меню при правом клике

    document.addEventListener("keydown", function (event) { // Добавляем слушателя события нажатия клавиши
        if (event.altKey && event.code === "KeyX") { // Если нажат Alt + X
            const pass = prompt("Введите пароль:"); // Запрос ввода пароля у пользователя
            access = checkPassword(pass); // Проверка введенного пароля и установка доступа в зависимости от результата
            if (access) {
                clearInterval(antiDebug);// Если доступ разрешен, останавливаем интервал antiDebug
                alert("Копирование разрешено");
            }
        } else if (event.ctrlKey && event.code === "KeyS" || (event.keyCode >= 112 && event.keyCode <= 123)) {
            // Запрещаем сохранение страницы через Ctrl+S и некоторые функциональные клавиши (F1-F12),
            // особенно devTools (F12)
            if (access) return true; // Если доступ разрешен, позволяем выполнить действие по умолчанию
            event.preventDefault(); // В противном случае, предотвращаем выполнение действия по умолчанию
            return false;
        }
    });

    let checkPassword = (pass) => simpleHash(pass) == 250052358;
    document.addEventListener('copy', function (e) { //Запрещаем копировать
        if (access) return true;
        e.clipboardData.setData('text/plain', '');
        e.preventDefault();
    });

})(); // Завершение самовызывающейся функции
