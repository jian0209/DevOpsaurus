import { boot } from "quasar/wrappers";
import VueCryptojs from "vue-cryptojs";

export default boot(({ app, router }) => {
  app.use(VueCryptojs);
});
