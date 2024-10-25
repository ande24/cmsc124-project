<script lang="ts" setup>
import { ref } from 'vue';
import { open, save } from '@tauri-apps/api/dialog';
import { readTextFile, writeTextFile } from '@tauri-apps/api/fs';

const emit = defineEmits(['action']);
const isFileSaved = ref(true);

const openExistingFile = async () => {
  try {
    const selected = await open({
      multiple: false,
      filters: [{ name: 'Text Files', extensions: ['txt'] }]
    });
    if (selected && typeof selected === 'string') {
      const content = await readTextFile(selected);
      console.log('File opened:', selected);
      emit('action', 'openFile', { name: selected.split('/').pop(), content });
    }
  } catch (error) {
    console.error('Error opening file:', error);
  }
};

const saveFile = async (content: string) => {
  try {
    const savePath = await save({
      filters: [{ name: 'Text Files', extensions: ['txt'] }]
    });
    if (savePath) {
      await writeTextFile(savePath, content);
      console.log('File saved:', savePath);
      isFileSaved.value = true;
    }
  } catch (error) {
    console.error('Error saving file:', error);
  }
};

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
    <v-btn id="saveFile" @click="$emit('action', 'saveFile')" icon :disabled="isFileSaved">
      <v-icon class="icons">mdi-content-save</v-icon>
    </v-btn>
    <!-- ... other buttons ... -->
  </v-toolbar>
</template>

<style>
  /* ... styles ... */
</style>