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
//   const filehandle  = await window.showSaveFilePicker({
//     types: [
//       {
//         description: 'Text Files',
//         accept: {
//           'text/plain': ['.txt'],
//         },

//       },
//     ],
//   });
//   // return handle;
//   // const writable = await filehandle.createWritable();
//   // await writable.write(content);
//   // await writable.close();
//   // isFileSaved.value = true;
//   emit('action','fileSaved', {name: filehandle.name, handle: filehandle})
// };


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