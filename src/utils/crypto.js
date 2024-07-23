import cryptoJs from "crypto-js";

export default class AESCrypto {
  constructor() {
    this.key = cryptoJs
      .SHA512(process.env.ENCRYPT_KEY)
      .toString(cryptoJs.enc.Hex)
      .substring(0, 32);
  }

  encrypt(data) {
    const key = cryptoJs.enc.Hex.parse(this.key);
    return cryptoJs.AES.encrypt(data, key, {
      mode: cryptoJs.mode.ECB,
      padding: cryptoJs.pad.Pkcs7,
    }).toString();
  }

  decrypt(data) {
    const key = cryptoJs.enc.Hex.parse(this.key);
    const decrypted = cryptoJs.AES.decrypt(data, key, {
      mode: cryptoJs.mode.ECB,
      padding: cryptoJs.pad.Pkcs7,
    });
    return decrypted.toString(cryptoJs.enc.Utf8);
  }
}

// function getEncryptedKey() {
//   return cryptoJs
//     .SHA512(process.env.ENCRYPT_KEY)
//     .toString(cryptoJs.enc.Hex)
//     .substring(0, 32);
// }

// export function encrypt(data) {
//   const key = cryptoJs.enc.Hex.parse(getEncryptedKey());
//   return cryptoJs.AES.encrypt(data, key, {
//     mode: cryptoJs.mode.ECB,
//     padding: cryptoJs.pad.Pkcs7,
//   }).toString();
// }

// export function decrypt(data) {
//   const key = cryptoJs.enc.Hex.parse(getEncryptedKey());
//   const decrypted = cryptoJs.AES.decrypt(data, key, {
//     mode: cryptoJs.mode.ECB,
//     padding: cryptoJs.pad.Pkcs7,
//   });
//   return decrypted.toString(cryptoJs.enc.Utf8);
// }
