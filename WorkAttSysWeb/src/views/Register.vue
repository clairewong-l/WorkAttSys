<template style="height:100%">
  <div class="register">
    <div class="rg-layout">
      <el-form
        :model="ruleForm"
        status-icon
        :rules="rules"
        ref="ruleForm"
        label-width="100px"
        class="demo-ruleForm"
      >
        <header>
          <div class="headerContent">
            <el-button-group>
              <el-button
                :class="[title === 1 ? 'active' : '']"
                @click="changeTitle(1)"
                >HR注册</el-button
              >
              <!-- <el-button
                :class="[title === 2 ? 'active' : '']"
                @click="changeTitle(2)"
                >Staff</el-button
              > -->
            </el-button-group>
            <span class="active"></span>
            <span></span>
          </div>
        </header>
        <el-form-item label="工号" prop="cardId">
          <el-input v-model="ruleForm.cardId"></el-input>
        </el-form-item>
        <el-form-item label="姓名" prop="name">
          <el-input v-model="ruleForm.name"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
          <el-input v-model="ruleForm.pass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="ruleForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="公司全称" prop="companyName">
          <el-input v-model="ruleForm.companyName"></el-input>
        </el-form-item>
        <el-form-item label="公司法人" prop="companyManager">
          <el-input v-model="ruleForm.companyManager"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button @click="submitForm('ruleForm')">注册</el-button>
          <el-button @click="resetForm('ruleForm')">取消</el-button>
          <el-button @click="()=>{$router.push('/')}">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
    <el-dialog
      title="注册成功"
      :visible.sync="centerDialogVisible"
      width="30%"
      center
    >
      <span>注册成功,去登录</span>
      <span slot="footer" class="dialog-footer">
        <el-button
          type="primary"
          @click="
            () => {
              $router.push('/');
            }
          "
          >登录</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>
<script>
import { register } from "@/assets/js/register";
import axios from 'axios';
export default {
  data() {
    // var checkAge = (rule, value, callback) => {
    //   if (!value) {
    //     return callback(new Error("年龄不能为空"));
    //   }
    //   setTimeout(() => {
    //     if (!Number.isInteger(value)) {
    //       callback(new Error("请输入数字值"));
    //     } else {
    //       if (value < 18) {
    //         callback(new Error("必须年满18岁"));
    //       } else {
    //         callback();
    //       }
    //     }
    //   }, 1000);
    // };
    const validateCardId = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入工号"));
        return;
      }
      callback();
    };
    const validateName = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入姓名"));
        return;
      }
      callback();
    };
    const validatePass = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入密码"));
        return;
      }
      callback();
    };
    const validatePhone = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入手机号"));
        return;
      }
      callback();
    };
    const validateCompanyName = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入公司全称"));
        return;
      }
      callback();
    };
    const validateCompanyManager = (rule, value, callback) => {
      if (value === "") {
        callback(new Error("请输入公司法人"));
        return;
      }
      callback();
    };

    return {
      centerDialogVisible: false,
      ruleForm: {
        cardId: "",
        name: "",
        pass: "",
        phone: "",
        companyName: "",
        companyManager: "",
      },
      title: 1,
      rules: {
        pass: [{ validator: validatePass, trigger: "blur" }],
        cardId: [{ validator: validateCardId, trigger: "blur" }],
        name: [{ validator: validateName, trigger: "blur" }],
        phone: [{ validator: validatePhone, trigger: "blur" }],
        companyName: [{ validator: validateCompanyName, trigger: "blur" }],
        companyManager: [
          { validator: validateCompanyManager, trigger: "blur" },
        ],
      },
    };
  },
  methods: {
    changeTitle(params) {
      this.title = params;
    },
     submitForm(formName) {

      
      this.$refs[formName].validate((valid) => {
        if (valid) {
          register(this.ruleForm).then((res) => {
            if(res.data.status==1){
             this.centerDialogVisible=true;
            }else{
               this.$notify({
                message: '注册失败',
                type: 'warning'
              });
            }
          })
          .catch(err => {
              console.log(err)

          })  
          // register(this.ruleForm).then((res) => {
          //   console.log("zheli ")
          //   console.log(res)
          //   if ( res.status == 1) {
          //     this.centerDialogVisible = true;
          //     console.log("这里")
          //     that.$notify({
          //       title: '成功',
          //       message: '这是一条成功的提示消息',
          //       type: 'success'
          //     });
              
          //     return;
          //   }
          //   that.$Message.error("注册失败")
          //   alert("注册失败");
          // });
      //   } else {
      //     console.log("error submit!!");
      //     return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    },
  },
};
</script>
<style lang="less" scoped>
.register {
  background: #d0c8c8;
  display: flex;
  height: 100vh;
  align-items: center;
  justify-content: center;
  .rg-layout {
    width: 400px;
    background: #fff;
    padding: 20px;
    display: flex;
    box-shadow: 10px 10px 20px 10px #999;
    border-radius: 4px;
    border: solid 1px #999;
  }
  header {
    margin-left: 100px;
    margin-bottom: 40px;
    border-radius: 6px !important;
    background: whitesmoke;
    display: inline-block;
    .el-button {
      font-size: 24px;
      font-weight: 600;
      padding-left: 0;
      padding-right: 0;
      width: 120px;
      background: whitesmoke;
      border: 0;
      &.active {
        background: papayawhip;
        border-radius: 6px !important;
      }
    }
  }
}
</style>