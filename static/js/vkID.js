function get_code_verifier (length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    const charactersLength = characters.length;

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * charactersLength);
        result += characters.charAt(randomIndex);
    }

    return result;
}

const VKID = window.VKIDSDK;

VKID.Config.init({
  app: 52237939,
  redirectUrl: 'https://id.vchern.me/id/oauth/vk/',
  mode: VKID.ConfigAuthMode.Redirect,
  codeVerifier: get_code_verifier(64),
});

// Создание экземпляра кнопки.
const oneTap = new VKID.OneTap();

// Получение контейнера из разметки.
const container = document.getElementById('VkIdSdkOneTap');

// Проверка наличия кнопки в разметке.
if (container) {
  console.log("Работает", container)
  // Отрисовка кнопки в контейнере с именем приложения APP_NAME, светлой темой и на русском языке.
  oneTap.render({ container: container, scheme: VKID.Scheme.LIGHT, lang: VKID.Languages.RUS })
        .on(VKID.WidgetEvents.ERROR, handleError); // handleError — какой-либо обработчик ошибки.
} else {
  console.log("Что-то не то", container)
}
