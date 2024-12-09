<template>
  <div>
    <h1>欢迎来到知识图谱</h1>
    <input v-model="customCypher" placeholder="请输入Cypher语句" style="width: 300px; margin-bottom: 20px;"/>
    <button @click="executeCypher">执行查询</button>
    <div id="viz"></div>
  </div>
</template>

<script>
import NeoVis from 'neovis.js/dist/neovis.js';

export default {
  name: 'NeovisComponent',
  data() {
    return {
      customCypher: "MATCH (a:Symptom)-[r]->(b:SleepDisorder {name: '失眠'}) RETURN a, r, b LIMIT 50"
    };
  },

  mounted() {
    this.$nextTick(() => {
      this.draw();
    });
  },
  methods: {
    draw() {
      const config = {
        container_id: 'viz',
        server_url: 'bolt://10.21.168.134:7687',
        server_user: 'neo4j',
        server_password: 'zyl1233',
        labels: {
          "Complication": { caption: 'name', size: 30, font: { size: 12, color: '#2196F3' } }, // 蓝色
          "DiagnosticStandard": { caption: 'name', size: 30, font: { size: 12, color: '#F44336' } }, // 红色
          "RelatedDisease": { caption: 'name', size: 30, font: { size: 12, color: '#8BC34A' } }, // 绿色
          "Risks": { caption: 'name', size: 30, font: { size: 12, color: '#FFEB3B' } }, // 黄色
          "SleepDisorder": { caption: 'name', size: 30, font: { size: 12, color: '#FF9800' } }, // 橙色
          "Symptom": { caption: 'name', size: 30, font: { size: 12, color: '#9C27B0' } }, // 紫色
          "Test": { caption: 'name', size: 30, font: { size: 12, color: '#607D8B' } }, // 蓝灰色
          "Treatment": { caption: 'name', size: 30, font: { size: 12, color: '#795548' } } // 棕色
        },
        relationships: {
          "ASSOCIATED_WITH": { caption: true, thickness: 1, color: '#BDBDBD' }, // 灰色
          "COOCCURS_WITH": { caption: true, thickness: 2, color: '#FF5722' }, // 深橙色
          "DIAGNOSED_BY": { caption: true, thickness: 2, color: '#3F51B5' }, // 深蓝色
          "INFLUENCES_RISK_OF": { caption: true, thickness: 2, color: '#CDDC39' }, // 亮绿色
          "RECOMMENDED_FOR": { caption: true, thickness: 2, color: '#FF9800' } // 橙色
        },
        initial_cypher: this.customCypher,
        arrows: true,
        hierarchical: true,
        hierarchical_sort_method: 'directed',
        zoomExtents: true // 启用缩放和平移
      };

      const viz = new NeoVis(config);
      viz.render();
    },
    executeCypher() {
      this.draw();
    }
  }
}
</script>

<style scoped>
#viz {
  width: 100%;
  height: 600px;
  border: 1px solid #ccc;
  margin-top: 20px;
  overflow: hidden; /* 防止溢出 */
}
h1 {
  text-align: center;
  margin-top: 50px;
}
</style>
