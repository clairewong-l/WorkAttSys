<template>
  <div class="divhead">
    <el-menu :default-active="$route.path" class="el-menu-demo" mode="horizontal" background-color="papayawhip" @select="handleSelect"
      text-color="white" active-text-color="#808080" >
      <el-row>
        <el-col :span="4">
          <el-image :src="briefLogoPath" style="height: 55px; width: 200px;float:right" />
        </el-col>
        <el-col :span="1">
          <el-divider direction="vertical"></el-divider>
        </el-col>
        <el-col :span="2" >
          <el-menu-item index="/MainPage"><span>主页</span></el-menu-item>
        </el-col>
        <el-col :span="2">
          <el-menu-item index="/ManagerPage"><span>管理中心</span></el-menu-item>
        </el-col>
        <el-col :span="2">
          <el-menu-item index="/MessagePage"><span>申请处理</span></el-menu-item>
        </el-col>
        <el-col :span="2">
          <el-menu-item index="/RecordPage"><span>考勤记录</span></el-menu-item>
        </el-col>
        <el-col :span="1" style="float:right">
          <el-dropdown>
            <span class="el-dropdown-link">
              <el-button type="text">
                <el-avatar size="small" icon="el-icon-user-solid"></el-avatar>
              </el-button>
            </span>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>
                <el-popover placement="bottom" width="160" v-model="confirmExit">
                  <p>确定退出？</p>
                  <div style="text-align: right; margin: 0">
                    <el-button size="mini" type="text" @click="confirmExit = false">取消</el-button>
                    <el-button type="primary" size="mini" @click="handleExit">确定</el-button>
                  </div>
                  <el-button type="text" slot="reference">退出登录</el-button>
                </el-popover>
              </el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-col>
        <el-col :span="1" style="float:right">
          <el-popover
            placement="top-start"
            title="新消息"
            width="200"
            trigger="hover"
            content="暂时没有新消息。">
            <el-badge is-dot slot="reference" type="warning">
              <el-button type="text" style="margin-top: 5px">
                <div style="font-size: 20px">
                  <i class="el-icon-bell"></i>
                </div>
              </el-button>
            </el-badge>
          </el-popover>
        </el-col>
      </el-row>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "HeadMenu",
  data() {
    return {
      confirmExit: false,
      briefLogoPath: require("../assets/images/logo_brief.png"),
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      //console.log(this.$route.path,key)
      if (this.$route.path != key) this.$router.replace(key);
    },
    handleExit(){
      this.$router.replace('/');
    }
  },
};
</script>

<style scoped>
.divhead{
  margin-top:-10px;
}
.el-divider--vertical {
  margin-top: 5px;
  height: 3em;
}
</style>

<style>
.el-menu-item span {
  font-size: larger;
  color: dimgray;
}
.el-menu-item.is-active {
      background-color: whitesmoke !important;
      border:3px solid white!important;
      border-radius: 20px;
      box-shadow:4px 4px 20px whitesmoke;
     
    }

.el-badge__content {
  margin-top: 15px;
  margin-right: 2px;
}
</style>