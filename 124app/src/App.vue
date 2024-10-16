<script setup lang="ts">
import CodeEditor from './assets/CodeEditor.vue';
import Toolbar from './assets/Toolbar.vue';
import Mainscreen from './assets/main-screen/Main-screen.vue';
</script>

<template>
  <div class="container">
    <!-- <Toolbar /> -->
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
