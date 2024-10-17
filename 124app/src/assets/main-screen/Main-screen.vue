<template>
  <v-app>
    <Navbar />
    <v-card>
      <v-layout>
        <v-navigation-drawer
          v-model="drawer"
          :rail="true"
          app
          permanent
          height="100%"
          class="sidebar-class"
        >
          <v-list density="compact" nav>
            <v-list-item
              prepend-icon="mdi-file-multiple"
              title="explorer-main"
              @click.stop="toggleRail('explorer')"
              style="color: white;"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-magnify"
              title="search-main"
              @click.stop="toggleRail('search')"
              style="color: white;"
            ></v-list-item>
            <v-list-item
              prepend-icon="mdi-creation-outline"
              title="run-debug-main"
              @click.stop="toggleRail('run-debug')"
              style="color: white;"
            ></v-list-item>
          </v-list>
        </v-navigation-drawer>
        <v-main style="height: 100vh; background-color: #343434;">
          <!-- Content for each rail -->
          <div v-if="activeRail === 'explorer'">
            <v-navigation-drawer :width="190" style="background-color: #202020; color: white;">
              <v-list-item title="EXPLORER" ></v-list-item>
              <v-divider></v-divider>
              <v-list-item link title="List Item 1"></v-list-item>
              <v-list-item link title="List Item 2"></v-list-item>
              <v-list-item link title="List Item 3"></v-list-item>
            </v-navigation-drawer>
          </div>
          <div v-if="activeRail === 'search'">
            <v-navigation-drawer :width="190" style="background-color: #202020; color: white">
              <v-list-item title="SEARCH"></v-list-item>
              <v-divider></v-divider>
              <v-list-item link title="List Item 1"></v-list-item>
              <v-list-item link title="List Item 2"></v-list-item>
              <v-list-item link title="List Item 3"></v-list-item>
            </v-navigation-drawer>
          </div>
          <div v-if="activeRail === 'run-debug'">
            <v-navigation-drawer :width="190" style="background-color: #202020; color: white">
              <v-list-item title="RUN and DEBUG"></v-list-item>
              <v-divider></v-divider>
              <v-list-item link title="List Item 1"></v-list-item>
              <v-list-item link title="List Item 2"></v-list-item>
              <v-list-item link title="List Item 3"></v-list-item>
            </v-navigation-drawer>
          </div>
          <div class="ide-name">
            <h1>AY DEE E</h1>
          </div>
          <div class="new-file" @click="newFileClicked">
            <button style="border: 4px solid white; border-radius: 40px;background-color: #02123c; color: white; padding-top: 10px; padding-bottom: 10px; padding-left: 30px; padding-right: 30px;"> New File </button>
          </div>
          <h2>Open existing file:</h2>
          <div class="existing-file">
          <v-btn class="existing-file-button">
          </v-btn>
          <v-btn class="existing-file-button">
          </v-btn>
          <v-btn class="existing-file-button">
          </v-btn>
          </div>
        </v-main>
      </v-layout>
    </v-card>
  </v-app>
</template>

<script>
import Navbar from './Navbar.vue'

export default {
  components: {
    Navbar
  },
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
    newFileClicked() {
      console.log("new file clicked");
      this.$emit('newFileClicked');
    }
  },
};
</script>

<style scoped>
h2 {
  padding-top: 60px;
  margin-left: 200px;
  color: white;
}
.sidebar-class {
  background: #202020;
}
.ide-name {
  display: flex;
  justify-content: center;
  padding-top: 60px;
  font-size: 50px;
  color: white;
}
.new-file {
  display: flex;
  justify-content: center;
  padding-top: 40px;
  font-size: 20px;
}
.existing-file {
  display: flex;
  margin-top: 30px;
  margin-left: 200px;
  margin-right: 200px;
  padding-top: 30px;
  padding-bottom: 30px;
  justify-content: space-around;
  background-color: #02123c;
}
.existing-file-button {
  padding: 125px;
}
</style>