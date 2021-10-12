<template>
  <div class="Deptinformation">
    <!--工具条-->
    <el-col class="toolbar" style="padding-bottom: 0px;margin-top:30px">
      <el-form :inline="true" :model="filters">
        
        <el-form-item>
          <el-input
            v-model="filters.dept_name"
            placeholder="部门名称"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getDepts">查询</el-button>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增</el-button>
        </el-form-item>
        <el-form-item>
          <el-button
          type="danger"
          @click="batchRemove"
          :disabled="this.sels.length === 0"
          >批量删除</el-button>
        </el-form-item>
      </el-form>
    </el-col>
    <!--列表-->
    <el-table
      :data="users"
      height="600px"
      highlight-current-row
      v-loading="listLoading"
      @selection-change="selsChange"
      

    >
      <el-table-column type="selection"> </el-table-column>
      <el-table-column type="index"> </el-table-column>
      <el-table-column prop="dept_id" label="部门编号" width="110px" margin-left="20px" sortable> </el-table-column>
      <el-table-column prop="dept_name" label="部门名称" width="100px"> </el-table-column>
      <el-table-column prop="wage_h" label="时薪" width="100px"> </el-table-column>
      <el-table-column prop="overtime_pay_h" label="加班时薪" width="100px">
      </el-table-column>
      <el-table-column prop="s_time" label="上班时间" width="110px"> </el-table-column>
      <el-table-column prop="e_time" label="下班时间" width="110px"> </el-table-column>
      <el-table-column prop="r_time" label="中午休息时间" width="110px"> </el-table-column>
      <el-table-column prop="late_times" label="限定迟到次数" width="110px">
      </el-table-column>
      <el-table-column prop="vacation_days" label="限定年假天数" width="110px">
      </el-table-column>
      <el-table-column prop="absent_times" label="限定缺勤次数" width="110px">
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template scope="scope">
          <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button
            
            >
          <el-button
            type="danger"
            size="small"
            @click="handleDel(scope.$index, scope.row)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <!--工具条-->
    <el-col :span="24" class="toolbar">
     
    </el-col>

    <!--编辑界面-->
    <el-dialog
      title="编辑"
      :visible.sync="editFormVisible"
      :close-on-click-modal="false"
    >
      <el-form
        :model="editForm"
        label-width="80px"
        :rules="editFormRules"
        ref="editForm"
      >
        <el-form-item label="部门编号" prop="dept_id">
          <el-input v-model="editForm.dept_id" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="部门名称" prop="dept_name">
          <el-input v-model="editForm.dept_name" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="时薪" prop="wage_h">
          <el-input v-model="editForm.wage_h" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="加班时薪" prop="overtime_pay_h">
          <el-input
            v-model="editForm.overtime_pay_h"
            auto-complete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="上班时间" prop="s_time">
          <el-input v-model="editForm.s_time" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="下班时间" prop="e_time">
          <el-input v-model="editForm.e_time" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="中午休息时间" prop="r_time">
          <el-input v-model="editForm.r_time" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="限定迟到次数" prop="late_times">
          <el-input
            v-model="editForm.late_times"
            auto-complete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="限定年假天数" prop="vacation_days">
          <el-input
            v-model="editForm.vacation_days"
            auto-complete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="限定缺勤次数" prop="absent_times">
          <el-input
            v-model="editForm.absent_times"
            auto-complete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="editFormVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click.native="editSubmit"
          :loading="editLoading"
          >提交</el-button
        >
      </div>
    </el-dialog>

    <!--新增界面-->
    <el-dialog
      title="新增"
      :visible.sync="addFormVisible"
      :close-on-click-modal="false"
    >
      <el-form
        :model="addForm"
        label-width="80px"
        :rules="addFormRules"
        ref="addForm"
      >
        <el-form-item label="部门编号" prop="dept_id">
          <el-input v-model="addForm.dept_id" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="部门名称" prop="dept_name">
          <el-input v-model="addForm.dept_name" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="时薪" prop="wage_h">
          <el-input v-model="addForm.wage_h" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="加班时薪" prop="overtime_pay_h">
          <el-input
            v-model="addForm.overtime_pay_h"
            auto-complete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="上班时间"  prop="s_time">
          <el-input v-model="addForm.s_time" type="time" value-format="HH:mm:ss" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="下班时间" prop="e_time">
          <el-input v-model="addForm.e_time" type="time" value-format="HH:mm:ss" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="中午休息时间" prop="r_time">
          <el-input v-model="addForm.r_time" type="time" value-format="HH:mm:ss" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="限定迟到次数" prop="late_times">
          <el-input
            v-model="addForm.late_times"
            auto-complete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="限定年假天数" prop="vacation_days">
          <el-input
            v-model="addForm.vacation_days"
            auto-complete="off"
          ></el-input>
        </el-form-item>
        <el-form-item label="限定缺勤次数" prop="absent_times">
          <el-input
            v-model="addForm.absent_times"
            auto-complete="off"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click.native="addFormVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click.native="addSubmit"
          :loading="addLoading"
          >提交</el-button
        >
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {
  getDepartment,
  updateDepartment,
  deleteDepartment,
  addDepartment
} from "@/assets/js/api";
export default {
  data() {
    return {
      options: [
        {
          value: "dept1",
          label: "部门一",
        },
        {
          value: "dept2",
          label: "部门二",
        },
      ],
      filters: {
        dept_id: "",
        dept_name: "",
      },
      users: this.$users,
      
      
      listLoading: false,
      sels: [], //列表选中列
      editFormVisible: false, //编辑界面是否显示
      editLoading: false,
      editFormRules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
      },
      //编辑界面数据
      editForm: {
          dept_id: "",
          dept_name: "",
          wage_h: '',
          overtime_pay_h: '',
          s_time: "",
          e_time: "",
          r_time: "",
          late_times: '',
          vacation_days: '',
          absent_times: '',
      },
      addFormVisible: false, //新增界面是否显示
      addLoading: false,
      addFormRules: {
        name: [{ required: true, message: "请输入姓名", trigger: "blur" }],
      },
      //新增界面数据
      addForm: {
          dept_id: "",
          dept_name: "",
          wage_h: '',
          overtime_pay_h: '',
          s_time: "",
          e_time: "",
          r_time: "",
          late_times: '',
          vacation_days: '',
          absent_times: '',
      },
    };
  },
  methods: {
     getDepartmentData() {
      getDepartment({  company_name: this.$store.getters.companyName}).then((res) => {
          // console.log(this.$store.getters.companyName);
          if ( res.status == 1) {
          this.users = res.data;
          this.total = res.total;
          console.log(this.users);
          console.log("你好急急急");
          return;
       }
      });
    },
    
    
    handleCurrentChange(val) {
      this.page = val;
      this.getDepts();
    },
    getDepts() {
    	let para = {
    		page: this.page,
    		dept_name: this.filters.dept_name,
        
    	};
    	this.listLoading = true;
      
    	getDepartment({ filters:this.filters, company_name: this.$store.getters.companyName}).then((res) => {
    		this.total = res.total;
    		this.users = res.data;
        this.options = res.options;
    		this.listLoading = false;
        console.log("这里呀",this.options);
    		//NProgress.done();
    	});
    },
   
    //删除
    handleDel: function (index, row) {
      console.log(row,"则例");
      this.$confirm("确认删除该记录吗?", "提示", {
        type: "warning",
      })
        .then(() => {
          this.listLoading = true;
          //NProgress.start();
          let para = { dept_id: row.dept_id };
          deleteDepartment(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            this.$message({
              message: "删除成功",
              type: "success",
            });
            this.getDepartmentData();
          });
        })
        .catch(() => {});
    },
    //显示编辑界面
    handleEdit: function (index, row) {
      this.editFormVisible = true;
      this.editForm = Object.assign({}, row);
      console.log(this.editForm);
    },
    //显示新增界面
    handleAdd: function () {
      this.addFormVisible = true;
      // this.addForm = {
      //   staff_id: "",
      //   name: "",
      //   sex: -1,
      //   department: "",
      //   job_type_id: "",
      //   annual_freedays: "",
      //   entry_time: "",
      // };
    },
    //编辑
    editSubmit: function () {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm("确认提交吗？", "提示", {}).then(() => {
            this.editLoading = true;
            //NProgress.start();
            let para = Object.assign({}, this.editForm);
            updateDepartment(para).then((res) => {
              console.log(res);
            this.editFormVisible = false;
            this.editLoading = false;
              this.$message({
                message: "编辑成功",
                type: "success",
              });
              this.getDepartmentData();
            });
          });
        }
      });
    },
    //新增
    addSubmit: function () {
      this.$refs.addForm.validate((valid) => {
        if (valid) {
          this.$confirm("确认提交吗？", "提示", {}).then(() => {
            this.addLoading = true;
            //NProgress.start();
            let para = Object.assign({}, this.addForm);
            para.birth =
              !para.birth || para.birth == ""
                ? ""
                : util.formatDate.format(new Date(para.birth), "yyyy-MM-dd");
            addDepartment({para,company_name: this.$store.getters.companyName} ).then((res) => {
              this.addLoading = false;
              //NProgress.done();
              this.$message({
                message: "提交成功",
                type: "success",
              });
              this.$refs["addForm"].resetFields();
              this.addFormVisible = false;
              this.getDepartmentData();
            });
          });
        }
      });
    },
    selsChange: function (sels) {
      this.sels = sels;
    },
    //批量删除
    batchRemove: function () {
      var ids = this.sels.map((item) => item.id).toString();
      this.$confirm("确认删除选中记录吗？", "提示", {
        type: "warning",
      })
        .then(() => {
          this.listLoading = true;
          //NProgress.start();
          let para = { ids: ids };
          deleteDepartment(para).then((res) => {
            this.listLoading = false;
            //NProgress.done();
            this.$message({
              message: "删除成功",
              type: "success",
            });
            this.getDepartmentData();
          });
        })
        .catch(() => {});
    },
  },
  mounted() {
    this.getDepartmentData();
  },
};
</script>

<style>
</style>