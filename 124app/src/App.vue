<script setup lang="ts">
import { ref } from 'vue'
import CodeEditor from './assets/CodeEditor.vue';
import Mainscreen from './assets/main-screen/Main-screen.vue';

const newFileOpened = ref(false);

const showEditor = () => {
  newFileOpened.value = true; 
};

</script>

<template>
  <div class="container">
    <CodeEditor v-if="newFileOpened"/>
    <Mainscreen v-else @newFileClicked="showEditor" />
  </div>
</template>

<style>
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
