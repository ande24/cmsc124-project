import { createApp } from "vue";

import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import '@mdi/font/css/materialdesignicons.css';

import { install as VueMonacoEditorPlugin } from '@guolao/vue-monaco-editor';
import { VueMonacoEditor } from '@guolao/vue-monaco-editor'

export default {
    components: { VueMonacoEditor }
}

import App from "./App.vue";

const vuetify = createVuetify({
    components,
    directives
})

const app = createApp(App);
app.use(VueMonacoEditorPlugin, {
    paths: {
        vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.43.0/min/vs'
    }
})
app.use(vuetify);
app.mount("#app");

