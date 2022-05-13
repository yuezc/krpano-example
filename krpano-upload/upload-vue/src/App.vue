<template>
  <div id="app">
    <AppHome></AppHome>
  </div>

</template>
<script>
import AppHome from "./views/home.vue"
export default {
  name: "App",
  components: {
    AppHome
  },
  mounted() {
  },
  methods: {

  }
}
</script>
<style scoped lang="scss">
#app html body{
  margin: 0;
  padding: 0;
  position: absolute;
  width: 100%;
  height: 100%;
}
::v-deep {
  .el-xx {
  }
}
</style>
