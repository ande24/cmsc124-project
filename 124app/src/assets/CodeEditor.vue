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

    <div>
      <!-- <button @click="copy">Copy</button>
      <button @click="cut">Cut</button>
      <button @click="paste">Paste</button>
      <button @click="undo">Undo</button>
      <button @click="redo">Redo</button> -->
    </div>
  </div>
</template>



<style scoped>
/* Additional styling for buttons */
button {
  margin: 5px;
  padding: 10px;
  font-size: 16px;
  cursor: pointer;
}

button:focus {
  outline: none;
  border: 2px solid #9b4dca; /* Focus effect */
}
</style>

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

<script lang="ts">
import { defineComponent, onMounted, onBeforeUnmount, ref } from "vue";
import * as monaco from "monaco-editor";

export default defineComponent({
  name: "MonacoEditor",
  setup() {
    const editor = ref<monaco.editor.IStandaloneCodeEditor | null>(null);

    // Debug: Log editor initialization
    onMounted(() => {
      editor.value = monaco.editor.create(document.getElementById("editor") as HTMLElement, {
        value: "function helloWorld() {\n    console.log('Hello, world!');\n}",
        language: "javascript",
        theme: "vs-dark",
      });

      console.log("Editor initialized:", editor.value);
    });

    onBeforeUnmount(() => {
      editor.value?.dispose();
    });

    const copy = () => {
      console.log("Copy triggered");
      editor.value?.trigger("keyboard", "editor.action.clipboardCopyAction", null);
    };

    const cut = () => {
      console.log("Cut triggered");
      editor.value?.trigger("keyboard", "editor.action.clipboardCutAction", null);
    };

    const paste = () => {
      console.log("Paste triggered");
      editor.value?.trigger("keyboard", "editor.action.clipboardPasteAction", null);
    };

    const undo = () => {
      console.log("Undo triggered");
      editor.value?.trigger("keyboard", "undo", null);
    };

    const redo = () => {
      console.log("Redo triggered");
      editor.value?.trigger("keyboard", "redo", null);
    };

    return { copy, cut, paste, undo, redo };
  },
});
</script>

<style scoped>
.editor-container {
  display: flex;
  flex-direction: column;
  height: 80%;
}

#editor {
  flex-grow: 1;
  overflow: auto;
  transform: scale(1.2);
  transform-origin: 0 0;
}

.actions {
  margin-top: 50px;
}
</style>
