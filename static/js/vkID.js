let VKID = window.VKIDSDK;

VKID.Config.init({
  app: 52237939,
  redirectUrl: 'https://id.vchern.me/id/oauth/vk/',
  mode: VKID.ConfigAuthMode.Redirect,
});

const oneTap = new VKID.OneTap();

const cnt = document.getElementById('VkIdSdkOneTap');

if (cnt) {
  oneTap.render({
    cnt,
    scheme: 'dark',
    lang: 0,
    styles: {
      width: 370,
      height: 40,
      borderRadius: 50,
    },
  });
}
