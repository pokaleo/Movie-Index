
<template>
   <suspense>
  <router-view :key="$route.fullPath"></router-view>
  </suspense>
</template>

<style >
html,
body,
#app {
  height: 100%;
  width: 100%;
  padding: 0;
  margin: 0;
}
</style>
