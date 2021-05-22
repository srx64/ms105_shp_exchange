<template>
  <div class="hexagon hexagon1">
    <div class="hexagon-in1">
      <div class="hexagon-in2"/>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'TestForm',
  }
</script>

<style scoped>
  .hexagon {
    overflow: hidden;
    visibility: hidden;
    transform: rotate(120deg);
  }
  .hexagon-in1 {
    overflow: hidden;
    width: 100%;
    height: 100%;
    transform: rotate(-60deg);
  }
  .hexagon-in2 {
    width: 100%;
    height: 100%;
    background-repeat: no-repeat;
    background-position: 50%;
    background-image: url(http://placekitten.com/240/240);
    visibility: visible;
    transform: rotate(-60deg);
  }
  .hexagon1 {
    width: 400px;
    height: 200px;
    margin: 0 0 0 -80px;
  }
</style>