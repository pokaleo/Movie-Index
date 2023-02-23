<template>
  <div id="SearchBar" class="searchbar">
      
      <el-input
        class="text"
        placeholder="Please input your query"
        v-model="query.queryMsg"
        style="width: 40%">
      </el-input>
      
      <select v-model="query.selected" class="selected">
        <option value="title">by title</option>
        <option value="cast">by cast</option>
        <option value="country">by country</option>
      </select>
    
      <!--router-link :to="'/result/'+selected+'/'+query"-->
      <el-button
        class="searchButton"
        @click="goSearchResult"
      >
        <img src="@/assets/svg/icons8-search.svg" alt="search">
      </el-button>
      <!--/router-link-->
  </div>
</template>

<script>
import { defineComponent,ref,reactive } from 'vue';
import { useRouter } from "vue-router"

export default defineComponent({
  name: "SearchBar",
  props: {
    q: String,
    t: String,
  },
  //emits: ["update:modelValue"],
  setup(props){
    const router = useRouter()
    var query = reactive({queryMsg:props.q, selected:props.t})
    //console.log("props"+props.q)
    //let queryMsg = ref("")
    //let selected = ref("title")
    //query.queryMsg = props.q
    //query.selected = props.t !=""? props.t :"title"

    function goSearchResult(){
      router.push({path:"/search",query:{q:query.queryMsg, t:query.selected}})
    }

    return{
      query,
      goSearchResult
    }
  }
});
</script>

<style lang="scss" scoped>
.text{
  width: 40%;
  height: 35px;
  outline: hidden;
  margin: auto;
  border: 1px solid black;
  background: white;
}
.searchButton{
  background: white;
}

.selected{
  height: 35px;
  background-color: white;
}

img{
  width: 20px;
}
</style>