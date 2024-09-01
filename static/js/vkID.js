let VKID = window.VKIDSDK;

VKID.Config.init({
  app: 52237939,
  redirectUrl: 'https://id.vchern.me/id/oauth/vk/',
});

const oneTap = new VKID.OneTap();

const container = document.getElementById('btn-vk');

if (container) {
  oneTap.render({
    container,
    scheme: 'dark',
    lang: 0,
    styles: {
      width: 370,
      height: 40,
      borderRadius: 50,
    },
  });
}
