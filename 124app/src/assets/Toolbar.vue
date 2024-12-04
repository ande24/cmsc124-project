<script lang="ts" setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import * as monaco from 'monaco-editor';

const emit = defineEmits(['action']);
const isFileSaved = ref(false);
const output = ref(null);
const error = ref(null);

const editor = ref<monaco.editor.IStandaloneCodeEditor | null>(null);

// Open file method
const openExistingFile = async () => {
  const [fileHandle] = await window.showOpenFilePicker({
    types: [
      {
        description: 'Text Files',
        accept: {
          'text/plain': ['.txt'],
        },
      },
    ],
  });
  isFileSaved.value = false;
  const file = await fileHandle.getFile();
  const content = await file.text();
  emit('action', 'openFile', { name: file.name, content, handle: fileHandle });
};

// Save file as method
const saveasFile = async () => {
  emit('action', 'saveasFile');
  isFileSaved.value = true;
};

// Clipboard copy method
const copyContent = async () => {
  const selectedText = window.getSelection()?.toString();
  if (selectedText) {
    try {
      await navigator.clipboard.writeText(selectedText);
      console.log('Selected text copied to clipboard:', selectedText);
      alert('Copied to clipboard!');
    } catch (err) {
      console.error('Failed to copy text:', err);
      alert('Failed to copy text. Please try again.');
    }
  } else {
    alert('No text selected to copy!');
  }
};

// Clipboard cut method (with Monaco)
const cutContent = () => {
  if (editor.value) {
    const selectedText = editor.value.getModel()?.getValueInRange(editor.value.getSelection()!);
    if (selectedText) {
      navigator.clipboard.writeText(selectedText).then(() => {
        editor.value?.executeEdits(null, [
          {
            range: editor.value.getSelection()!,
            text: '',
            forceMoveMarkers: true,
          },
        ]);
        console.log('Text cut and copied to clipboard:', selectedText);
      });
    }
  }
};

// Clipboard paste method (with Monaco)
const pasteContent = async () => {
  try {
    const clipboardText = await navigator.clipboard.readText();
    if (clipboardText && editor.value) {
      const selection = editor.value.getSelection();
      editor.value.executeEdits(null, [
        {
          range: selection,
          text: clipboardText,
          forceMoveMarkers: true,
        },
      ]);
      console.log('Pasted text into editor');
    }
  } catch (err) {
    console.error('Error reading clipboard:', err);
  }
};

// Undo and redo for Monaco Editor
const undo = () => {
  editor.value?.trigger('keyboard', 'undo', null);
};

const redo = () => {
  editor.value?.trigger('keyboard', 'redo', null);
};

// Lifecycle hook: Initialize Monaco editor
onMounted(() => {
  const editorElement = document.getElementById('editor') as HTMLElement;
  if (editorElement) {
    editor.value = monaco.editor.create(editorElement, {
      value: 'function helloWorld() {\n    console.log("Hello, world!");\n}',
      language: 'javascript',
      theme: 'vs-dark', // Optional: Use a dark theme
    });
  }
});

// Lifecycle hook: Dispose of Monaco editor
onBeforeUnmount(() => {
  editor.value?.dispose();
});

// Method to run a Python script (using axios for backend call)
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
  <v-toolbar app dense class="toolbar">
    <v-btn id="newFile" title="Open new file" @click="$emit('action', 'newFile')" icon>
      <v-icon class="icons">mdi-file-plus</v-icon>
    </v-btn>
    <v-btn id="openFile" title="Open existing file" @click="openExistingFile" icon>
      <v-icon class="icons">mdi-folder-open</v-icon>
    </v-btn>
    <v-btn id="saveFile" title="Save" @click="$emit('action', 'saveFile')" icon :disabled="isFileSaved" :class="{'disabled-btn': isFileSaved}">
      <v-icon class="icons">mdi-content-save</v-icon>
    </v-btn>
    <v-btn id="saveasFile" title="Save as" @click="saveasFile" icon :disabled="isFileSaved" :class="{'disabled-btn': isFileSaved}">
      <v-icon class="icons">mdi-content-save-settings</v-icon>
    </v-btn>
    <v-btn id="cut" title="Cut" @click="cutContent" icon>
      <v-icon class="icons">mdi-content-cut</v-icon>
    </v-btn>
    <v-btn id="paste" title="Paste"@click="pasteContent" icon>
      <v-icon class="icons">mdi-content-paste</v-icon>
    </v-btn>
    <v-btn id="copy" title="Copy"@click="copyContent" icon>
      <v-icon class="icons">mdi-content-copy</v-icon>
    </v-btn>
    <v-btn id="undo" title="Undo"@click="undo" icon>
      <v-icon class="icons">mdi-undo</v-icon>
    </v-btn>
    <v-btn id="redo" title="Redo"@click="redo" icon>
      <v-icon class="icons">mdi-redo</v-icon>
    </v-btn>
    <v-spacer></v-spacer>
    <div id="play" title="Compile and run" style="padding-right: 50px;">
      <v-btn id="compile" @click="runPythonScript" icon>
        <v-icon class="icons">mdi-play-box-edit-outline</v-icon>
      </v-btn>
      <div v-if="output" style="color: white;">Output: {{ output }}</div>
      <div v-if="error" style="color: red;">Error: {{ error }}</div>
    </div>
  </v-toolbar>
</template>

<style scoped>
.v-toolbar {
  background-color: #1e1e1e;
  width: 100%;
  padding-left: 20px;
}

.toolbar {
  display: flex;
  gap: 20px; /* This adds space between the buttons */
}

/* Shrink the icons to 75% */
.v-btn {
  padding: 10px 20px;
  font-size: 1rem;
  position: relative; /* Ensure the glow is behind the button */
  overflow: hidden; /* Prevent the glow from overflowing */
}

.v-btn:hover {
  background-color: #9b4dca; /* Lighter purple background on hover */
  color: transparent; /* Dark text on hover */
  box-shadow: 0 0 20px 5px rgba(162, 110, 226, 0.8), 0 0 30px 10px rgba(162, 110, 226, 0.6); /* Purple glow */
}

.v-btn:hover .icons {
  color: #1a1a1a; /* Dark icon color on hover */
}

.v-btn:active {
  transform: scale(0.98); /* Slight shrink on click */
  box-shadow: none; /* Remove glow on active state */
}

.disabled-btn {
  background-color: #444; /* Darker background when disabled */
  color: #888; /* Grey text */
  cursor: not-allowed; /* Show 'not-allowed' cursor */
}

.disabled-btn:hover {
  background-color: #444; /* No hover effect */
}

.icons {
  color: #e0e0e0; /* Icon color */
  padding-right: 12px;
  padding-left: 12px;
}

/* Optional: Apply consistent spacing between icons */
.v-btn + .v-btn {
  margin-left: 10px;
}

.custom-divider {
  width: 1px;
  height: 24px;
  border-left: 1px solid white;
}

.icons {
  color: #e0e0e0;
}
</style>
