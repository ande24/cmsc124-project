<template>
  <div class="editor-container">
    <div id="editor">
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
      <button @click="copy">Copy</button>
      <button @click="cut">Cut</button>
      <button @click="paste">Paste</button>
      <button @click="undo">Undo</button>
      <button @click="redo">Redo</button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, onBeforeUnmount, ref } from "vue";
import * as monaco from "monaco-editor";
import { readText } from "@tauri-apps/api/clipboard";

export default defineComponent({
  name: "MonacoEditor",
  setup() {
    // Ref for Monaco Editor instance
    const editor = ref<monaco.editor.IStandaloneCodeEditor | null>(null);

    // Methods for Clipboard and Undo/Redo Actions
    const copy = () => {
      editor.value?.trigger("keyboard", "editor.action.clipboardCopyAction", null);
    };

    const cut = () => {
      editor.value?.trigger("keyboard", "editor.action.clipboardCutAction", null);
    };

    const paste = async () => {
      console.log("Paste triggered");

      try {
        const clipboardText = await readText();
        if (clipboardText) {
          const editorInstance = editor.value;
          if (editorInstance) {
            const selection = editorInstance.getSelection();
            editorInstance.executeEdits(null, [
              {
                range: selection,
                text: clipboardText,
                forceMoveMarkers: true,
              },
            ]);
          }
        }
      } catch (err) {
        console.error("Failed to read from clipboard:", err);
      }
    };

    const undo = () => {
      editor.value?.trigger("keyboard", "undo", null);
    };

    const redo = () => {
      editor.value?.trigger("keyboard", "redo", null);
    };

    // Lifecycle Hook: Initialize Monaco Editor
    onMounted(() => {
      editor.value = monaco.editor.create(document.getElementById("editor") as HTMLElement, {
        value: "function helloWorld() {\n    console.log('Hello, world!');\n}",
        language: "javascript",
        theme: "vs-dark", // Optional: Use a dark theme
      });
    });

    // Lifecycle Hook: Dispose of the editor
    onBeforeUnmount(() => {
      editor.value?.dispose();
    });

    return {
      copy,
      cut,
      paste,
      undo,
      redo,
    };
  },
});
</script>

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



defineExpose({
  formatCode
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

#editor {
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
