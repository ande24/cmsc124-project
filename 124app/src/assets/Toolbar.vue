<script lang="ts" setup>
import { ref } from 'vue';

const emit = defineEmits(['action']);
const isFileSaved = ref(true);

const openExistingFile = async () => {
    const [fileHandle] = await window.showOpenFilePicker({
      types: [
        {
          description: 'Text Files',
          accept: {
            'text/plain': ['.txt'],
          },
        }
      ],
    });
    const file = await fileHandle.getFile();
    const content = await file.text();
    // textArea.value = contents;
    emit('action', 'openFile', { name: file.name, content, handle: fileHandle });
  
};



// const saveFile = async (content: string) => {
//   try {
    
//   } 
// };

// ... other functions ...

</script>

<template>
  <v-toolbar app dense>
    <v-btn id="newFile" @click="$emit('action', 'newFile')" icon>
      <v-icon class="icons">mdi-file-plus</v-icon>
    </v-btn>
    <v-btn id="openFile" @click="openExistingFile" icon>
      <v-icon class="icons">mdi-folder-open</v-icon>
    </v-btn>
    <v-btn id="saveFile" @click="$emit('action', 'saveFile')" icon="isFileSaved">
      <v-icon class="icons">mdi-content-save</v-icon>
    </v-btn>
    <v-btn id ="undo" >
      <v-icon class = "icons">mdi-undo</v-icon>
    </v-btn>
    <v-btn id ="redo" >
      <v-icon class = "icons">mdi-redo</v-icon>
    </v-btn>
    <v-btn id ="cut" >
      <v-icon class = "icons">mdi-content-cut</v-icon>
    </v-btn>
    <v-btn id ="undo" >
      <v-icon class = "icons">mdi-content-paste</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<style scoped>
  /* ... styles ... */
  .v-toolbar{
    background-color: #1e1e1e;
  }

  .icons{
    color: antiquewhite;
  }
</style>