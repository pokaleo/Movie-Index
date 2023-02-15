<template>
    <div id="KeyWordsBar">
      <div class="sidebar">
        <div class="sidebar-content">
          <div class="sidebar-header">
            <p>Keywords</p>
          </div>
          <el-divider class="sidebar-divider"/>
          <div class="sidebar-body">
            <el-scrollbar height="450px">
            <el-space direction="vertical">
            <el-tag
                class="tag"
                v-for="keyword in keywords"
                :key="keyword"
            >
            {{keyword}}
            </el-tag>
          </el-space>
          </el-scrollbar>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
export default{
    name: "KeyWordsBar",
    props:['keywords'],
    data() {
        return{
            //keywords: ['keyword1','keyword2', 'keyword3']
        }
    }
}
</script>

<style scoped>

.sidebar{
    display: flex;
    flex-direction: column;
    width: 200px;
    justify-items: center;
    align-items: center;
    font-family:Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
}

p{
    font-style: oblique;
    font-size: x-large;
    font-weight:200;
}
.sidebar-body{
    flex-direction: column;
    flex-wrap: wrap;
}
.tag{
    background-color: whitesmoke;
    border-radius: 10px;
    margin-top: 10px;
    margin: 5px;
    color: black;
    font-size: small;
    border-color: darkgray;
}
</style>