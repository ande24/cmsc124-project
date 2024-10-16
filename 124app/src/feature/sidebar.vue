<template>
    <v-app>
      <v-card>
        <v-layout>
          <v-navigation-drawer
            v-model="drawer"
            :rail="true" 
            app
            permanent
            height="100%"
          >
            <v-list density="compact" nav>
              <v-list-item
                prepend-icon="mdi-file-multiple"
                title="explorer-main"
                @click.stop="toggleRail('explorer')"
              ></v-list-item>
              <v-list-item
                prepend-icon="mdi-magnify"
                title="search-main"
                @click.stop="toggleRail('search')"
              ></v-list-item>
              <v-list-item
                prepend-icon="mdi-creation-outline"
                title="run-debug-main"
                @click.stop="toggleRail('run-debug')"
              ></v-list-item>
            </v-list>
          </v-navigation-drawer>
          <v-main style="height: 100vh">
            <!-- Content for each rail -->
                <div v-if="activeRail === 'explorer'" >
                    <v-navigation-drawer :width="190">
                        <v-list-item title="EXPLORER"></v-list-item>
                        <v-divider></v-divider>
                        <v-list-item link title="List Item 1"></v-list-item>
                        <v-list-item link title="List Item 2"></v-list-item>
                        <v-list-item link title="List Item 3"></v-list-item>
                    </v-navigation-drawer>
                </div>
                <div v-if="activeRail === 'search'">
                    <v-navigation-drawer :width="190">
                        <v-list-item title="SEARCH"></v-list-item>
                        <v-divider></v-divider>
                        <v-list-item link title="List Item 1"></v-list-item>
                        <v-list-item link title="List Item 2"></v-list-item>
                        <v-list-item link title="List Item 3"></v-list-item>
                    </v-navigation-drawer>
                </div>
                <div v-if="activeRail === 'run-debug'">
                    <v-navigation-drawer :width="190">
                        <v-list-item title="RUN and DEBUG"></v-list-item>
                        <v-divider></v-divider>
                        <v-list-item link title="List Item 1"></v-list-item>
                        <v-list-item link title="List Item 2"></v-list-item>
                        <v-list-item link title="List Item 3"></v-list-item>
                    </v-navigation-drawer>
                </div>
          </v-main>
        </v-layout>
      </v-card>
    </v-app>
  </template>
  
  <script>
  export default {
    data() {
      return {
        drawer: true, // Sidebar starts open
        activeRail: '', // Track which rail is currently active
      };
    },
    methods: {
      toggleRail(page) {
        // Toggle the rail; if the same page is clicked, it closes the rail
        if (this.activeRail === page) {
          this.activeRail = ''; // Close the rail if it's already open
        } else {
          this.activeRail = page; // Set the rail to the clicked page
        }
      },
    },
  };
  </script>