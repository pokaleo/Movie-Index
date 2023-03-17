<template>
  <div class="hello">
    <h1 class="title">Movie Index</h1>
    <div>
      <img src="@/assets/logo.png" alt="search" class="logo"/>
    </div>

    <div class="inputQuery">
      <SearchBar :t="'any'"/>
      <!--el-button size="small" @click="sendQuery" style="margin-top:20px">Search</el-button-->
    </div>
    <div class="footer">
      <a :href="'https://doc.movieindex.me'">Documentation: see https://doc.movieindex.me</a>
    </div>
  </div>
</template>

<script>
import SearchBar from './SearchBar.vue';
export default {
  name: 'LoadingView',
  components:{
    SearchBar
  },
  props: {
    msg: String
  },
  
  data() {
    return{
      query: "",
      results: "",
      mode:"title",
    }
  },

  methods:{
    sendQuery(){
      const path = 'http://localhost:8800/test'
      let postMsg = { query: this.query}
      console.log(postMsg)
      //print(this.query)
      this.axios.post(path, postMsg)
        .then(response => {
          this.results = response.data.results
          console.log(response.data)
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
.hello{
  display: flex;
  flex-direction: column;
  text-align: center;
  min-height: 100%;
}
.logo{
  width: 200px;
  height: 200px;
  align-self: center;
}

.title{
  font-size: 72px;
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
}
.inputQuery{
  margin-top: 2%;
  flex: 1;
}

.footer{
  margin-bottom: 7px;
  flex: 0;
  font-size: x-small;
}
</style>
