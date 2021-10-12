<template>
  <div class="RecordPage">
    <HeadMenu />
    <div class="outer-background">
      <div class="core-background">
        <el-tabs class="border-card"
            style="height: 99%;
                  width: 100%;
                  margin: auto;
                  margin-top:5px;
                  background-color: papayawhip;
                  "
        >
          <el-tab-pane label="图表模式">
            <div style="width: 100%; float: left;margin-top:30px">
              <div id="diagramChart"></div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="周历模式" name="calendarModel">
            <div style="width: 100%; float: left">
              <div style="width: 70%; float: left">
                <div class="calendarChart">
                  <el-calendar
                    :range="calculateDateRange"
                    style="margin-top: 5px;padding-top: 43px;height: 100%; border: 40px papayawhip solid"
                  >
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
                        <div>{{ data.day.split("-").slice(1)[1] }}</div>
                        <div :style="degreeColor(data.day)">
                          {{ recordDegree(data.day) }}
                        </div>
                      </div>
                    </template>
                  </el-calendar>
                </div>
              </div>
              <div style="width: 30%; float: right">
                <el-table
                  :data="staffRecordMsgs"
                  height="600px"
                  stripe
                  style="width: 93%;margin-top: 45px;padding-top: 47px;"
                >
                  <el-table-column prop="staff_id" label="工号" width="70" ></el-table-column>
                  <el-table-column prop="name" label="姓名" width="100" ></el-table-column>
                  <el-table-column prop="datetime" label="日期" width="90" ></el-table-column>
                  <el-table-column prop="department" label="部门" width="90" ></el-table-column>
                  <el-table-column prop="status" label="状态" width="60" ></el-table-column>
                </el-table>
              </div>
            </div>
          </el-tab-pane>
          <el-tab-pane label="报表模式" name="formModel">
            <div style="width:70%; margin: auto;margin-top:20px">
              <div style="width: 600px;margin: auto;margin-left: 300px">
                <el-input v-model="queryMsg" placeholder="输入工号/姓名查询" style="width: 60%" ></el-input>
                <el-button icon="el-icon-search" circle style="margin-left: 5px" @click="queryStaffRecord"></el-button>
                <el-button style="width: 18%;margin-left: 80px;" @click="exportExcel">导出EXCEL</el-button>
              </div>
              <el-table ref="filterTable" :data="currentRecord" height='530' style="width: 100%;margin-top:30px" id="out-table">
                <el-table-column prop="staff_id" label="工号" width="180" ></el-table-column>
                <el-table-column prop="name" label="姓名" width="150" ></el-table-column>
                <el-table-column prop="department" label="部门" width="150"
                  :filters = createFilterDict(department) :filter-method="filterColum">
                </el-table-column>
                <el-table-column prop="status" label="状态" width="150" 
                  :filters = createFilterDict(recordStatus) :filter-method="filterColum">
                </el-table-column>
                <el-table-column prop="count" label="累计"></el-table-column>
              </el-table>
            </div>
          </el-tab-pane>
        </el-tabs>
        <el-popover placement="right" width="400" style="position:absolute;left:250px; top:83px" trigger="click">
          指定某个月
          <el-date-picker v-model="currentDateRange[0]" type="month" placeholder="选择查看的月份" value-format="yyyy-MM"
            @change="handelDateUpdate">
          </el-date-picker>
          或选择查看范围
          <!-- 日期范围的model是一个包含两个时间的数组 -->
          <el-date-picker v-model="currentDateRange" type="datetimerange" :picker-options="pickerOptions" range-separator="至"
           value-format="yyyy-MM-dd"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            align="right"
            @change="handelDateUpdate">
          </el-date-picker>
          <el-button slot="reference">
            {{recordDateRange()}}
          </el-button>
        </el-popover>
      </div>
    </div>
    <CopyrightFooter />
  </div>
</template>

