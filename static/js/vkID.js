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

async function generateCodeChallenge(codeVerifier) {
    const encoder = new TextEncoder();
    const data = encoder.encode(codeVerifier);

    const hash = await crypto.subtle.digest('SHA-256', data);

    const byteArray = new Uint8Array(hash);

    const base64String = btoa(String.fromCharCode(...byteArray));
    const codeChallenge = base64String.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');

    return codeChallenge;
}

const VKID = window.VKIDSDK;

generateCodeChallenge(get_code_verifier(64)).then(
    codeChallenge => {
        VKID.Config.init({
            app: 52237939,
            redirectUrl: "https://id.vchern.me/id/login/",
            mode: VKID.ConfigAuthMode.InNewTab,
            codeChallenge: codeChallenge,
        });
    }
)

const oneTap = new VKID.OneTap();

const container = document.getElementById('VkIdSdkOneTap');

if (container) {
  oneTap.render({ container: container, scheme: VKID.Scheme.LIGHT, lang: VKID.Languages.RUS });
}

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);


if (urlParams.has('code')) {
    entries = urlParams.entries();
    for(const entry of entries) {
        console.log(`${entry[0]}: ${entry[1]}`);
    }
    const code = urlParams.get('code')
    const device_id = urlParams.get('device_id')
    console.log(VKID.Config.store.codeChallenge)
    console.log(VKID.Auth.exchangeCode(code, device_id))
}