<template>
    <v-toolbar app>
        <v-btn @click="openNewFile" icon>
            <v-icon class="icons">mdi-file-plus</v-icon>
        </v-btn>
        <v-btn @click="openExistingFile" icon>
            <v-icon class="icons">mdi-folder-open</v-icon>
        </v-btn>
        <v-btn @click="saveFile" icon :disabled="isFileSaved">
            <v-icon class="icons">mdi-content-save</v-icon>
        </v-btn>
        <v-btn @click="saveAsNewFile" icon>
            <v-icon class="icons">mdi-content-save-settings</v-icon>
        </v-btn>
        <v-btn @click="cut" icon>
            <v-icon class="icons">mdi-content-cut</v-icon>
        </v-btn>
        <v-btn @click="paste" icon>
            <v-icon class="icons">mdi-content-paste</v-icon>
        </v-btn>
        <v-btn @click="undo" icon>
            <v-icon class="icons">mdi-undo</v-icon>
        </v-btn>
        <v-btn @click="redo" icon>
            <v-icon class="icons">mdi-redo</v-icon>
        </v-btn>
    </v-toolbar>
  </template>

<script>
    /*functions here*/
</script>

<style>
    .v-toolbar {
        background-color: #1e1e1e; 
    }

    .custom-divider {
        width: 1px; 
        height: 24px; 
        border-left: 1px solid white;
    }

    .icons {
        color: white;
    }
</style>