<script>
import moment from "moment"; //moment.js时间格式
import { getAllAttRecord, getExRecordMsg, getDepartmentName } from "../assets/js/api";
import initStatus from "../assets/js/map";
import HeadMenu from "../components/HeadMenu.vue";
import CopyrightFooter from "../components/CopyrightFooter.vue";
import FileSaver from "file-saver";
import XLSX from "xlsx";

export default {
  name: "RecordPage",

  components: {
    HeadMenu,
    CopyrightFooter,
  },
  data() {
    const staffRecord = {
      staff_id: "S23333",
      name: "小明",
      status: "迟到",
      department: "销售",
      count: 3
    };
    return {
      currentDepartment: "全部",
      currentModelValue: 'diagramModel',//当前查看模式
      isDateRange:false,
      currentDateRange:['',''],//选择查看的日期范围,包含起始日期和截至日期
      selectedDay: "",    //选择查看的日期
      vaildDayInRecord:[], //有记录的日期
      recordStatus:initStatus.recordStatus,
      department: ["全部", "销售", "前台", "管理", "后勤"],
      queryMsg: "",
      monthRecord: {
        "2021-07-13": {
          attendance_num: 30,
          late_num: 3,
          early_leave_num: 2,
          absence_num: 1,
          leave_num: 4,
        },
        "2021-07-14": {
          attendance_num: 30,
          late_num: 2,
          early_leave_num: 3,
          absence_num: 5,
          leave_num: 1,
        },
      },
      currentMonthRecord: {
        "2021-07-13": {
          attendance_num: 30,
          late_num: 3,
          early_leave_num: 2,
          absence_num: 1,
          leave_num: 4,
        },
        "2021-07-14": {
          attendance_num: 30,
          late_num: 2,
          early_leave_num: 3,
          absence_num: 5,
          leave_num: 1,
        },
      },
      pickerOptions: {
          shortcuts: [{
            text: '最近一周',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近一个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30);
              picker.$emit('pick', [start, end]);
            }
          }, {
            text: '最近两个月',
            onClick(picker) {
              const end = new Date();
              const start = new Date();
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 60);
              picker.$emit('pick', [start, end]);
            }
          }
        ]
      },
      recordContainer: Array(20).fill(staffRecord),
      currentRecord:Array(5).fill(staffRecord),
      staffRecordMsgs: Array(2).fill(staffRecord),
    };
  },
  computed: {
    filterDepartment() {
      return this.department.filter((item) => item !== this.currentDepartment);
    },
    calculateDateRange(){
      // //格式要求，开始时间必须是周起始日，结束时间必须是周结束日，且时间跨度不能超过两个月
      let beg = moment(this.currentDateRange[0]).weekday(1).format('YYYY-MM-DD');
      let end = moment(this.currentDateRange[1]).weekday(7).format('YYYY-MM-DD');
      // console.log(beg, end);
      return [beg, end];
    }
  },
  methods: {
    handelDateUpdate(val){
      let dateRange='';
      this.isDateRange = val.length < 3;
      if(this.isDateRange)
        dateRange = val[0] + ' ' + val[1];
      else{
        dateRange = val;
        this.currentDateRange[1] = moment(val).endOf('month').format("YYYY-MM-DD");
        // console.log(this.currentDateRange[1]);
      }
      // console.log(val, dateRange);
      this.updateAllAttRecord(dateRange);
    },
    handelDateCellSelect(date) {
      // console.log(date.day)
      this.selectedDay = date.day;
      this.updateExRecordMsg(date.day);
    },
    queryStaffRecord(){
      if(this.queryMsg.trim().length<1){
        this.currentRecord = this.recordContainer;
        return;
      }
      let _value = this.queryMsg.trim().toLowerCase();
      // console.log(_value);
      let resultData = []; // 用于存放搜索出来数据的新数组
      if (_value) {
        this.recordContainer.filter(item => {
          if ((item.staff_id.toLowerCase().indexOf(_value) !== -1)||
          (item.name.toLowerCase().indexOf(_value) !== -1)) {
            resultData.push(item);
          }
        })
      }
      this.currentRecord = resultData;
    },
    //传入一个可迭代的类别数组对象，生成el-table-column的过滤器
    createFilterDict(_array){
      // console.log(_array)
      let results = []
      //表头类别是不需要的
      for(let i=1;i<_array.length;i++){
        let filterItem = {text: _array[i], value: _array[i]}
        // console.log(filterItem)
        results.push(filterItem)
      }
      return results;
    },
    filterColum(value, row, column){
      const property = column['property'];
      return row[property] === value;
    },
    updateAllAttRecord(dateRange) {
      // console.log(date)
      getAllAttRecord({
        company_name: this.$store.getters.companyName,
        date_range: dateRange,
      }).then((response) => {
        //获取了一个月的记录和统计信息
        if (response.status == 1) {
          // console.log(response.data);
          this.currentRecord = this.recordContainer = response.data.allAttRecord;
          this.currentMonthRecord = this.monthRecord = response.data.allAttRecordCount;
          this.vaildDayInRecord = [];
          for (let _record in this.currentMonthRecord) {
            this.vaildDayInRecord.push(_record);//同时获取有记录的日期
          }
          if(this.currentModelValue=='diagramModel')
            this.drawDiagram();
        } else {
          console.log(response.msg);
        }
      });
    },
    updateExRecordMsg(date) {
      getExRecordMsg({
        company_name: this.$store.getters.companyName,
        datetime: date
      }).then((response) => {
        if (response.status == 1) {
          this.staffRecordMsgs = response.data;
        } else {
          console.log(response.msg);
        }
      });
    },
    recordDateRange(){
      return this.isDateRange?
      moment(this.currentDateRange[0]).format('YYYY年M月D日') + ' 至 ' + moment(this.currentDateRange[1]).format('YYYY年M月D日')
      : moment(this.currentDateRange[0]).format('YYYY年M月')
    },
    recordDegree(date) {
      //date格式为yyyy-mm-dd
      let calRecord = this.currentMonthRecord[date];
      // console.log(date, calRecord)
      if (calRecord) {
        //比较late_num early_leave_num absence_num leave_num
        let ExNum =
          (calRecord.late_num?calRecord.late_num:0) +
          (calRecord.early_leave_num?calRecord.early_leave_num:0) +
          (calRecord.absence_num?calRecord.absence_num:0) +
          (calRecord.leave_num?calRecord.leave_num:0);
        // console.log(ExNum);
        if (ExNum > 5) return "严重";
        else if(ExNum > 1) return "异常";
        else return "正常";
      }
    },
    degreeColor(val){
      val = this.recordDegree(val);
      if (val === "严重"){
        return {'color':'red'}
        }
      else if (val === "异常"){
        return {'color':'orange'}
      }
      else if (val === "正常"){
        return {'color':'lightblue'}
      }
    },
    dataProcess() {
      //将monthRecord转化为echart可显示的数据
      var result = [];
      let _product = this.vaildDayInRecord;
      _product.unshift("product")
      let _attendance_num = ["出勤"];
      let _late_num = ["迟到"];
      let _early_leave_num = ["早退"];
      let _absence_num = ["缺勤"];
      let _leave_num = ["请假"];
      for (let _record in this.currentMonthRecord) {
        // console.log(this.monthRecord[_record].late_num, this.monthRecord[_record].early_leave_num,
        // this.monthRecord[_record].absence_num, this.monthRecord[_record].leave_num);
        _attendance_num.push(this.currentMonthRecord[_record].attendance_num);
        _late_num.push(this.currentMonthRecord[_record].late_num);
        _early_leave_num.push(this.currentMonthRecord[_record].early_leave_num);
        _absence_num.push(this.currentMonthRecord[_record].absence_num);
        _leave_num.push(this.currentMonthRecord[_record].leave_num);
      }
      result.push(_product);
      result.push(_attendance_num);
      result.push(_late_num);
      result.push(_early_leave_num);
      result.push(_absence_num);
      result.push(_leave_num);
      return result;
    },
    drawDiagram() {
      this.$nextTick(() => {
        let myChart = this.$echarts.init(document.getElementById("diagramChart"));

        let option = {
          legend: {},
          tooltip: {
            trigger: "axis",
          },
          dataset: {
            source: this.dataProcess(),
          },
          xAxis: { type: "category" },
          yAxis: { gridIndex: 0 },
          grid: { top: "55%" },
          dataZoom: [
            {
              // 这个dataZoom组件，默认控制x轴。
              type: "slider", // 这个 dataZoom 组件是 slider 型 dataZoom 组件
              start: 10, // 左边在 10% 的位置。
              end: 60, // 右边在 60% 的位置。
            },
          ],
          series: [
            { type: "line", smooth: true, seriesLayoutBy: "row" },
            { type: "line", smooth: true, seriesLayoutBy: "row" },
            { type: "line", smooth: true, seriesLayoutBy: "row" },
            { type: "line", smooth: true, seriesLayoutBy: "row" },
            { type: "line", smooth: true, seriesLayoutBy: "row" },
            {
              type: "pie",
              id: "pie",
              radius: "30%",
              center: ["50%", "25%"],
              label: {
                formatter: "{b} : ({d}%)",
              },
              encode: {
                itemName: "product",
                value: 2,
                tooltip: 2,
              },
            },
          ],
        };
        myChart.on("updateAxisPointer", function (event) {
          var xAxisInfo = event.axesInfo[0];
          if (xAxisInfo) {
            var dimension = xAxisInfo.value + 1;
            myChart.setOption({
              series: {
                id: "pie",
                label: {
                  formatter: "{b}: {@[" + dimension + "]} ({d}%)",
                },
                encode: {
                  value: dimension,
                  tooltip: dimension,
                },
              },
            });
          }
        });
        myChart.setOption(option);
      });
    },
    exportExcel() {
      /* 从表生成工作簿对象 */
      var wb = XLSX.utils.table_to_book(document.querySelector("#out-table"));
      /* 获取二进制字符串作为输出 */
      var wbout = XLSX.write(wb, {
        bookType: "xlsx",
        bookSST: true,
        type: "array"
      });
      try {
        FileSaver.saveAs(
        new Blob([wbout], { type: "application/octet-stream" }),
        //设置导出文件名称
        "record.xlsx"
        );
      } catch (e) {
          if (typeof console !== "undefined") console.log(e, wbout);
      }
      return wbout;
    }
  },
  mounted() {
    let _date = moment(new Date());
    this.selectedDay = moment(_date).format("YYYY-MM-DD");
    this.currentDateRange[0] = _date.startOf("month").format("YYYY-MM-DD");
    this.currentDateRange[1] = _date.endOf('month').format("YYYY-MM-DD");
    // console.log(this.currentDateRange[0], this.currentDateRange[1]);
    this.updateAllAttRecord(this.currentDateRange[0] + ' ' + this.currentDateRange[1]);
    this.updateExRecordMsg(this.selectedDay);
    //计算统计到的有效日期
    getDepartmentName({
        "company_name":this.$store.getters.companyName
        }).then((response)=>{
          if(response.status==1){
            this.department = response.data;
          }else{
            console.log(response.msg)
          }
          this.department.unshift('全部')
        }
      );
  },
};
</script>
<style scoped>
.calendarChart {
  width: 100%;
  background: papayawhip;
}
#diagramChart {
  width: 100%;
  height: 570px;
  background: papayawhip;
}
</style>

<style>
.calendarChart .el-calendar-table .el-calendar-day {
  height: 68px;
}
</style>