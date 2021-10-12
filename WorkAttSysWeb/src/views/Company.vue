<template>
  <div class="cominformation"
  style="margin-top:60px">
   

    <el-table
    :data="time_settings"
    highlight-current-row
    v-loading="listLoading"
   
    >
    
    <el-table-column type="selection"> </el-table-column>
    <el-table-column type="index"> </el-table-column>
    <el-table-column prop="test" label="             " width="200px" sortable> </el-table-column>
    <el-table-column prop="late_period" label="限定迟到时间段/小时" width="400px" sortable> </el-table-column>
    <el-table-column prop="early_period" label="限定缺勤时间段/小时" width="400px"> </el-table-column>
    <el-table-column label="操作" width="150">
        <template scope="scope">
        <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
            >编辑</el-button>
        </template>
    </el-table-column>  
    </el-table>

    <!--编辑界面-->
    <el-dialog
      title="编辑"
      :visible.sync="editFormVisible"
      :close-on-click-modal="false"
    >
      <el-form
        :model="editForm"
        label-width="200px"
        :rules="editFormRules"
        ref="editForm"
      >
        <el-form-item label="限定迟到时间段/小时" prop="late_period">
          <el-input v-model.number="editForm.late_period" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="限定早退时间段/小时" prop="early_period">
          <el-input v-model.number="editForm.early_period" auto-complete="off"></el-input>
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
        label-width="200px"
        :rules="addFormRules"
        ref="addForm"
      >
        <el-form-item label="限定迟到时间段/小时" prop="late_period">
          <el-input v-model="editForm.late_period" auto-complete="off"></el-input>
        </el-form-item>
        <el-form-item label="限定早退时间段/小时" prop="early_period">
          <el-input v-model="editForm.early_period" auto-complete="off"></el-input>
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
  getTime,
  updateTime
} from  "@/assets/js/api";
export default {
  data() {
    return {
     
      time_settings: [
        {
          late_period: "1",
          early_period: "1",
          
        },
      ],
      total: 0,
      page: 1,
      listLoading: false,
      sels: [], //列表选中列
      editFormVisible: false, //编辑界面是否显示
      editLoading: false,
      editFormRules: {
        late_period: [{ required: true,type:"number" ,min: 0, max: 5, message: "请输入限定迟到时间段(0-5)", trigger: "blur" }],
        early_period: [{ required: true,type:"number" ,min: 0, max: 5, message: "请输入限定早退时间段(0-5)", trigger: "blur" }],
      },
      //编辑界面数据
      editForm: {
        id: 1,
        late_period: "",
        early_period: "",
        
      },
      addFormVisible: false, //新增界面是否显示
      addLoading: false,
      addFormRules: {
        late_period: [{ required: true, message: "请输入限定迟到时间段", trigger: "blur" }],
        early_period: [{ required: true, message: "请输入限定早退时间段", trigger: "blur" }],
      },
      //新增界面数据
      addForm: {
        late_period: "",
        early_period: "",

      },
    };
  },

  methods:{

    getTimeData() {
      getTime({ company_name: this.$store.getters.companyName }).then((res) => {
        console.log(res.data);
        if (res.status == 1) {
          this.time_settings = res.data;
          this.total = res.total;
          return;
        }
        
      });
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
      this.addForm = {
        late_period: "",
        early_period: "",
        
      };
    },

    //编辑
     editSubmit: function () {
      this.$refs.editForm.validate((valid) => {
        if (valid) {
          this.$confirm("确认提交吗？", "提示", {}).then(() => {
            this.editLoading = true;
            //NProgress.start();
            let para = Object.assign({}, this.editForm);
            console.log(para);
            updateTime({para, company_name: this.$store.getters.companyName }).then((res) => {
              console.log(res);
              this.editFormVisible = false;
              this.editLoading = false;
              if(res.status===1){
                this.$message({
                message: "编辑成功",
                type: "success",
              });
              }
              else{
                this.$message({
                message: "编辑失败",
                type: "success",
              });
              }
              this.getTimeData();
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
            addTime(para).then((res) => {
              this.addLoading = false;
              //NProgress.done();
              this.$message({
                message: "提交成功",
                type: "success",
              });
              this.$refs["addForm"].resetFields();
              this.addFormVisible = false;
              this.getTimeData();
            });
          });
        }
      });
    },
  },
  mounted() {
    this.getTimeData();    
  },
    
    
  
};
  
</script>