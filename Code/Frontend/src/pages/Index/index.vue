!<!--  -->
<template>
  <div class='container'>
    <div class="header">
      <!--input class="iconfont search_input " type="text" placeholder="search"-->
      <SearchBar/>
    </div>
    <div class="content">
      <div class="big-title">
        Did you mean: <i>Funny movie</i> or <i>Fun movie</i>?
      </div>
      <div class="movie-list">
        <div class="movie-item" v-for="(item, index) in movieList" :key="index" @click="goMovieDetailPage(item.id)">
          <div class="movie-name">{{ item.movieName }}</div>
          <div class="movie-description">{{ item.description }}</div>
          <div class="movie-info">
            <span>Director:{{ item.director }} • </span>
            <span>Year: {{ item.year }} • </span>
            <span>Country:{{ item.country }} • </span>
            <span>Runtime:{{ item.runtime }}</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang='ts'>
import { reactive } from 'vue';
import { useRouter } from "vue-router"
import SearchBar from '../MovieDetail/SearchBar.vue';

const router = useRouter()
const movieList = reactive([
  {
    id: 1,
    movieName: "Monsieur Vincent",
    description: "St. Vincent de Paul struggles to bring about peace and harmony among the peasant and the nobles in the midst of the Black Death in Europe, carrying on his charitable work in the face of all obstacies...",
    director: "David Johnson",
    year: "1987",
    country: "United Kingdom",
    runtime: '117'
  },
  {
    id: 2,
    movieName: "Another Movie",
    description: "A fantastic movie describe...",
    director: "Willam Dart",
    year: "1966",
    country: "United States",
    runtime: '178'
  },
  {
    id: 3,
    movieName: "Cute cat",
    description: "A cat movie which was directed by a famous director, and .....",
    director: "Jake Craig",
    year: "1998",
    country: " France",
    runtime: '98'
  }
])

/**
 * 跳转电影详情页面
 * @param movieId 
 */
const goMovieDetailPage = (movieId: string | number) => {
  router.push("/detail/" + movieId)
}
</script>

<style scoped lang="less">
.container {
  height: 100%;
  width: 100%;
  padding-top: 0px;
  box-sizing: border-box;
}
.header{
  background-color: black;
  text-align: center;
}

.content {
  width: 600px;
  height: 300px;
  margin: 0 auto;
  margin-top: 30px;

  .big-title {
    font-weight: bold;
    padding-left: 20px;
    box-sizing: border-box;

    i {
      color: blue;
    }
  }

  .movie-list {
    height: 400px;
    overflow-y: auto;

    .movie-item {
      border: 1px solid #000;
      padding: 10px 24px;
      box-sizing: border-box;
      margin: 10px 0;
      background-color: #eee;
      cursor: pointer;

      .movie-name {
        color: blue;
      }

      .movie-description {
        font-size: 12px;
        min-height: 50px;
        padding: 2px 0;
      }

      .movie-info {
        font-weight: bold;
        font-size: 12px;
      }
    }
  }

}
</style>