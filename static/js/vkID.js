const VKID = window.VKIDSDK;

// VKID.Config.init({
//   app: 52237939,
//   redirectUrl: 'https://id.vchern.me/id/oauth/vk/',
//   mode: VKID.ConfigAuthMode.Redirect,
// });

// Создание экземпляра кнопки.
const oneTap = new VKID.OneTap();

// Получение контейнера из разметки.
const container = document.getElementById('VkIdSdkOneTap');

// Проверка наличия кнопки в разметке.
if (container) {
  // Отрисовка кнопки в контейнере с именем приложения APP_NAME, светлой темой и на русском языке.
  oneTap.render({ container: container, scheme: VKID.Scheme.LIGHT, lang: VKID.Languages.RUS })
        .on(VKID.WidgetEvents.ERROR, handleError); // handleError — какой-либо обработчик ошибки.
}
