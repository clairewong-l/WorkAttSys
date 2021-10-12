<template>
  <div class="mainPage">
    <HeadMenu />
    <div class="outer-background">
      <div class="core-background">
        <div style="width: 50%; float: left;margin-top:30px ;margin-left:20px">
          <div class="recordChart">
            <el-calendar :first-day-of-week="7">
              <template slot="dateCell" slot-scope="{ data }">
                <div
                  :class="data.isSelected ? 'is-selected' : ''"
                  @click="handelDateCellSelect(data)"
                  style="
                    margin-top: -5px;
                    padding-top: 10px;
                    position: relative;
                    width: 100%;
                    height: 100%;
                  "
                >
                  {{ data.day.split("-").slice(1)[1] }}
                </div>
              </template>
            </el-calendar>
          </div>
          <div style="width: 100%">
            <div
              style="
                width: 20%;
                float: left;
                height: 140px;
                padding: 5px;
                background-color: whitesmoke;
              "
            >
              <div class="dayPanel">
                <div style="width: 100%">
                  <span
                    style="font-size: 50px; color: blueviolet; margin: auto"
                    >{{ selectDate.day }}</span
                  >
                </div>
                <div style="width: 100%; color: gray">
                  <span>{{ selectDate.year }}年</span>
                  <span>{{ selectDate.month }}月</span>
                </div>
                <div style="width: 100%; color: red">
                  <span>出勤状态</span>
                </div>
              </div>
            </div>
            <div
              style="
                width: 70%;
                float: left;
                height: 150px;
              "
            >
              <div style="width: 100%">
                <el-empty :image-size="60" description="暂无异常出勤记录" v-if="!staffRecordMsgs||staffRecordMsgs.length==0"></el-empty>
                <el-carousel
                  :interval="4000"
                  type="card"
                  height="140px"
                  class="dayRecordCarousel"
                  v-else
                >
                  <el-carousel-item
                    v-for="(item, i) in staffRecordMsgs"
                    :key="i"
                  >
                    <div class="dayRecordMsg">
                      <div style="width: 100%; margin-top: 10px">
                        {{ item.name }}{{ item.id }}
                      </div>
                      <div style="width: 100%; margin-top: 10px">
                        {{ item.status }}
                      </div>
                    </div>
                  </el-carousel-item>
                </el-carousel>
              </div>
            </div>
          </div>
        </div>
        <div style="width: 48%; float: left;margin-top:30px">
          <div style="width: 100%; height: 450px; padding-bottom: 10px">
            <div
              style="
                height: 100%;
                width: 90%;
                background-color: papayawhip;
                margin: auto;
                border:3px solid whitesmoke;
                border-radius: 20px;
                box-shadow:4px 4px 19px whitesmoke;
              "
              v-if="!contentUnfold"
            >
              <div style="width: 100%; height: 450px">
                <div style="width: 100%; float: left">
                  <h3>欢迎您!{{ $store.getters.hrName }}</h3>
                  <span style="margin-left: 50px">公司： {{ $store.getters.companyName }}</span>
                  <span style="margin-left: 50px">法人： {{ legalPerson }}</span>
                </div>

                 <el-carousel
              style="height: 355px; width: 600px; margin: auto"
              v-if="!contentUnfold"
               >
              <el-carousel-item
                style="height: 100%; width: 100%; margin-top:20px"
                v-for="item in imgList"
                :key="item.name"
              >
                <el-image :src="item.src" style="height: 100%"></el-image>
              </el-carousel-item>
            </el-carousel>
              </div>
              <div style="width: 100%; height: 150px;"></div>
            </div>
            <el-card
              class="box-card"
              style="height: 100%; width: 90%;
                     margin: auto;
                     background-color: papayawhip !important;
                     border:3px solid white!important;
                     border-radius: 20px;
                     box-shadow:4px 4px 20px whitesmoke;"
                     
              v-else-if="contentUnfold"
            >
              <div slot="header" class="clearfix" style="height: 20px">
                <el-link
                  :underline="false"
                  style="float: left; padding: 3px 6px;
                  border:3px solid white!important;
                     border-radius: 20px;
                     box-shadow:4px 4px 20px whitesmoke;
                     "
                  @click="contentUnfold = false"
                  >返回</el-link
                >
                <div class="noticeDetailTitle">
                  <h4 v-if="isEditedNotice">编辑公告</h4>
                  <h4 v-if="!isEditedNotice">新建公告</h4>
                </div>
                <el-dropdown
                  split-button
                  type="text"
                  szie="mini"
                  @click="handleNoticeCommand('save')"
                  @command="handleNoticeCommand"
                  style="float: right; margin-bottom: 13px; margin-right: -10px;
                  padding: 0 10px;
                  border:3px solid white!important;
                     border-radius: 20px;
                     box-shadow:4px 4px 20px whitesmoke;
                     font-family:Fantasy"
                  v-if="isEditedNotice"
                >
                  保存
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item command="add">
                      <el-button type="text">新建</el-button>
                    </el-dropdown-item>
                    <!-- <el-dropdown-item command="delete">删除</el-dropdown-item> -->
                    <el-dropdown-item command="delete">
                      <el-popover
                        placement="bottom"
                        width="160"
                        v-model="confirmDeleteVisible"
                      >
                        <p>确定要删除该公告吗？</p>
                        <div style="text-align: right; margin: 0">
                          <el-button
                            size="mini"
                            type="text"
                            @click="confirmDeleteVisible = false"
                            >取消</el-button
                          >
                          <el-button
                            type="primary"
                            size="mini"
                            @click="handleDeleteNotice"
                            >确定</el-button
                          >
                        </div>
                        <el-button type="text" slot="reference">删除</el-button>
                      </el-popover>
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
                <el-button
                  type="text"
                  style="float: right; margin-bottom: 3px; margin-right: 5px"
                  v-if="!isEditedNotice"
                  @click="handleNoticeCommand('new')"
                  >发布</el-button
                >
              </div>
              <div class="text item" style="margin: auto; height: 100%;background: papayawhip">
                <el-input
                  type="textarea"
                  style="background-color: papayawhip"
                  v-model="currentNotice.info"
                  placeholder="发布一段0-600字的公告，提醒员工注意事项吧"
                  :autosize="{ minRows: 15, maxRows: 20 }"
                ></el-input>
              </div>
            </el-card>
          </div>
          <div style="width: 50%; float: left;">
            <div class="noticePanel">
              <div
                style="
                  width: 100%;
                  height: 23px;
                  border-bottom: 2px solid gainsboro;
                "
              >
                <el-popover placement="left" width="400" trigger="click">
                  <el-container class="noticeMorePanel">
                    <el-header style="height:30px; width:100%;background-color: whitesmoke;padding-top:5px;">
                      <span class="miniTitle">历史公告</span>
                    </el-header>
                    <el-main style="padding:0">
                      <el-divider></el-divider>
                      <div
                        v-for="(item, i) in noticeMsgs"
                        :key="i"
                        style="width: 100%"
                      >
                        <el-link :underline="false" @click="showNoticeDetail(i)">
                          <div style="width: 350px; height: 25px">
                            <div
                              style="width: 80%; font-size:15px; float: left; text-align: left"
                            >
                              <div class="ellipsis-display-text">
                                {{ item.info }}
                              </div>
                            </div>
                            <div
                              style="
                                width: 20%;
                                float: right;
                                text-align: right;
                                font-size: smaller;
                                color: gray;
                              "
                            >
                              {{ item.datetime }}
                            </div>
                          </div>
                        </el-link>
                        <el-divider></el-divider>
                      </div>
                    </el-main>
                  </el-container>
                  <el-link
                    slot="reference"
                    :underline="false"
                    class="noticeMoreHeader"
                    >&lt;&lt; 更多</el-link
                  >
                </el-popover>
                <el-link
                  :underline="false"
                  class="noticeHeader"
                  @click="showNoticeDetail(-1)"
                  >公告</el-link
                >
              </div>
              <div style="width: 100%">
                <el-link
                  :underline="false"
                  v-for="(item, i) in noticeMsgs.slice(0, 4)"
                  :key="i"
                  @click="showNoticeDetail(i)"
                  style="width: 100%"
                >
                  <div
                    style="
                      width: 350px;
                      height: 25px;
                      padding-top: 5px;
                      border-bottom: 2px solid gainsboro;
                    "
                  >
                    <div
                      style="
                        width: 78%;
                        float: left;
                        text-align: left;
                        padding-left: 5px;
                      "
                    >
                      <div class="ellipsis-display-text">{{ item.info }}</div>
                    </div>
                    <div
                      style="
                        width: 20%;
                        float: right;
                        text-align: right;
                        font-size: smaller;
                        color: gray;
                      "
                    >
                      {{ item.datetime }}
                    </div>
                  </div>
                </el-link>
              </div>
            </div>
          </div>
          <div style="width: 45%; float: left;">
            <div class="staffNewsPanel">
              <div style="position:absolute; text-align:right; right:80px">
                <span class="miniTitle">最新动态</span>
              </div>
              <el-empty :image-size="56" description="暂时没有动态" v-if="!staffNews||staffNews.length==0"></el-empty>
              <el-timeline style="padding-top:10px" v-else>
                <el-timeline-item
                  v-for="(item, i) in staffNews"
                  :key="i"
                  :timestamp="item.time"
                  placement="top"
                >
                  <el-card style="height: 40px; width: 80%; background: transparent;
      border-radius: 20px;
      ">
                    <p style="margin-top: -10px">
                      {{ item.name }} {{ item.info }}
                    </p>
                  </el-card>
                </el-timeline-item>
              </el-timeline>
            </div>
          </div>
        </div>
      </div>
    </div>
    <CopyrightFooter />
  </div>
