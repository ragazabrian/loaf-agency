import Vue from "vue";
import {
  TweenMax,
  TimelineMax,
  TweenLite,
  ScrollToPlugin,
  SplitText,
} from "./gsap";
import ScrollMagic from "scrollmagic";

const GSAP = {
  install(Vue, options) {
    // GSAP
    Vue.prototype.$GSAP = {
      TweenMax,
      TweenLite,
      TimelineMax,
      Linear,
      Power1,
      Power2,
      Power3,
      Back,
    };
    // ScrollMagic
    Vue.prototype.$ScrollMagic = {
      Controller: ScrollMagic.Controller,
      Scene: ScrollMagic.Scene,
    };
  },
};

Vue.use(GSAP);



// WEBPACK FOOTER //
// ./src/plugins/gsap-scrollmagic.js