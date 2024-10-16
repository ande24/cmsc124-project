<script setup lang="ts">
import CodeEditor from './assets/CodeEditor.vue';
import Mainscreen from './assets/main-screen/Main-screen.vue';
</script>

<template>
  <div class="container">
    <!-- <CodeEditor /> -->
     <Mainscreen />
  </div>
</template>

<style>
  .container {
    display: flex;
    flex-direction: column; 
    height: 100vh; 
  }

  .CodeEditor {
    flex-grow: 1; 
  }
</style>
