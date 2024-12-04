<template>
  <div class="editor-container">
    <div class="editor">
      <vue-monaco-editor
        v-model:value="code"
        theme="vs-dark"
        :options="MONACO_EDITOR_OPTIONS"
        @mount="handleMount"
        @change="handleChange"
      />
    </div>

    <!-- Example buttons to trigger actions -->
    <div class="actions">
      <button @click="undo">Undo</button>
      <button @click="redo">Redo</button>
      <button @click="cut">Cut</button>
      <button @click="paste">Paste</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, shallowRef, watch } from 'vue'

const props = defineProps(['content']);
const emit = defineEmits(['update:content']);

const MONACO_EDITOR_OPTIONS = {
  automaticLayout: true,
  formatOnType: true,
  formatOnPaste: true,
}

const code = ref(props.content);
const editorRef = shallowRef();

watch(() => props.content, (newContent) => {
  if (newContent !== code.value) {
    code.value = newContent;
  }
});

const handleMount = (editor) => {
  editorRef.value = editor;
};

const handleChange = (value) => {
  emit('update:content', value);
};

// Function to undo the editor content
const undo = () => {
  if (editorRef.value) {
    editorRef.value.trigger('keyboard', 'undo');
  }
};

// Function to redo the editor content
const redo = () => {
  if (editorRef.value) {
    editorRef.value.trigger('keyboard', 'redo');
  }
};

// Function to cut the selected text
const cut = () => {
  if (editorRef.value) {
    editorRef.value.trigger('keyboard', 'cut');
  }
};

// Function to paste content from clipboard
const paste = () => {
  if (editorRef.value) {
    editorRef.value.trigger('keyboard', 'paste');
  }
};

defineExpose({
  formatCode,
  undo,
  redo,
  cut,
  paste
});

function formatCode() {
  editorRef.value?.getAction('editor.action.formatDocument').run();
}
</script>

<style scoped>
.editor-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.editor {
  flex-grow: 1;
  overflow: auto;
}

.actions {
  margin-top: 10px;
}

button {
  margin-right: 10px;
  padding: 5px 10px;
}
</style>
