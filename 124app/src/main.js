import { createApp } from "vue";
import { appWindow } from '@tauri-apps/api/window';
import { invoke } from '@tauri-apps/api/tauri';

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

import App from "./App.vue";

appWindow.on('tauri://ready', () => {
    // Simulate a delay or wait for actual initialization to complete
    setTimeout(() => {
      // Hide the splash screen
      invoke('close_splashscreen');
  
      // Show the main window
      appWindow.show();
    }, 3000); // Delay of 2 seconds for the splash screen
  });

const vuetify = createVuetify({
    components,
    directives,
})

createApp(App).use(vuetify).mount("#app");
