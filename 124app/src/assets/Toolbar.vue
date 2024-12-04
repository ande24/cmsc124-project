<script lang="ts" setup>
import { ref } from 'vue';
import axios from 'axios';

const emit = defineEmits(['action']);
const isFileSaved = ref(true);
const output = ref(null);
const error = ref(null);

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
  emit('action', 'openFile', { name: file.name, content, handle: fileHandle });
};

const saveasFile = async () => {
  emit('action', 'saveasFile');
};

const copyContent = async () => {
  const selectedText = window.getSelection().toString(); // Get highlighted text
  if (selectedText) {
    navigator.clipboard.writeText(selectedText)
      .then(() => {
        console.log("Selected text copied to clipboard:", selectedText);
        alert("Copied to clipboard!");
      })
      .catch((err) => {
        console.error("Failed to copy text:", err);
        alert("Failed to copy text. Please try again.");
      });
  } else {
    alert("No text selected to copy!");
  }
};

const pasteContent = async () => {
  navigator.clipboard.readText()
    .then((text) => {
      document.getElementById("textInput").value = text; // Paste into input
    })
    .catch((err) => console.error("Error reading clipboard:", err));
};

const runPythonScript = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/compile-File/');
    output.value = response.data.output;
    error.value = response.data.error;
  } catch (err) {
    error.value = err.message;
  }
};
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
    <v-btn id="saveasFile" @click="saveasFile" icon>
      <v-icon class="icons">mdi-content-save-settings </v-icon>
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
    <v-btn id ="paste" @click = "pasteContent" icon >
      <v-icon class = "icons">mdi-content-paste</v-icon>
    </v-btn>
    <v-btn id = "copy" @click = "copyContent" icon>
      <v-icon class = "icons">mdi-content-copy</v-icon>
    </v-btn>
    <v-spacer></v-spacer>
    <div id="play">
      <v-btn id= "compile" @click="runPythonScript" icon>
        <v-icon class = "icons">mdi-play-box-edit-outline</v-icon>
      </v-btn>
      <div v-if="output" style="color: white;">Output: console.log({{ output }})</div>
      <div v-if="error" style="color: red;">Error: {{ error }}</div>
    </div>
  </v-toolbar>
</template>

<style scoped>
  .v-toolbar {
    background-color: #1e1e1e;
  }

  .icons {
    color: antiquewhite;
  }

  .compile{
    display: flex;
    padding-right: 50px;
  }
</style>
