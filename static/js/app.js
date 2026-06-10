//Получаем элементы со страницы
const form = document.getElementById('shortenForm');
const longUrlInput = document.getElementById('longUrl');
const customCodeInput = document.getElementById('customCode');
const resultDiv = document.getElementById('result');
const shortLink = document.getElementById('shortLink');
const copyBtn = document.getElementById('copyBtn');
const stats = document.getElementById('stats');
const errorDiv = document.getElementById('error');
const submitBtn = document.getElementById('submitBtn');

//Обработчик отправки формы
form.addEventListener('submit', async (e) => {
    //Предотвращаем стандартную перегрузку страницы
    e.preventDefault();

    //скрываем предыдущие результаты и ошибки
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');

    //Получаем значения из полей
    const longUrl = longUrlInput.value.trim();
    const customCode = customCodeInput.value.trim();

    //Проверяем, что ссылка начинается с http(s)://
    if (!longUrl.startsWith('http://') && !longUrl.startsWith('https://')){
        showError('Ссылка должна начинаться с http:// или https://');
        return
    }

    //Меняем текст кнопки на "Создаю..."
    submitBtn.textContent = 'Создаю...';
    submitBtn.disabled = true;

    try {
        //Формируем данные для отправки
        const requestData = {
            long_url: longUrl
        };

        //Если пользователь ввел свой код
        if (customCode) {
            requestData.custom_code = customCode;
        }

        //Отправляем POST запрос на наш API
        const response = await fetch('shorten',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        //получаем ответ от сервера
        const data = await response.json();

        //Если ответ успешный (статус 201)
        if (response.ok){
            //Формируем полный URL для короткой ссылки
            const fullShortUrl = window.location.origin + data.short_url;

            //Отображаем результат
            shortLink.href = fullShortUrl;
            shortLink.textContent = fullShortUrl;
            stats.textContent = `Переходов: ${data.clicks}`;

            //Показываем блок с результатом
            resultDiv.classList.remove('hidden');

            //очищаем форму
            longUrlInput.value = '';
            customCodeInput.value = '';
        } else{
            // Если сервер вернул ошибку (например, код уже занят)
            showError(data.detail || 'Произошла ошибка при создании ссылки');
        }
    } catch (error) {
        // Если произошла ошибка сети
        showError('Не удалось подключиться к серверу.');
        console.error('Ошибка:', error);
    } finally {
        // Возвращаем исходный текст кнопки
        submitBtn.textContent = 'Сократить';
        submitBtn.disabled = false;
    }
});

// Обработчик кнопки "Копировать"
copyBtn.addEventListener('click', async () => {
    try {
        // Копируем ссылку в буфер обмена
        await navigator.clipboard.writeText(shortLink.href);

        // Меняем текст кнопки на время
        const originalText = copyBtn.textContent;
        copyBtn.textContent = '✅ Скопировано!';

        // Возвращаем исходный текст через 2 секунды
        setTimeout(() => {
            copyBtn.textContent = originalText;
        }, 2000);

    } catch (error) {
        console.error('Не удалось скопировать:', error);
    }
});

// Функция для отображения ошибок
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}