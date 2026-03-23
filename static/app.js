document.addEventListener("DOMContentLoaded", function(){

  let selectedModel = "rf";
  let chart = null;
  
  const form = document.getElementById("params-form");
  const paramsCard = document.getElementById("params-card");
  const resultsSection = document.getElementById("results");
  
  const navParams = document.getElementById("nav-params");
  const navResults = document.getElementById("nav-results");
  
  const modelButtons = document.querySelectorAll(".model-btn");
  const previewRisk = document.getElementById("preview-risk");
  const modelDesc = document.getElementById("model-desc");
  
  const riskPercent = document.getElementById("risk-percent");
  const resultRing = document.getElementById("result-ring");
  const riskBadge = document.getElementById("risk-badge");
  
  const resetBtn = document.getElementById("reset-btn");
  const backBtn = document.getElementById("back-btn");
  
  const rawTable = document.getElementById("raw-values");
  const chartCanvas = document.getElementById("paramsChart");
  
  
  navParams.addEventListener("click",function(e){
  e.preventDefault();
  paramsCard.classList.remove("hidden");
  resultsSection.classList.add("hidden");
  });
  
  navResults.addEventListener("click",function(e){
  e.preventDefault();
  paramsCard.classList.add("hidden");
  resultsSection.classList.remove("hidden");
  });
  
  
  modelButtons.forEach(function(btn){
  
  btn.addEventListener("click",function(){
  
  modelButtons.forEach(function(b){
  b.classList.remove("active");
  });
  
  btn.classList.add("active");
  selectedModel = btn.dataset.model;
  
  if(selectedModel === "rf"){
  modelDesc.textContent = "Random Forest — ensemble tree model";
  }else{
  modelDesc.textContent = "ANN — neural network prediction model";
  }
  
  });
  
  });
  
  
  resetBtn.addEventListener("click",function(){
  form.reset();
  previewRisk.textContent = "—";
  });
  
  
  backBtn.addEventListener("click",function(){
  resultsSection.classList.add("hidden");
  paramsCard.classList.remove("hidden");
  });
  
  
  form.addEventListener("submit",async function(e){
  
  e.preventDefault();
  
  const formData = new FormData(form);
  let data = {};
  
  formData.forEach(function(value,key){
  data[key] = Number(value);
  });
  
  data.model = selectedModel;
  
  try{
  
  const response = await fetch("/predict",{
  method:"POST",
  headers:{
  "Content-Type":"application/json"
  },
  body:JSON.stringify(data)
  });
  
  const result = await response.json();
  showResults(result,data);
  
  }catch(err){
  console.error(err);
  alert("Prediction failed");
  }
  
  });
  
  
  function showResults(result,inputs){
  
  const risk = Math.round(result.risk*100);
  
  riskPercent.textContent = risk + "%";
  previewRisk.textContent = risk + "%";
  
  resultRing.style.background =
  `conic-gradient(#e94f4f 0% ${risk}%, #eee ${risk}% 100%)`;
  
  riskBadge.textContent = risk > 50 ? "High Risk" : "Low Risk";
  
  populateTable(inputs);
  drawChart(inputs);
  
  paramsCard.classList.add("hidden");
  resultsSection.classList.remove("hidden");
  
  }
  
  
  function populateTable(data){
  
  rawTable.innerHTML = "";
  
  Object.keys(data).forEach(function(key){
  
  const row = document.createElement("tr");
  
  row.innerHTML = `
  <td>${key}</td>
  <td>${data[key]}</td>
  `;
  
  rawTable.appendChild(row);
  
  });
  
  }
  
  
  function drawChart(data){
  
  const labels = Object.keys(data);
  const values = Object.values(data);
  
  if(chart){
  chart.destroy();
  }
  
  chart = new Chart(chartCanvas,{
  type:"bar",
  data:{
  labels:labels,
  datasets:[{
  label:"Patient Parameters",
  data:values
  }]
  }
  });
  
  }
  
  });