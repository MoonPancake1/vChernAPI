const VKID = window.VKIDSDK;

VKID.Config.init({
  app: 0,
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
