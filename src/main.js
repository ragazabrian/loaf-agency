// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from "vue";
import App from "./App";
import router from "./router";
import axios from "axios";
import { Loader, middleware } from "resource-loader";
import sniffer from "sniffer";
import VueGtm from "vue-gtm";
import { updateMeta } from "./seo";

import "./assets/tw.css";
import "./main.scss";

if (process.env.NODE_ENV === "production") {
  Vue.use(VueGtm, {
    id: "GTM-M2B6V85",
    debug: process.env.NODE_ENV === "development",
    vueRouter: router,
    trackOnNextTick: true,
  });
}

sniffer.addClasses(document.documentElement);

window.dpr = window.devicePixelRatio;
window.dpr = Math.min(window.dpr || 1, 2);

Vue.prototype.$eventBus = new Vue();
Vue.config.productionTip = false;

window.App = { menu: false };
window.routeStorage = {};

/// -------------------------------------------------
// TOGGLE THIS FROM STAGING TO LIVE WHEN SETTING LIVE
const dataDomain = "https://wp.loaf.agency";
//const dataDomain = "http://wploaf.local";
/// -------------------------------------------------

const dataURL = dataDomain + "/wp-json/acf/v3/global";

new Vue({
  el: "#app",
  router,
  data: function () {
    return {
      dataDomain: dataDomain,
      loading: true,
      progress: 0,
      firstLoad: true,
      content: [],
      vid_cache: {},
      img_cache: {},
      showcase_cache: {},
    };
  },
  manifest: [],
  methods: {
    getData: function () {
      console.log("get data");
      axios
        .get(dataURL)
        .then((response) => {
          console.log("data recieved, getting assets...");
          this.content = response.data;
          // The first navigation ran before the data arrived, so redo the
          // page's title/meta now that WordPress settings and items exist
          updateMeta(this.$route, this.content);
          this.getAssets();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getAssets: function () {
      let loader = new Loader();
      let $this = this;
      let manifest = $this.$options.manifest;
      console.log("getAssets");
      this.$eventBus.$emit("loaded");
    },
  },
  created: function () {
    console.log("app ready");
    this.getData();
  },
  mounted() {
    window.App.el = this.$el.children[0];
  },
  components: { App },
  template: "<App/>",
});



// WEBPACK FOOTER //
// ./src/main.js