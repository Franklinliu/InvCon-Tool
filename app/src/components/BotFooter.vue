<template>
    <footer id="footer">
      <p class="text-center">© InvCon 2022, A Dynamic Invariant Detector for Ethereum Smart Contracts!</p>
    </footer>
</template>
<script>
export default {
  name: "BotFooter",
  props: {
    msg: String
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#footer {
   position: fixed;
   left: 0;
   bottom: 0;
   width: 100%;
   text-align: center;
}
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>