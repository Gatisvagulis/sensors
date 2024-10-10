<template>
  <div class="container">
    <!-- Input field for searching sensors by name -->
    <input
      class="search-input"
      v-model="searchQuery"
      placeholder="Search by sensor name"
    />
    <!-- Dropdown for filtering sensors by type -->
    <select
      v-model="selectedSensorType"
      class="filter-dropdown"
    >
      <option value="">All sensor types</option>
      <option
        v-for="(variant, typeId) in sensorTypes"
        :key="typeId"
        :value="typeId"
      >
        {{ variant[Object.keys(variant)[0]].name }}
      </option>
    </select>
    <!-- Checkbox list for toggling visibility of metric columns -->
    <div class="checkbox-container">
      <label
        class="metric-checkbox"
        v-for="metric in metrics"
        :key="metric.id"
      >
        <input
          type="checkbox"
          :value="metric.id"
          v-model="visibleMetrics"
        />
        {{ metric.name }} {{ metric.unit }}
      </label>
    </div>
    <!-- Table displaying sensors and their metrics -->
    <table class="styled-table">
      <thead>
        <tr>
          <!-- Column for sensor name, sortable -->
          <th @click="sortBy('name')">Sensor Name</th>
          <!-- Dynamic columns for visible metrics, sortable -->
          <th
            v-for="metric in visibleMetricColumns"
            :key="metric.id"
            @click="sortBy(metric.id)"
          >
            {{ metric.name }} {{ metric.unit }}
          </th>
        </tr>
      </thead>
      <tbody>
        <!-- Rows for each sensor, with columns for each visible metric -->
        <tr
          v-for="sensor in filteredAndSortedSensors"
          :key="sensor.id"
        >
          <td>{{ sensor.name || "Unnamed Sensor" }}</td>
          <td
            v-for="metric in visibleMetricColumns"
            :key="metric.id"
          >
            {{ sensor.metrics[metric.id]?.v || "N/A" }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
const sensors = ref([]); // Stores sensor data
const metrics = ref([]); // Stores metric data
const sensorTypes = ref([]); // Stores sensor type data

const searchQuery = ref(""); // User input for search query
const sortOrder = ref("name"); // Tracks the current sorting order ('asc' or 'desc')
const sortKey = ref("asc"); // Tracks the column used for sorting
const selectedSensorType = ref(""); // Stores the selected sensor type for filtering

// Tracks the IDs of the visible metrics (for toggling columns)
const visibleMetrics = ref([]);

// Computed property to get only the visible metrics (based on checkboxes)
const visibleMetricColumns = computed(() => {
  return metrics.value.filter((metric) =>
    visibleMetrics.value.includes(metric.id)
  );
});

// Computed property to filter and sort the sensors based on user input
const filteredAndSortedSensors = computed(() => {
  return sensors.value
    .filter((sensor) => {
      // Filters sensors by name and selected sensor type
      const matchName = sensor.name
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase());
      const matchTypes = selectedSensorType.value
        ? sensor.type === parseInt(selectedSensorType.value)
        : true;
      return matchName && matchTypes;
    })
    .sort((a, b) => {
      // Sorting logic based on the selected sort key and order
      const modifier = sortOrder.value === "asc" ? 1 : -1;
      if (sortKey.value === "name") {
        // Sort by sensor name
        if (a.name < b.name) return -1 * modifier;
        if (a.name > b.name) return 1 * modifier;
        return 0;
      } else {
        // Sort by metric value (using the metric ID as the sort key)
        const aMetricValue = a.metrics[sortKey.value]?.v || 0;
        const bMetricValue = b.metrics[sortKey.value]?.v || 0;
        if (aMetricValue < bMetricValue) return -1 * modifier;
        if (aMetricValue > bMetricValue) return 1 * modifier;
        return 0;
      }
    });
});

// Function to fetch data from the API (sensors, sensorTypes, and metrics)
const fetchData = async () => {
  try {
    const sensorsData = await $fetch("/api/sensors");
    const metricsData = await $fetch("/api/metrics");
    // Storing the fetched data into the reactive variables
    sensorTypes.value = await $fetch("/api/sensorTypes");
    sensors.value = Object.values(sensorsData);
    metrics.value = metricsData.data.items.map((metric) => ({
      id: metric.id,
      name: metric.name,
      unit: metric.units.find((u) => u.selected).name,
    }));
    // By default, make all metrics visible
    visibleMetrics.value = metrics.value.map((metric) => metric.id);
  } catch (error) {
    console.log(error); // Handle API fetch errors
  }
};

// Function to handle sorting when a column header is clicked
const sortBy = (key) => {
  // If the same column is clicked, toggle the sort order
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    // Set the sort key to the newly clicked column and reset the sort order
    sortKey.value = key;
    sortOrder.value = "asc";
  }
};
// Fetch data from the API when the component is created
fetchData();
</script>

<style lang="css" scoped>
.container {
  padding: 20px;
  max-width: 100%;
}

.search-input,
.filter-dropdown {
  padding: 10px;
  margin-bottom: 20px;
  width: 300px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.checkbox-container {
  margin-bottom: 20px;
}

.metric-checkbox {
  margin-right: 15px;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 16px;
}

.styled-table thead {
  background-color: #f4f4f4;
}

.styled-table th,
.styled-table td {
  padding: 10px 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
  cursor: pointer;
}

.styled-table th {
  background-color: #007bff;
  color: white;
}

.styled-table tr:hover {
  background-color: #f1f1f1;
}

.styled-table tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>
