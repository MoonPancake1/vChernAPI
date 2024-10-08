function get_code_verifier(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    const charactersLength = characters.length;

    for (let i = 0; i < length; i++) {
        const randomIndex = Math.floor(Math.random() * charactersLength);
        result += characters.charAt(randomIndex);
    }

    return result;
}

function get_user_data(userTokens) {
    VKID.Auth.userInfo(userTokens.access_token).then(
        userData => {
            let user = userData.user
            window.location.href = `https://id.vchern.me/id/oauth/vk/?` + new URLSearchParams(user).toString() +
                '&' + new URLSearchParams(userTokens).toString()
        }
    )
}

const VKID = window.VKIDSDK;

VKID.Config.init({
    app: 52264590,
    redirectUrl: "https://id.vchern.me/id/login/",
    mode: VKID.ConfigAuthMode.InNewTab,
    codeVerifier: get_code_verifier(64),
});

const oneTap = new VKID.OneTap();

const container = document.getElementById('VkIdSdkOneTap');

if (container) {
  oneTap.render({ container: container, scheme: VKID.Scheme.LIGHT, lang: VKID.Languages.RUS });
}

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);


if (urlParams.has('code')) {
    entries = urlParams.entries();
    const code = urlParams.get('code')
    const device_id = urlParams.get('device_id')
    VKID.Auth.exchangeCode(code, device_id).then(
        userTokens => get_user_data(userTokens)
    )
}