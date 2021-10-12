<template>
  <div class="ManagerPage">
    <HeadMenu />
    <div class="outer-background">
      <div class="core-background">
        <div style="width: 50%; float: left;margin-left: 20px;">
          <div style="width: 100%; height: 100px;">
            <el-container>
                <el-container>
                  <el-aside width="100px">
          <div class="aside">
            <div
              @click="changeTab(1)"
              :class="[tabIndex === 1 ? 'active' : '']"
            >
              员工管理
            </div>
            <div
              @click="changeTab(2)"
              :class="[tabIndex === 2 ? 'active' : '']"
            >
              部门管理
            </div>
             <div
              @click="changeTab(3)"
              :class="[tabIndex === 3 ? 'active' : '']"
            >
              考勤设置
            </div>
          </div>
        </el-aside>
       
       <div style="padding: 0;margin-left: 20px ">
          <div v-if="tabIndex === 1"><Staff /></div>
           <div v-if="tabIndex === 2"><Department /></div>
           <div v-if="tabIndex === 3"><Company /></div>
       </div>
     
     
      </el-container>
     
    </el-container>
  
              </div>
             </div>
           </div>
         </div>
    
     <CopyrightFooter />
  </div>
</template>

<script>
import HeadMenu from "../components/HeadMenu.vue";
import CopyrightFooter from "../components/CopyrightFooter.vue";
import Department from  "@/views/Department.vue";
import Staff from "@/views/Staff.vue"
import Company from '@/views/Company.vue';

export default {
  name: "ManagerPage",

  components: {
    HeadMenu,
    CopyrightFooter,
    Staff,
    Company,
    Department,
    
  },
  data() {
    const staffMsg = {
      id: "S23333",
      name: "xiaoming",
      state: "在职",
    };
    const staffRecordMsg = {
      id: "S23333",

      name: "xiaoming",
      stateMsg: "请假",
    };
    const notice = {
      head: "关于你是电你是光你是唯一的神话这件事关于你是电你是光你是唯一的神话这件事关于你是电你是光你是唯一的神话这件事",
      date: "2021-7-8",
    };
    return {
      tabPosition: "left",
      tabIndex: 1,
      logoPath: require("../assets/images/logo.png"),
      contentUnfold: false,
      companyMsg: {
        introduction: "996就是福报",
        legalPerson: "刘大",
      },
      noticeMsgIndex: 0, //显示在详公告信息的index
      noticeMsgs: Array(10).fill(notice),
      recordDate: {
        year: "",
        month: "",
        day: "",
      },
      staffRecordMsgs: Array(20).fill(staffRecordMsg),
      staffMsgs: Array(10).fill(staffMsg),
      msxMsgNum: 5,
    };
  },
  // 方法
  methods: {
    showNoticeDetail(i) {
      console.log(i);
      this.contentUnfold = true;
      this.noticeMsgIndex = i;
    },
     changeTab(params) {
      this.tabIndex = params;
    },
    handleMenuCommand(command) {
      console.log(command);
    },
  },
  mounted() {
    var date = new Date();
    this.recordDate.year = date.getFullYear();
    this.recordDate.month = date.getMonth() + 1;
    this.recordDate.day =
      date.getDate() < 10 ? "0" + date.getDate() : date.getDate();
  },
};
</script>

<style scoped>
.detailShow {
  width: 100%;
  height: 100%;
  margin: atuo;
}
.noticePanel {
  width: 100%;
  /* height: 400px; */
  margin: auto;
}
.noticeHeader {
  width: 20%;
  float: left;
  text-align: left;
  font-weight: bold;
  font-size: large;
}
.noticeMore {
  text-align: right;
  float: right;
  font-weight: bold;
  color: gainsboro;
}
.notice {
  width: 100%;
  padding: 5px;
  border-bottom: 2px solid gainsboro;
}
.dayRecordMsg {
  width: 80%;
  height: 50%;
  margin: auto;
}
.dayPanel {
  width: 80%;
  height: 80%;
  margin: auto;
  background-color: white;
}
.dayRecordPanel {
  /* position: absolute; */
  width: 50%;
  height: 100%;
  margin: auto;
}
.msgNotice {
  text-align: left;
}
.dayRecordChart {
  width: 100%;
}
.recordChart {
  width: 90%;
}
.alignLeftTitle {
  font-family: Microsoft YaHei;
  font-weight: bold;
  float: left;
}
.alignRightDate {
  float: left;
  width: 10%;
  border: 1px solid;
  font-size: x-small;
  color: gray;
}
</style>


<style>
.tab {
  height: 100vh;
  padding-top: 57px;
  transform: translateY(-57px - 40px );
  z-index: 10;
}
.aside {
  height: calc(100vh - 57px - 40px);
  display: flex;
  flex-flow: column;
  justify-content: space-around;
  font-size: 18px;
}
.aside div {
  cursor: pointer;
  padding: 40px 10px;
  background: bisque;
  transition: 0.3s;
}
.aside div.active {
  background-color: whitesmoke !important;
  border:3px solid white!important;
  border-radius: 20px;
  box-shadow:4px 4px 10px whitesmoke;
}
.recordChart .el-calendar-table .el-calendar-day {
  height: 50px;
}

.dayRecordCarousel .el-carousel__item:nth-child(2n) {
  background-color: gainsboro;
}

.dayRecordCarousel .el-carousel__item:nth-child(2n + 1) {
  background-color: whitesmoke;
}
</style>