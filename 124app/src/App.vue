<template>
  <div class="container">
    <Toolbar @fileOpened="onFileOpened"/>
    <CodeEditor v-if="fileOpened" />
    <GetStarted v-else/>
  </div>
</template>

<script>
import Toolbar from './assets/Toolbar.vue';
import CodeEditor from './assets/CodeEditor.vue'; 
import GetStarted from './assets/GetStarted.vue';

export default {
  data() {
    return {
      fileOpened: false, // Tracks whether a file has been opened
    };
  },
  components: {
    Toolbar,
    CodeEditor,
    GetStarted
  },
  methods: {
    onFileOpened() {
      this.fileOpened = true;  // Show editor once file has been opened
    }
    }
};
</script>

<style>
  div {
    background-color: #1e1e1e;
  }

  .container {
    display: flex;
    flex-direction: column; 
    height: 100vh; 
    width: 100vw;
  }

  .CodeEditor {
    flex-grow: 1; 
  }
</style>
