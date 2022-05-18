<template>
  <div id="app">
    <NavHeader></NavHeader>
    <Tab> </Tab>
    <BotFooter> </BotFooter>
  </div>
</template>

<script>
import Tab from "./components/Tab";
import BotFooter from "./components/BotFooter";
import NavHeader from "./components/NavHeader";
export default {
  // name: "App",
  components: {
    BotFooter,
    NavHeader,
    Tab
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
  height: 90vh; /* vh stands for view-port height, 1vh is 1% of screen height*/
}
</style>
