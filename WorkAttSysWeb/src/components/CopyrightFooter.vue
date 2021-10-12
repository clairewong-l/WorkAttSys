<template>
    <div class="divFooter">
      <div class="content">Copyright@</div>
      <div style="font-weight:bold;display: inline-block;">选项目忘了找人组</div>
      <el-divider direction="vertical"></el-divider>
      <div class="content">Welcome to WorkAttSys!</div>
    </div>
</template>

<script>
  export default {
    name: 'CopyrightFooter'
  }
</script>

<style scoped>
.divFooter{
  font-size: small;
  width:100%;
  height:44px;
  background-color: papayawhip;
  padding-top:1px
}
.content{
  display: inline-block;
  margin: 10px;
}

</style>