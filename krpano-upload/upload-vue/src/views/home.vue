<template>
  <div>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>Krpano 全景服务在线生成</span>
        <el-button style="float: right; padding: 3px 0" type="text" @click="submitUpload()" :disabled="disabled">立即合成
        </el-button>
      </div>
      <div style="float: left;margin-bottom: 15px;padding-left: 5px">
        <div style="float: left;line-height: 40px">作品名称：</div>
        <div style="float: left">
          <el-input style="float: left" v-model="title" placeholder="请输入作品名称"></el-input>
        </div>
      </div>
      <div style="float: left;margin-bottom: 15px;padding-left: 5px">
        <div style="float: left;line-height: 40px">作品作者：</div>
        <div style="float: left">
          <el-input style="float: left" v-model="author" placeholder="请输入作品作者"></el-input>
        </div>
      </div>
      <div style="">
        <el-upload
            class="upload-demo"
            ref="upload"
            action="http://1.13.15.226:8000/upload_image"
            :file-list="fileList || []"
            list-type="picture"
            :auto-upload=false
            :on-change="handleChange"
            :on-remove="handleChange"
            multiple
            drag
        >
          <i class="el-icon-upload"></i>
          <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        </el-upload>
      </div>

    </el-card>
    <el-card class="preview-card" v-show="screenVisible">
      <iframe :src=url style="border:none;outline:none;width: 100%;height: 81vh;border-radius: 12px;"></iframe>
    </el-card>
  </div>
</template>


<script>
import {createVR, submitIMG} from "../api/index.js"

export default {
  name: "Home",
  data() {
    return {
      title: '',
      author: '',
      fileList: [],
      url: '',
      disabled: true,
      screenVisible: false,
      formData: [],
      loading: ''
    };
  },
  computed: {
    options() {
      const {title, author, fileList} = this
      return {title, author, fileList}
    }
  },
  watch: {
    options: {
      handler() {
        if (this.title != '' && this.author != '' && this.fileList.length != 0) {
          this.disabled = false
        } else {
          this.disabled = true
        }
      }
    }
  },
  methods: {
    //手动模拟提交上传
    submitUpload() {
      let that = this;
      that.loading = this.$loading({
        lock: true,
        text: '正在生成全景服务',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      });
      let formData = new FormData();  //  用FormData存放上传文件
      formData.append('title', this.title)
      this.fileList.forEach(file => {
        formData.append('file', file.raw)
      })
      // 调用上传接口
      submitIMG(formData).then((res) => {
        this.create()
      })
    },
    handleChange(file, fileList) {
      this.fileList = fileList.slice(-3);
    },
    create() {
      let that = this;
      createVR().then((res) => {
        that.url = res;
        that.screenVisible = true;
        that.loading.close();
      })
    }
  }
}
</script>

<style scoped lang="scss">
.box-card {
  width: 405px;
  margin-left: 5%;
  margin-top: 3%;
  float: left;
}

.preview-card {
  width: 1200px;
  height: 85vh;
  margin-top: 3%;
  position: absolute;
  right: 50px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both
}
</style>