</template>

<script>
import moment from "moment"; //moment.js时间格式
import HeadMenu from "../components/HeadMenu.vue";
import CopyrightFooter from "../components/CopyrightFooter.vue";
import {
  getNewNotice,
  getStaffNews,
  addNotice,
  updateNotice,
  deleteNotice,
  getExRecordMsg,
} from "../assets/js/api";

export default {
  name: "MainPage",

  components: {
    HeadMenu,
    CopyrightFooter,
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
      status: 1,
    };
    const notice = {
      notice_id: 1,
      info: "关于你是光你是电你是唯一的神话这件事",
      datetime: "2021-7-8 8:30",
    };
    const staffNew = {
      name: "张三",
      time: "7:30",
      info: "刚刚打卡成功",
    };
    return {

      imgList:[
        {
          name:"p1",
          src: require("../assets/images/logo.png")
        },
        {
          name:"p2",
          src: require("../assets/images/1.png")
        },
        {
          name:"p3",
          src: require("../assets/images/logo_brief.png")
        },
        
      ],

      logoPath: require("../assets/images/logo.png"),
      legalPerson: "张三",
      contentUnfold: false,
      isEditedNotice: false,
      confirmDeleteVisible: false,
      noticeMsgs: Array(20).fill(notice),
      currentNotice: notice, //显示在公告详情
      staffNews: Array(5).fill(staffNew), //员工的最新出勤动态
      selectDate: {
        year: 2021,
        month: 7,
        day: 17,
      },
      staffRecordMsgs: Array(5).fill(staffRecordMsg),
      msxMsgNum: 5,
    };
  },
  // 方法
  methods: {
    showNoticeDetail(i) {
      // this.$message(i);
      //当直接点击公告时传入i值-1，为新建公告
      this.contentUnfold = true;
      if (i >= 0) {
        this.isEditedNotice = true;
        this.currentNotice = { ...this.noticeMsgs[i] }; //取消数据绑定避免修改公告时直接影响主界面
      } else {
        this.isEditedNotice = false;
        this.clearNotice();
      }
    },
    loadMoreNotice() {},
    handleNoticeCommand(command) {
      if (command == "add") {
        //新建公告
        this.clearNotice();
        this.isEditedNotice = false;
      } else if (command == "save") {
        //修改并发布
        if (this.currentNotice.info.trim().length < 1) {
          return;
        }
        this.currentNotice.datetime = moment(new Date()).format(
          "YYYY-MM-DD hh:mm:ss"
        );
        updateNotice({
          id: this.currentNotice.notice_id,
          datetime: this.currentNotice.datetime,
          info: this.currentNotice.info,
        }).then((response) => {
          if (response.status == 1) {
            this.$message("修改成功");
            //本地处理，删除旧公告再加新公告
            for (var i = 0; i < this.noticeMsgs.length; i++) {
              if (this.noticeMsgs[i].notice_id == this.currentNotice.notice_id) {
                this.noticeMsgs.splice(i, 1);
                break;
              }
            }
            this.noticeMsgs.unshift(this.currentNotice);
            this.contentUnfold = false;
          }
        });
      } else if (command == "new") {
        //发布新公告
        if (this.currentNotice.info.trim().length < 1) {
          return;
        }
        this.currentNotice.datetime = moment(new Date()).format(
          "YYYY-MM-DD hh:mm:ss"
        );
        addNotice({
          company_name: this.$store.getters.companyName,
          datetime: this.currentNotice.datetime,
          info: this.currentNotice.info,
        }).then((response) => {
          if (response.status == 1) {
            this.$message("发布成功");
            this.currentNotice.notice_id = response.data.notice_id;
            this.noticeMsgs.unshift(this.currentNotice);
            this.contentUnfold = false;
          } else {
            this.$message(response.msg);
          }
        });
        //删除公告已在子控件中处理
      }
    },
    handleDeleteNotice() {
      this.confirmDeleteVisible = false;
      deleteNotice({
        id: this.currentNotice.notice_id,
      }).then((response) => {
        if (response.status == 1) {
          this.$message("已成功删除公告");
          for (var i = 0; i < this.noticeMsgs.length; i++) {
            if (this.noticeMsgs[i].notice_id == this.currentNotice.notice_id) {
              this.noticeMsgs.splice(i, 1);
              break;
            }
          }
          this.contentUnfold = false;
        } else {
          this.$message(response.msg);
        }
      });
    },
    clearNotice() {
      this.currentNotice = {
        info: "",
        datetime: "",
      };
    },
    updateExRecordMsg(date) {
      getExRecordMsg({
        company_name: this.$store.getters.companyName,
        datetime: date,
      }).then((response) => {
        this.staffRecordMsgs = response.data;
        if (response.status == 0) {
          console.log(response.msg);
        }
      });
    },
    handelDateCellSelect(data) {
      var date0 = new Date(data.day);
      this.selectDate.year = date0.getFullYear();
      this.selectDate.month = date0.getMonth() + 1;
      this.selectDate.day = date0.getDate();
      this.updateExRecordMsg(data.day);
    },
  },
  mounted() {
    //获取公告
    // console.log(this.$store.getters.companyName);
    getNewNotice({ company_name: this.$store.getters.companyName }).then(
      (response) => {
        this.noticeMsgs = response.data;
        if (response.status == 0) {
          console.log(response.msg);
        }
      }
    );
    //获取出勤动态
    getStaffNews({ company_name: this.$store.getters.companyName }).then(
      (response) => {
        console.log(response.data)
        this.staffNews = response.data;
        if (response.status == 0) {
          console.log(response.msg);
        }
      }
    );
    var date = moment(new Date()).format("YYYY-MM-DD");
    this.updateExRecordMsg(date);
  },
};
</script>
<style scoped>
.noticePanel {
  width: 100%;
  height: 300px;
  margin: auto;
}
.noticeHeader {
  float: right;
  text-align: right;
  font-weight: bold;
  font-size: large;
}
.noticeMorePanel {
  width: 400px;
  max-height: 650px;
  overflow: auto;
}
.noticeMoreHeader {
  text-align: left;
  float: left;
  font-weight: bold;
  color: gainsboro;
}
.notice {
  width: 100%;
  padding: 5px;
  border-bottom: 2px solid gainsboro;
}
.noticeDetailTitle {
  width: 70%;
  float: left;
  margin-top: -10px;
  margin-left: 50px;
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
.staffNewsPanel {
  height: 180px;
  overflow: auto;
  text-align: left;
}
.miniTitle{
  font-size:large;
  font-weight:bold;
}
.recordChart {
  width: 90%;
}
.el-divider--horizontal {
  margin: 8px 0;
  background: 0 0;
  border-top: 1px dashed #e8eaec;
}
</style>

<style>
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
